from marshmallow import Schema, fields

class CompanySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    

class ProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    company_id = fields.Int()