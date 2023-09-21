from .Base import BaseModel
from .User import User
from peewee import ForeignKeyField


class Followers(BaseModel):
    current = ForeignKeyField(User,field="id")
    following = ForeignKeyField(User,field="id")