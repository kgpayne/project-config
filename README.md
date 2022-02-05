# Project Config

Project config for humans.

Define your config as Python classes and map them to files on disk.

Key features:

- ORM-style class definitions of config objects.
- Classes mapped to files for reading and writing.
- Automated JSONSchema generation of mapped files.

## Notes

- Use [`ruamel`](https://yaml.readthedocs.io/en/latest/index.html) for reading and writing YAML, maintaining comments.
- Use [`benedict`](https://github.com/fabiocaccamo/python-benedict) for json-style key paths in Python.

e.g.

```python
import sys
from benedict import benedict
from ruamel.yaml import YAML

inp = """\
# example
people:
  - name:
      # details
      family: Smith   # very common
      given: Alice    # one of the siblings
"""

yaml = YAML()
doc = benedict(yaml.load(inp))
doc['people[0].name.middle'] = 'Anne'
yaml.dump(doc._dict, sys.stdout)
```

- [`json-schema-to-class`](https://github.com/FebruaryBreeze/json-schema-to-class) and [`warlock`](https://github.com/bcwaldon/warlock) offer inspiration for mapping to and from JSONSchema.