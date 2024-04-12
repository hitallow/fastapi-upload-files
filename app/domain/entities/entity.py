from pydantic import BaseModel


def to_camel_case(snake_prop: str):
    splited = snake_prop.split("_")
    return splited[0] + "".join(letter.title() for letter in splited[1:])


class BaseClassConfig:
    populate_by_name = True
    alias_generator = to_camel_case


class Entity(BaseModel):
    class Config(BaseClassConfig):
        pass
