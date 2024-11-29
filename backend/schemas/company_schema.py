from marshmallow import Schema, fields

class CompanySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()