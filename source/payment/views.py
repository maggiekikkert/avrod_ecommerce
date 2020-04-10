from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from .models import Customer, Subscription, License
from .keygen import generate
import stripe
import json
import os
import datetime

stripe.api_key = settings.STRIPE_SECRET_KEY
global stripe_customer

# License Management page
class LicenseView(LoginRequiredMixin, TemplateView):
    template_name = 'license.html'

    def get(self, request):
        user = self.request.user
        customer = Customer.objects.filter(user_id=user)

        # If the user is already a stripe customer, send their stripe customer id through the session
        if customer.exists():
            customer_id = Customer.objects.values_list('customer_id', flat=True).get(user_id=user)
            subscription = Subscription.objects.filter(customer_id=customer_id)
            # if they have an active subscription send them to the management page
            if subscription.exists():
                subscription = Subscription.objects.get(customer_id=customer_id)
                last_period = stripe.Subscription.retrieve(subscription.sub_id).cancel_at_period_end
                request.session['sub_last_period'] = last_period    # store info in the browser session
                return redirect('payment:manage', sub_id=subscription.sub_id)
            # otherwise send to the page to sign up for a new subscription
            else:
                session = stripe.checkout.Session.create(
                    customer = customer_id,
                    payment_method_types=['card'],
                    subscription_data={
                        'items': [{
                            'plan': 'plan_GfW2im5hu5EkF1',
                        }],
                    },
                    success_url='http://127.0.0.1:8000/licensing/success?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url='http://127.0.0.1:8000/licensing/',
                    metadata= {
                        'avrod_id': user.id
                    }
                )
        # if they aren't already a stripe customer create a session with no customer id
        else:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                subscription_data={
                    'items': [{
                        'plan': 'plan_GfW2im5hu5EkF1',
                    }],
                },
                success_url='http://127.0.0.1:8000/licensing/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://127.0.0.1:8000/licensing/',
                metadata= {
                    'avrod_id': user.id
                }
            )

        # Pass the session id to the html page so it can be accessed by Stripe Checkout
        context = {
            'session_id': session.id
        }

        return render(request, self.template_name, context)
        

# Display Payment success page
class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'success.html'

    def get(self, request):
        return render(request, self.template_name)


# Display subscription management page
class ManageLicenseView(LoginRequiredMixin, TemplateView):
    template_name = 'manage.html'

    def get(self, request, *args, **kwargs):
        # Get the subscription information
        sub_id = kwargs.get('sub_id')
        last_period = request.session.get('sub_last_period')
        subscription = Subscription.objects.get(sub_id=sub_id)

        # Create a checkout session in case user wants to update payment information
        session = stripe.checkout.Session.create(
            customer=subscription.customer_id.customer_id,
            payment_method_types=['card'],
            mode='setup',
            setup_intent_data={
                'metadata': {
                    'subscription_id': sub_id
                },
            },
            success_url='http://localhost:8000/licensing/manage/'+sub_id+'/success/',
            cancel_url='http://localhost:8000/licensing/manage/'+sub_id+'/',
            metadata={
                'avrod_id': self.request.user.id,
            }
        )

        # Send subscription information to the html template
        context = {
            'session_id': session.id,
            'subscription': subscription,
            'last_period': last_period,
        }
        return render(request, self.template_name, context)


# Process subscription cancellation request and display success message
class CancelSubscriptionView(LoginRequiredMixin, TemplateView):
    template_name = 'cancel.html'
    
    def get(self, request, *args, **kwargs):
        # Get the subscription information
        sub_id = kwargs.get('sub_id')
        subscription = Subscription.objects.get(sub_id=sub_id)

        # Set that the subscription will end at the end of current period
        stripe.Subscription.modify(
            sub_id,
            cancel_at_period_end=True
        )

        # Send sub id to the html page
        context = {
            'sub_id': sub_id,
        }

        return render(request, self.template_name, context)


# Display success message after updating payment method for subscription
class UpdateSubscriptionView(LoginRequiredMixin, TemplateView):
    template_name = 'update-success.html'

    def get(self, request, *args, **kwargs):
        sub_id = kwargs.get('sub_id')
        context = {
            'sub_id': sub_id,
        }

        return render(request, self.template_name, context)


# Process Subscription reactivation and display success message
class ReactivateSubscriptionView(LoginRequiredMixin, TemplateView):
    template_name = 'reactivate.html'

    def get(self, request, *args, **kwargs):
        # Get subscription information
        sub_id = kwargs.get('sub_id')
        subscription = Subscription.objects.get(sub_id=sub_id)

        # Update subscription to not end at the end of current period
        stripe.Subscription.modify(
            sub_id,
            cancel_at_period_end=False,
        )

        # Send sub id to the html template
        context = {
            'sub_id': sub_id,
        }

        return render(request, self.template_name, context)


# Webhook Receiver
endpoint_secret = 'whsec_P2OxXQZFSLJ1F5kgPULOEKa0DcoqjVJj'  # This will change when you set up your own webhook receiver through stripe
@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print("checkout.session.completed")
        print(session)

        user = User.objects.get(id = session.metadata.avrod_id)
        print(user)

        customer = Customer.objects.filter(user_id=user)
        print(customer)
        customer_id = session.customer
        if not customer.exists():
            print('creating customer')
            # Create customer in Django
            customer = Customer.create(
                customer_id,
                user
            )
            customer.save()
        else:
            print('retrieving customer')
            customer = Customer.objects.get(user_id=user)

        subscription = Subscription.objects.filter(customer_id=customer.customer_id)
        print(subscription)
        if subscription.exists():
            print('updating payment method')
            # User is updating their card information
            intent_id = session.setup_intent
            intent = stripe.SetupIntent.retrieve(intent_id)
            print(intent)
            print(stripe.Customer.retrieve(intent.customer))
            stripe.Customer.modify(
                customer.customer_id,
                invoice_settings={'default_payment_method': intent.payment_method}
            )
            print('updated subscription')
            return HttpResponse(status=200)
        else:
            print('creating subscription')
            # User needs a subscription
            key = generate(get_random_string(32))
            license_key = License.create(key)
            license_key.save()
            stripe_sub = stripe.Subscription.retrieve(session.subscription)
            sub_end_date = datetime.datetime.fromtimestamp(float(stripe_sub.current_period_end)).date()

            subscription = Subscription.create(
                stripe_sub.id,
                customer,
                license_key,
                sub_end_date
            )
            subscription.save()

    # Handle customer.subscription.deleted event
    elif event['type'] == 'customer.subscription.deleted':
        session = event['data']['object']
        customer = session.customer

        subscription = Subscription.objects.get(customer_id=customer)
        License.objects.filter(license_key=subscription.license_key).delete()
        Subscription.objects.filter(sub_id=subscription.sub_id).delete()

    return HttpResponse(status=200)