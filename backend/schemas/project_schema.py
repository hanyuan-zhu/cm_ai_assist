from marshmallow import Schema, fields

class ProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    company_id = fields.Int()