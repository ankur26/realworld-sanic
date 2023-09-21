from peewee import SqliteDatabase, Model

class BaseModel(Model):
    class Meta:
        database = SqliteDatabase("conduit.db")
        