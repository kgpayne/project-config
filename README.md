# Project Config

Project config for humans.

Define your config as Python classes and map them to files on disk.

Key features:

- ORM-style class definitions of config objects.
- Classes mapped to files for reading and writing.
- Automated JSONSchema generation of mapped files.

## Example

```python
import project_config as pc


class SettingGroupValidation(pc.Model):
    pass


class Setting(pc.Model):
    pass


class Extractor(pc.Model):
    __metadata__ = {"additionalProperties": True}
    name = pc.Field(str, required=True)
    inherit_from = pc.Field(str)
    pip_url = pc.Field(str)
    variant = pc.Field(str)
    namespace = pc.Field(str)
    config = pc.Field(str)
    label = pc.Field(str)
    logo_url = pc.Field(str)
    executable = pc.Field(str)
    settings = pc.Array(Setting)
    docs = pc.Field(str)
    settings_group_validation = pc.Array(SettingGroupValidation)
    commands = pc.Field(str)


class Plugins(pc.Model):
    __metadata__ = {"additionalProperties": False}
    extractors = pc.Array(Extractor)


class ProjectFile(pc.Model):
    __metadata__ = {
        "title": "A Project file.",
        "description": "Project is an Open Source project. Read more at https://github.com/kgpayne/project-config",
    }
    plugins = pc.Field(Plugins)


example_project_values = {
    "plugins": {
        "extractors": [
            {
                "name": "test-extractor",
                "inherit_from": "test-inherit-from",
                "pip_url": "test-pip-url",
            }
        ]
    }
}

project_config = ProjectFile.from_dict(example_project_values)
print(project_config.plugins.extractors[0].name)
# $ "test-extractor"
```

## Notes

- [`json-schema-to-class`](https://github.com/FebruaryBreeze/json-schema-to-class) and [`warlock`](https://github.com/bcwaldon/warlock) offer inspiration for mapping to and from JSONSchema.
- Consider [`ruamel`](https://yaml.readthedocs.io/en/latest/index.html) for reading and writing YAML, maintaining comments.
- Consider [`benedict`](https://github.com/fabiocaccamo/python-benedict) for json-style key paths in Python (if needed).

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
