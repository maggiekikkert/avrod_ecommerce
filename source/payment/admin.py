from django.contrib import admin

from .models import Session, License, Customer, Subscription

admin.site.register(Session)
admin.site.register(License)
admin.site.register(Customer)
admin.site.register(Subscription)
