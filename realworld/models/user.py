from peewee import BlobField, CharField, Model


class User(Model):
    username = CharField(unique=True)
    password = BlobField()
    email = CharField(unique=True)
    bio = CharField(null=True)
    image = CharField(null=True)
