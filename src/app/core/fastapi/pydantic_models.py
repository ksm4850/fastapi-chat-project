import inspect

from fastapi import Form
from fastapi.exceptions import RequestValidationError
from pydantic import BaseConfig, BaseModel, ConfigDict, ValidationError

from app.core.utils.camelcase import snake2camel


class BodyBaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=snake2camel)


class ResponseBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=snake2camel,
        populate_by_name=True,
        from_attributes=True,
    )
