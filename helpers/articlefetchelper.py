
'''
The primary helper function for get articles
Options : 
single?=True
id=None or int
user=None or user (for feed based articles)
limit=per get how many articles=20 but can be changed
offset=0 
tag_filter=None or str | 
author = None or str | 
favorited=False | user should exist if this is true
'''
from models.Article import Article
from models.User import User
from models.Tags import Tags
from models.Followers import Followers
from models.TagToArticle import TagToArticle
from models.FavoritedArticlesByUser import FavoritedArticlesByUser
from playhouse.shortcuts import model_to_dict
from sanic import SanicException
from peewee import IntegrityError


async def following(current:int,following:int)->bool:
    return Followers.get_or_none(current=current,following=following) is not None

async def favorited(userid:int,articleid:int)->bool:
    return FavoritedArticlesByUser.get_or_none(userid=userid,articleid=articleid) is not None

async def favorite_count(articleid:int)->bool:
    return FavoritedArticlesByUser.select(FavoritedArticlesByUser.articleid==articleid).count()

async def get_tags(articleid):
    tags = TagToArticle.select().join(
                Tags,on=(Tags.id==TagToArticle.tagid)).join(
                    Article, on=(Article.id==TagToArticle.articleid)).where(
                        Article.id==articleid)
    print(tags.dicts())
    return [tag.tagid.tag for tag in tags]

async def get_follower_articles(userid,limit,offset):
    subquery_user = Followers.select(Followers.following).where(Followers.current == userid)
    query_for_user = Article.select(Article).join(User).where(Article.author.in_(subquery_user)).order_by(Article.updatedAt)
    counts_of_followed_articles = query_for_user.count()
    lower,higher = offset, offset+limit
    if counts_of_followed_articles <= lower:
        return [model_to_dict(row) for row in query_for_user.paginate(1,counts_of_followed_articles)]
    elif lower < counts_of_followed_articles < higher:
        return [model_to_dict(row) for row in query_for_user.paginate(lower+1,counts_of_followed_articles)]
    else:
        return [model_to_dict(row) for row in query_for_user.paginate(lower+1,higher)]

async def get_all_articles(limit,offset,tag,author,favorite):
    #query building sequence starts
    #Not sure if this is the right assumption but we're going to assume that all inputs can arrive at the same time
    # print(tag,author,favorite)
    subquery = None
    if tag and not author and not favorite:
        t= Tags.get_or_none(tag=tag)
        if t:
            subquery = TagToArticle.select(TagToArticle.articleid).where(TagToArticle.tagid==t)
        else:
            raise SanicException("Tag not found",404)
            return []
    elif not tag and author and not favorite:
        user_id = User.get_or_none(username=author)
        if user_id:
            subquery = Article.select(Article.id).where(Article.author == user_id)
        else:
            raise SanicException("Author not found",404)
            return []
    elif not tag and not author and favorite:
        user_id = User.get_or_none(username=favorite)
        if user_id:
            subquery = FavoritedArticlesByUser.select(FavoritedArticlesByUser.articleid).where(FavoritedArticlesByUser.userid == user_id)
        else:
            raise SanicException("No user like this exists",404)
            return []
    
    lower = offset
    higher = offset+limit
    res = []
    
    if subquery is not None:
        print("1")
        if subquery.count() == 0:
            return []
        else:
            print("2")
            query= Article.select().where(Article.id.in_(subquery))
    else:
        print("3")
        query = Article.select()
    # print(query)
    # print(subquery)
    # print(query)
    counts_for_articles = query.count()
    if counts_for_articles < lower:
        res = [model_to_dict for row in query.paginate(1,counts_for_articles)]
    elif lower <= counts_for_articles <= higher:
        res = [model_to_dict(row) for row in query.paginate(lower+1,counts_for_articles)]
    else:
        res = [model_to_dict(row) for row in query.paginate(lower+1,higher)]
    return res

async def get_articles_from_helper(
        single:bool=True,
        slug:str="",
        user:dict=None,
        limit:int=20,
        offset:int=0,
        author:str="",
        tag:str="",
        favorite:str=""
)->dict:
    # print(author,tag,favorite)
    if single and slug and user:
        # We need to get a single article and ensure that the favorite matching is sure
        article = Article.get_or_none(Article.slug==slug)
        if not article:
            raise SanicException("Not found",404)
        article = model_to_dict(Article.get(Article.slug==slug))
        article["author"]["following"] == await following(user["id"],article["author"]["id"])
        article["favorited"] = await favorited(user["id"],article["id"])             
        article["favoritesCount"] = await favorite_count(article["id"])
        article["tagList"] = await get_tags(article["id"])
        return article
    if not single:
        #We will ignore the slug here and ideally we should not get a slug in this request
        results = None
        if user:
            results = await get_follower_articles(user["id"],limit,offset)
        else:
            results = await get_all_articles(limit,offset,tag,author,favorite)
        for r in results:
            #The results here only give us a few things, i.e the article and the author.
            #There's a few more things that need to be added, i.e following the user (if there is a user)
            #Checking the favorited counts, and also checking whether you've favorited that article.
            r["tagList"] = await get_tags(r["id"])
            r["favorited"] =await favorited(user["id"],r["id"]) if user else False
            r["author"]["following"] =await following(user["id"],r["author"]["id"]) if user else False
            r["favoritesCount"] = await favorite_count(r["id"])
        return results

async def get_single_article(user,article_id=None,article_slug=None):
    if article_id or article_slug:
        try:
            article_query = Article.select().where(Article.id == article_id) if article_id else Article.select().where(Article.slug == article_slug)
            if article_query.count() == 0:
                raise SanicException("The slug or ID does not exist",404)
        except IntegrityError as ie:
            print(ie)
            raise SanicException("There has been an an internal server error",500)
        except SanicException as se:
            print(se)
            if se.status_code == 404:
                raise se
        except Exception as e:
            print(e)
            raise SanicException("Non database issue",500)
        
        article_obj = [model_to_dict(row) for row in article_query][0]
        if article_obj:
            article_obj["favorited"] =await favorited(user["id"],article_obj["id"]) if user else False
            article_obj["author"]["following"]=await following(user["id"],article_obj["author"]["id"]) if user else False
            article_obj["favoritesCount"] = await favorite_count(article_obj["id"])
            article_obj["tagList"] = await get_tags(article_obj["id"])
            return article_obj
