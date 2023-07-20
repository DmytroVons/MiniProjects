#!/usr/bin/python3
from marshmallow import Schema, fields, validate


class EntitySchema(Schema):
    id = fields.UUID(required=True)
    name = fields.String(required=True, validate=validate.Length(min=3, max=10))


class PersonSchema(Schema):
    id = fields.UUID(required=True)
    firstName = fields.String(required=True, validate=validate.Length(max=50))
    lastName = fields.String(required=True, validate=validate.Length(max=50))
    dateOfBirth = fields.DateTime(format="%Y-%m-%d")
    email = fields.Email(required=True)
    contactNumber = fields.String(required=True, validate=validate.Length(max=30))
    age = fields.Integer(validate=validate.Range(min=1, max=150))
    salary = fields.Decimal(required=True)
    address = fields.String(validate=validate.Length(min=3, max=50))
    entities = fields.Nested(EntitySchema(), many=True)
