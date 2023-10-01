from peewee import ForeignKeyField, Model

from .article import Article
from .user import User


class FavoritedArticlesByUser(Model):
    userid = ForeignKeyField(User, field="id")
    articleid = ForeignKeyField(Article, field="id")
