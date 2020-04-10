# avrod_ecommerce

### Requirements
* latest version of Python and Postgres
### Setup Steps
1. Clone this repository
2. Run a virtual environment with the command `pipenv shell`
3. Install dependencies with command `pip install`
4. Create a postgres database with information listed in DATABASES in settings.py
    - source/app/conf/development/settings.py
5. Run the local server using command `python source/manage.py runserver`
6. Create a [Stripe](https://stripe.com/en-ca) account and update the Stripe keys in settings.py
7. Change any other secret keys as needed

### Explanation of Apps
#### Accounts
- Cloned from: https://github.com/egorsmkv/simple-django-login-and-register and updated for our specifications
- Contains everything for managing user accounts
- Templates folder:  contains all the html pages for account management, as well as email templates
- Users are required to activate their accounts before accessing the website. When the website is setup locally with no way of sending emails you must manually change their 'is_active' value to true in the database with `update auth_user set is_active = 't' where username = '[account username]'`

#### App
- Contains the website settings in the conf folder under development or production. Right now all the current settings are defined in the development settings.py folder
- Has top level url paths in urls.py

#### Content
- This isn't really an app, it contains all static files being used within the project such as css files, javascript, images, and html layout templates

#### Main
- Contains the code for the index and change language pages in views.py

#### Payment
- Contains all code that manages payment in the website
- templates folder contains all html page templates
- admin.py contains code required to access payment model objects through the admin portal of the website (<site url>/admin)
- keygen.py contains code required to generate license keys when the user signs up for a subscription

##### Webhook Receiver
- Stripe has [instructions](https://stripe.com/docs/stripe-cli) on how to test a locally running web site using Stripe CLI
    - The endpoint_secret in `source/payment/views.py` immediately above the webhook receiver function towards the bottom of the file needs to be changed to the one the Stripe CLI gives you
- When the website is publicly accessible through the internet, webhooks can be tested through the Stripe dashboard following [these instructions](https://stripe.com/docs/webhooks/test#dashboard)
- Currently the only events being handled are checkout.session.completed and customer.subscription.deleted
