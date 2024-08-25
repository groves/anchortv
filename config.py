from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


class Class(BaseModel):
    name: str
    hour: int
    days: list[str]
    sheet: str


class Config(BaseSettings):
    classes: list[Class]
    model_config = SettingsConfigDict(toml_file="config.toml")

    @classmethod
    def settings_customise_sources(cls, settings_cls, *_, **__):
        return (TomlConfigSettingsSource(settings_cls),)
