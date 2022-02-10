from datetime import date, datetime
from typing import Literal, Union

from pydantic import BaseModel, Field, SecretStr, validator
from typing_extensions import Annotated


class ConfigModel(BaseModel):
    pass


class _BaseSettingDefinition(BaseModel):
    name: str
    label: str = None
    kind: str


class StringSetting(_BaseSettingDefinition):
    kind: Literal["string"]
    value: str = None


class IntegerSetting(_BaseSettingDefinition):
    kind: Literal["integer"]
    value: int = None


class PasswordSetting(_BaseSettingDefinition):
    kind: Literal["password"]
    value: SecretStr = None


class DatetimeSetting(_BaseSettingDefinition):
    kind: Literal["datetime"]
    value: Union[datetime, date] = None


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
