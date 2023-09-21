from .Base import BaseModel
from peewee import CharField, BlobField

class User(BaseModel):
    username = CharField(unique=True)
    password = BlobField()
    email = CharField(unique=True)
    bio = CharField(null=True)
    image = CharField(null=True)

    def __repr__(self) -> str:
        return f"username-{self.username},email-{self.email}"