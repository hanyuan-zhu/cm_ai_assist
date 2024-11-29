from marshmallow import Schema, fields

class EmployeeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    position = fields.Str()
    hire_date = fields.Date()
    status = fields.Str()
    company_id = fields.Int()
    project_id = fields.Int()
    creator_id = fields.Int()