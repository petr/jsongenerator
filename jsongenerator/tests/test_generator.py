

import json
from jsonschema import validate

from jsongenerator.jsongenerator import Parser, Generator

FAKE_SCHEMA = '''{
    "$schema": "http://json-schema.org/draft-04/schema",
    "additionalProperties": false,
    "type": "object",
    "definitions": {
        "item": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "item_name": {
                    "type": "string"
                }
            }
        }
    },
    "properties": {
        "number": {
            "type": "integer"
        },
        "flag": {
            "type": "boolean"
        },
        "status": {
            "enum": ["active", "frozen"]
        },
        "items": {
            "type": "array",
            "items": [
                { "$ref": "#/definitions/item" }
            ]
        }
    }
}'''


def test_all():
    schema = json.loads(FAKE_SCHEMA)
    parser = Parser(schema)
    parsed_data = parser.begin()
    generator = Generator()
    generated_data = generator.generate(parsed_data)
    validate(generated_data, schema)
