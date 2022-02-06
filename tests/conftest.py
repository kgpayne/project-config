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
    __metadata__ = {
        "additionalProperties": False
    }
    extractors = pc.Array(Extractor)


class ProjectFile(pc.Model):
    __metadata__ = {
        "title": "A Project file.",
        "description": "Project is an Open Source project. Read more at https://github.com/kgpayne/project-config"
    }
    plugins = pc.Field(Plugins)


example_project_values = {
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


@pytest.fixture
def example_project_dict():
    return example_project_values


@pytest.fixture
def example_project(example_project_dict):
    return ProjectFile.from_dict(
        example_project_dict
    )
