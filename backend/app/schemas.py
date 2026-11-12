from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


# creating these classes are important because they describe how data can be stored, and what data is allowed to come in and out of the API

class OperatorBase(BaseModel): 
    operator_name: str = Field(min_length=1, description="The operator's name in MW4 2026")
    real_name: str = Field(min_length=1, description="The operator's real name")
    faction: str = Field(min_length=1, description="The faction the operator is a part of (what group they belong to)")
    nationality : str = Field (min_length=1, description="The nation the operator is from")
    language : str = Field (min_length=1, description="The language the operator speaks")
    is_available: bool = Field (description = "Whether the operator can be bought from a bundle or not")
    image_of_operator: str = Field (description = "The picture of the operator (Got it from MW 2026 page)")


class OperatorCreate(OperatorBase):
    """Body of a POST request. No `id`: the database assigns it."""


class OperatorUpdate(OperatorBase):
    """Body of a PUT request. An update replaces every field."""


class OperatorResponse(OperatorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
