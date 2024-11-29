from marshmallow import Schema, fields

class ChangeSchema(Schema):
    id = fields.Int(dump_only=True)
    type = fields.Str()
    employee_id = fields.Int()
    from_company_id = fields.Int()
    to_company_id = fields.Int()
    from_project_id = fields.Int()
    to_project_id = fields.Int()
    effective_date = fields.Date()
    status = fields.Str()