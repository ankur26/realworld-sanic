from peewee import CharField, Model


class Tag(Model):
    tag = CharField(unique=True)
