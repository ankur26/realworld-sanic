from peewee import CharField

from .base import BaseModel


class Tag(BaseModel):
    tag = CharField(unique=True)
