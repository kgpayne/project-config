import os
from pathlib import Path
from typing import Any, Dict, List, Literal, Union

import pytest
from pydantic import BaseModel, Field, SecretStr, validator
from typing_extensions import Annotated

from project_config.orm import (
    ConfigModel,
    DatetimeSetting,
    IntegerSetting,
    PasswordSetting,
    StringSetting,
)
from project_config.project_dir import ProjectDir, ProjectFile, ProjectFilePattern


class Command(BaseModel):
    args: str
    executable: str = None


class SettingDefinition(BaseModel):
    __root__: Annotated[
        Union[StringSetting, IntegerSetting, PasswordSetting, DatetimeSetting],
        Field(discriminator="kind"),
    ]

    @validator("__root__", pre=True)
    def ensure_kind(cls, v):
        if "kind" not in v:
            v["kind"] = "string"
        return v

    # These are required because __root__ doesn't expose the wrapped type attributes
    @property
    def name(self):
        return self.__root__.name

    @property
    def label(self):
        return self.__root__.label

    @property
    def value(self):
        return self.__root__.value

    @property
    def kind(self):
        return self.__root__.kind


class PluginModel(ConfigModel):
    name: str
    inherit_from: str = None
    pip_url: str = None
    variant: str = None
    namespace: str = None
    config: Dict[str, Any] = Field(default_factory=dict)
    label: str = None
    logo_url: str = None
    executable: str = None
    settings: List[SettingDefinition] = Field(default_factory=list)
    docs: str = None
    settings_group_validation: List[str] = Field(default_factory=list)
    commands: Dict[str, Command] = Field(default_factory=dict)


@pytest.fixture(scope="class")
def example_config_model():
    return PluginModel


@pytest.fixture(scope="class")
def example_config_values():
    return {
        "name": "tap-github",
        "pip_url": "git+https://github.com/MeltanoLabs/tap-github.git",
        "namespace": "tap_github",
        "settings": [
            {
                "name": "repo",
                # "kind": "string",
            },
            {
                "name": "token",
                "kind": "password",
                "value": "s3cr3t",
            },
            {
                "name": "some_number",
                "kind": "integer",
                "value": "10",
            },
            {
                "name": "start_date",
                "kind": "datetime",
                "value": "2021-01-01",
            },
        ],
        "commands": {
            "info": {
                "args": "--test",
            }
        },
    }


@pytest.fixture(scope="class")
def example_project_directory(example_config_model):
    project_root = os.path.join(
        os.path.dirname(__file__), "fixtures", "example_project"
    )
    meltano_file = ProjectFile(
        model=example_config_model, path=Path("meltano.yml"), required=True
    )
    meltano_files = ProjectFilePattern(
        model=example_config_model,
        include_glob_patterns=["*.meltano.yml", "**/*.meltano.yml"],
    )
    return ProjectDir(root=project_root, files=[meltano_file, meltano_files])
