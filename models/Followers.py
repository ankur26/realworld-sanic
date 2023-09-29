from peewee import ForeignKeyField

from .Base import BaseModel
from .User import User


class Followers(BaseModel):
    current = ForeignKeyField(User, field="id")
    following = ForeignKeyField(User, field="id")
