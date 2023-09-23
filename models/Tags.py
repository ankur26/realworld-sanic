from peewee import CharField

from .Base import BaseModel

class Tags(BaseModel):
    tag = CharField(unique=True)
