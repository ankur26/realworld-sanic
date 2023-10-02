"""
This is the primary helper to get articles in all kinds of scenarios
Whether it be with or without a user
Whether it be with or without a filter
With some standard defaults for pagination
"""

from peewee import IntegrityError
from playhouse.shortcuts import model_to_dict
from sanic import NotFound, SanicException
from sanic.log import logger

from ..models.article import Article
from ..models.articletag import TagToArticle
from ..models.comment import Comment
from ..models.follower import Follower
from ..models.tag import Tag
from ..models.user import User
from ..models.userfavorite import FavoritedArticlesByUser


async def following(current: int, following: int) -> bool:
    logger.info("following: running for id {} to id {}".format(current, following))
    return Follower.get_or_none(current=current, following=following) is not None


async def favorited(userid: int, articleid: int) -> bool:
    logger.info(
        "favorited: running for user {} to article {}".format(userid, articleid)
    )
    return (
        FavoritedArticlesByUser.get_or_none(userid=userid, articleid=articleid)
        is not None
    )


async def favorite_count(articleid: int) -> bool:
    logger.info("favorite_count: running for article {}".format(articleid))
    return FavoritedArticlesByUser.select(
        FavoritedArticlesByUser.articleid == articleid
    ).count()


async def get_tags(articleid):
    logger.info("get_tags: running for {}".format(articleid))
    tags = (
        TagToArticle.select()
        .join(Tag, on=(Tag.id == TagToArticle.tagid))
        .join(Article, on=(Article.id == TagToArticle.articleid))
        .where(Article.id == articleid)
    )
    return [tag.tagid.tag for tag in tags]


async def get_follower_articles(userid, limit, offset):
    logger.info(
        "get_follower_articles with limit {} for user {} starting from offset {}".format(
            limit, userid, offset
        )
    )
    subquery_user = Follower.select(Follower.following).where(
        Follower.current == userid
    )
    query_for_user = (
        Article.select(Article)
        .join(User)
        .where(Article.author.in_(subquery_user))
        .order_by(Article.updatedAt)
    )
    counts_of_followed_articles = query_for_user.count()
    lower, higher = offset, offset + limit
    if counts_of_followed_articles <= lower:
        return [
            model_to_dict(row)
            for row in query_for_user.paginate(1, counts_of_followed_articles)
        ]
    elif lower < counts_of_followed_articles < higher:
        return [
            model_to_dict(row)
            for row in query_for_user.paginate(lower + 1, counts_of_followed_articles)
        ]
    else:
        return [
            model_to_dict(row) for row in query_for_user.paginate(lower + 1, higher)
        ]


async def get_all_articles(limit, offset, tag, author, favorite):
    # query building sequence starts
    # Not sure if this is the right assumption but we're going to assume that all inputs can arrive at the same time
    logger.info(
        "get_all_articles: fetching articles with linit {} offset {} tag {} author {} favorite {}".format(
            limit, offset, tag, author, favorite
        )
    )
    subquery = None
    if tag and not author and not favorite:
        t = Tag.get_or_none(tag=tag)
        if t:
            subquery = TagToArticle.select(TagToArticle.articleid).where(
                TagToArticle.tagid == t
            )
        else:
            # raise SanicException("Tag not found",404)
            return []
    elif not tag and author and not favorite:
        user_id = User.get_or_none(username=author)
        if user_id:
            subquery = Article.select(Article.id).where(Article.author == user_id)
        else:
            # raise SanicException("Author not found",404)
            return []
    elif not tag and not author and favorite:
        user_id = User.get_or_none(username=favorite)
        if user_id:
            subquery = FavoritedArticlesByUser.select(
                FavoritedArticlesByUser.articleid
            ).where(FavoritedArticlesByUser.userid == user_id)
        else:
            # raise SanicException("No user like this exists",404)
            return []

    lower = offset
    higher = offset + limit
    res = []

    if subquery is not None:
        if subquery.count() == 0:
            return []
        else:
            query = Article.select().where(Article.id.in_(subquery))
    else:
        query = Article.select()

    counts_for_articles = query.count()
    logger.info(
        "We have total {} articles and filtered {} articles".format(
            Article.select().count(), subquery.count()
        )
    )
    if counts_for_articles < lower:
        res = [model_to_dict(row) for row in query.paginate(1, counts_for_articles)]
    elif lower <= counts_for_articles <= higher:
        res = [
            model_to_dict(row) for row in query.paginate(lower + 1, counts_for_articles)
        ]
    else:
        res = [model_to_dict(row) for row in query.paginate(lower + 1, higher)]
    return res


async def get_tags_following_favorite_information(article, user=None):
    logger.info(
        "get_tags_following_favorite_information: for article {} with user {}".format(
            article["id"], user["username"] if user else "anonymous"
        )
    )
    article["tagList"] = await get_tags(article["id"])
    article["favorited"] = await favorited(user["id"], article["id"]) if user else False
    article["author"]["following"] = (
        await following(user["id"], article["author"]["id"]) if user else False
    )
    article["favoritesCount"] = await favorite_count(article["id"])
    return article


async def get_articles_from_helper(
    single: bool = True,
    slug: str = "",
    user: dict = None,
    limit: int = 20,
    offset: int = 0,
    author: str = "",
    tag: str = "",
    favorite: str = "",
    name: str = "",
) -> dict:
    # print(author,tag,favorite)
    if single:
        logger.info("get_articles_from_helper: single")
        return await get_tags_following_favorite_information(
            user, model_to_dict(Article.get(Article.slug == slug))
        )
    else:
        # We will ignore the slug here and ideally we should not get a slug in this request
        results = None
        if user and name == "get_feed":
            logger.info("get_articles_from_helper: user and get_feed")
            results = await get_follower_articles(user["id"], limit, offset)
        elif (user and name == "get_articles") or (not user and name == "get_articles"):
            logger.info("get_articles_from_helper: user and get_articles")
            results = await get_all_articles(limit, offset, tag, author, favorite)
        for r in results:
            # The results here only give us a few things, i.e the article and the author.
            # There's a few more things that need to be added, i.e following the user (if there is a user)
            # Checking the favorited counts, and also checking whether you've favorited that article.
            r = await get_tags_following_favorite_information(r, user)
        return results


async def get_single_article(user, article_id=None, article_slug=None):
    logger.info("get_single_article")
    if article_id or article_slug:
        try:
            article_query = (
                Article.select().where(Article.id == article_id)
                if article_id
                else Article.select().where(Article.slug == article_slug)
            )
            if article_query.count() == 0:
                raise NotFound("The slug or ID does not exist")
        except IntegrityError as ie:
            raise SanicException(
                f"There has been an an internal server error {ie}", 500
            )
        return await get_tags_following_favorite_information(
            [model_to_dict(row) for row in article_query][0], user
        )


async def get_comments(user, article):
    logger.info("get_comments")
    results = [
        model_to_dict(row)
        for row in Comment.select().where(Comment.articleid == article)
    ]
    for r in results:
        del r["articleid"]
        r["author"] = r["userid"]
        r["author"]["following"] = (
            await following(user["id"], r["author"]["id"]) if user else False
        )
    return results


async def get_single_comment(user, comment):
    logger.info("get_single_comment")
    comment = model_to_dict(Comment.get_or_none(id=comment))
    del comment["articleid"]
    comment["author"] = comment["userid"]
    comment["author"]["following"] = (
        await following(user["id"], comment["author"]["id"]) if user else False
    )
    return comment
