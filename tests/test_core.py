import pytest
import project_config as pc


class SettingGroupValidation(pc.Model):
    pass


class Setting(pc.Model):
    pass


class Extractor(pc.Model):
    __metadata__ = {
        "additionalProperties": True
    }
    name = pc.Item(str, required=True)
    inherit_from = pc.Item(str)
    pip_url = pc.Item(str)
    variant = pc.Item(str)
    namespace = pc.Item(str)
    config = pc.Item(str)
    label = pc.Item(str)
    logo_url = pc.Item(str)
    executable = pc.Item(str)
    settings = pc.Array(Setting)
    docs = pc.Item(str)
    settings_group_validation = pc.Array(SettingGroupValidation)
    commands = pc.Item(str)


class Plugins(pc.Model):
    __metadata__ = {
        "additionalProperties": False
    }
    extractors = pc.Array(Extractor)


class ProjectFile(pc.Model):
    __metadata__ = {
        "title": "A Project file.",
        "description": "Project is an Open Source project. Read more at https://github.com/kgpayne/project-config"
    }
    plugins = pc.Item(Plugins)


example_project_file_dict = {
    "plugins": {
        "extractors": [
            {
                "name": "test-extractor",
                "inherit_from": "test-inherit-from",
                "pip_url": "test-pip-url"
            }
        ]
    }
}

pf = ProjectFile.from_dict(example_project_file_dict)

def test_dict_storage():
    assert pf._dict == example_project_file_dict

def test_properties_created():
    top_keys = [
        k for k in list(pf.__class__.__dict__.keys())
        if not k.startswith('__')
    ]
    assert top_keys == [
        '_dict', '_model', 'plugins'
    ]

    plugins_keys = [
        k for k in list(pf.plugins.__class__.__dict__.keys())
        if not k.startswith('__')
    ]
    assert plugins_keys == [
        '_dict', '_model', 'extractors'
    ]

    extractor_keys = [
        k for k in list(pf.plugins.extractors[0].__class__.__dict__.keys())
        if not k.startswith('__')
    ]
    assert extractor_keys == [
        '_dict', '_model', 'name', 'inherit_from', 'pip_url'
    ]


def test_edit_dict():
    pf.plugins.extractors[0].name = 'updated-test-extractor'
    assert example_project_file_dict['plugins']['extractors'][0]['name'] == 'updated-test-extractor'


def test_required_field():
    """ This should raise on instantiation ideally.
    """
    example_project_file_dict['plugins']['extractors'][0].pop('name')
    with pytest.raises(pc.RequiredFieldError):
        pf = ProjectFile.from_dict(example_project_file_dict)
        pf.plugins.extractors[0].name
