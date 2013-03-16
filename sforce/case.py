from sforce import schema

class Case(schema.Model):
    id = schema.Integer() # ID references case number
    summary = schema.String()
    description = schema.Text()
    customer_id = schema.Integer()

