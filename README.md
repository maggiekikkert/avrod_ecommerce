# avrod_ecommerce

### Setup Steps
1. Clone this repository
2. Run a virtual environment with the command `pipenv shell`
3. Install dependencies with command `pip install`
4. Create a postgres database with information listed in DATABASES in settings.py
    - source/app/conf/development/settings.py
5. Run the local server using command `python source/manage.py runserver`
6. Create a [Stripe](https://stripe.com/en-ca) account and update the Stripe keys in settings.py
7. Change any other secret keys as needed
