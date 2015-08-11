# jsongenerator

Json schema generator.

## Using
```python
import json

from jsongenerator import jsongenerator

with open('schema.json') as schema_file:
    schema_data = json.loads(schema_file.read())

parser = jsongenerator.Parser(schema_data)
parsed_data = parser.begin()

generator = jsongenerator.Generator()
generated_data = generator.generate(parsed_data)

```

## Runing test

Simple type tox
```
tox
```
