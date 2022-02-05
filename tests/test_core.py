import project_config as pc


class SettingGroupValidation:
    pass


class Setting(pc.Model):
    pass


class Extractor(pc.Model):
    __metadata__ = {
        "additionalProperties": True
    }
    name = pc.Item(str)
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


class ProjectFile(pc.File):
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

def test_dict_persistence():
    pf = ProjectFile(example_project_file_dict)
    assert pf._dict == example_project_file_dict
