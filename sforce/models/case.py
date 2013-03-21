from sforce.models import Schema

class Case(Schema):

    service_name = "Case" 
    def __init__(self):
        super(Case, self).__init__()

Case.register_model()
