#!/usr/bin/env python3
from marshmallow import Schema, fields


class WeatherDataSchema(Schema):
    timestamp = fields.DateTime(format="%Y %m %d %H")
    speed = fields.Float()


class WeatherModelSchema(Schema):
    metadata = fields.Dict()
    data = fields.Nested(WeatherDataSchema, many=True)
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
