from pydantic import BaseModel, ConfigDict


def to_camel_case(snake_prop: str):
    splited = snake_prop.split("_")
    return splited[0] + "".join(letter.title() for letter in splited[1:])


class Entity(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        alias_generator=to_camel_case,
        populate_by_name=True,
    )
