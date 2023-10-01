from peewee import ForeignKeyField, Model

from .user import User


class Follower(Model):
    current = ForeignKeyField(User, field="id")
    following = ForeignKeyField(User, field="id")
