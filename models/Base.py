from peewee import Model, SqliteDatabase


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase("conduit.db")
