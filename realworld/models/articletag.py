from peewee import ForeignKeyField, Model

from .article import Article
from .tag import Tag


class TagToArticle(Model):
    articleid = ForeignKeyField(Article, field="id")
    tagid = ForeignKeyField(Tag, field="id")
