from sforce.models import Model

class Account(Model):
    service_name = "Account"
    customer_name = None
    contact_email = None
    assets = None
    leads = None
