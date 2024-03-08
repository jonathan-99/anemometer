#!/usr/bin/env python3
from marshmallow import Schema, fields

class WeatherConfigurationSchema(Schema):
    class Meta:
        fields = ("version", "date_submitted", "date_received", "filename", "src_ip", "hostname")

    version = fields.Float()
    date_submitted = fields.DateTime()
    date_received = fields.DateTime()
    filename = fields.String()
    src_ip = fields.String()
    hostname = fields.String()

    # Define the nested schema for the 'data' field
    class DataSchema(Schema):
        filename = fields.String()
        datetime = fields.DateTime()
        speed = fields.Float()

    data = fields.Nested(DataSchema)

    relationship = fields.Dict()

    validation = fields.Dict()


# Usage:
# To deserialize JSON to Python objects:
# data = {...}  # Your JSON data
# schema = WeatherConfigurationFileSchema()
# result = schema.load(data)
# print(result)
#
# To serialize Python objects to JSON:
# python_objects = {...}  # Your Python objects
# schema = WeatherConfigurationFileSchema()
# result = schema.dump(python_objects)
# print(result)
