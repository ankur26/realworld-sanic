from peewee import ForeignKeyField

from .base import BaseModel
from .user import User


class Follower(BaseModel):
    current = ForeignKeyField(User, field="id")
    following = ForeignKeyField(User, field="id")
