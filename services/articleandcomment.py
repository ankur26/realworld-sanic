from sanic import Blueprint,SanicException,json
from models.Article import Article
from models.Tags import Tags
from models.TagToArticle import TagToArticle
from models.FavoritedArticlesByUser import FavoritedArticlesByUser
from models.Comments import Comments
from helpers.serializer_helper import serialize_output,serialize_multiple,get_query_items,merge_objects
from middleware.requestcontentvalidator import validate_data
from middleware.requestvalidator import validate_request_body_exists,validate_request_object_exists_in_body,validate_authorization_token_exists,authorize
from schemas.ArticleAndCommentValidationAndSerializationSchema import ArticleCreateType,ArticleOutputType,ArticleUpdateType,CommentOutputType,CommentCreateType
from playhouse.shortcuts import dict_to_model, model_to_dict
from helpers.article_and_comment_fetch_helper import get_articles_from_helper,get_single_article,get_comments,get_single_comment
from peewee import IntegrityError

article_bp = Blueprint("article",url_prefix="/articles")

@article_bp.post("/",name="create_article")
@validate_request_body_exists
@validate_request_object_exists_in_body("article")
@validate_authorization_token_exists()
@authorize()
@validate_data(ArticleCreateType,"article")
async def create_article(request,validated_data:ArticleCreateType):
    current_user = request.ctx.user
    validated_data = validated_data.model_dump()
    validated_data["author"] = current_user["id"]
    article_cursor = dict_to_model(Article,validated_data,ignore_unknown=True)
    try:
        #We need to create and article first, the tags then can be associated with 
        #Whose ID can be then be passed for us to create tags.
        article_id = article_cursor.save()
        if article_id:
            # print(article_id,article_cursor.id)
            taglist = validated_data["tagList"]
            for t in taglist:
                tag_cursor = Tags.get_or_none(tag=t)
                if not tag_cursor:
                    #We will create a tag here and get it's ID
                    tag_cursor = Tags(tag=t).save()
                #We now have the article ID and the tag ID at this point, now just add this entry to the tagToarticletable
                tag_to_article_id = TagToArticle(articleid=article_id,tagid=tag_cursor).save()
                if not tag_to_article_id:
                    print("Some error happened")
                #We now have a tag list, we now have a article entry
            article_output = await get_single_article(user=current_user,article_id=article_id)   
            return json(await serialize_output(ArticleOutputType,article_output,"article"))
    except IntegrityError as e:
        print (e)
        raise SanicException("The data had an error while being created",500)
    except Exception as e:
        print(e)
        raise SanicException("There is some unexpected error",500)


@article_bp.get("/<slug:str>",name="get_single_article")
@validate_authorization_token_exists(allow_anonymous=True)
@authorize()
async def get_article(request,slug):
    user = request.ctx.user
    article = await get_single_article(user,article_slug=slug)
    return json(await serialize_output(ArticleOutputType,article,"article"))

@article_bp.get("/",name="get_articles")
@validate_authorization_token_exists(allow_anonymous=True)
@authorize()
async def get_articles(request):
    query_dict =await get_query_items(request.query_args)
    user = request.ctx.user
    results = await get_articles_from_helper(
        limit=query_dict.get('limit',20),
        offset=query_dict.get('offset',0),
        author=query_dict.get('author',None),
        tag=query_dict.get('tag',None),
        favorite=query_dict.get('favorited',None),
        user=user,
        single=False
        )
    results = await serialize_multiple(ArticleOutputType,results,"article",include_counts=True)
    
    return json(results)

@article_bp.get("/feed",name="get_feed")
@validate_authorization_token_exists()
@authorize()
async def get_feed(request):
    query_dict =await get_query_items(request.query_args)
    user = request.ctx.user
    results = await get_articles_from_helper(
        limit=query_dict.get('limit',20),
        offset=query_dict.get('offset',0),
        author=query_dict.get('author',None),
        tag=query_dict.get('tag',None),
        favorite=query_dict.get('favorited',None),
        user=user,
        single=False
        )
    results = await serialize_multiple(ArticleOutputType,results,"article",include_counts=True)
    return json(results)


@article_bp.post("/<slug:str>/favorite",name="toggle_favorite")
@article_bp.delete("/<slug:str>/favorite",name="untoggle_favorite")
@validate_authorization_token_exists()
@authorize()
async def toggle_favorite(request,slug):
    user = request.ctx.user
    article_id = Article.get_or_none(slug=slug)
    # print(user,article_id)
    if article_id and user:
        if request.method == "POST":
            id = FavoritedArticlesByUser.get_or_create(articleid = article_id,userid = user["id"])
            return json(await serialize_output(ArticleOutputType,await get_single_article(user=user,article_id=article_id),"article"))
        elif request.method == "DELETE":
            favorite = FavoritedArticlesByUser.get_or_none(articleid=article_id,userid=user["id"])
            FavoritedArticlesByUser.delete_by_id(favorite)
            return json(await serialize_output(ArticleOutputType,await get_single_article(user=user,article_id=article_id),"article"))
    else:
        raise SanicException("Slug not found not found",404)
    

@article_bp.put("/<slug:str>",name="update_article")
@validate_request_body_exists
@validate_request_object_exists_in_body("article")
@validate_authorization_token_exists()
@authorize()
@validate_data(ArticleUpdateType, "article",)
async def update_article(request,validated_data:ArticleUpdateType,slug):
    user = request.ctx.user
    article = Article.get(slug=slug)
    original = model_to_dict(article,exclude=["author"])
    if original["author"]["id"] != user["id"]:
        return json(
            {"errors":"You don't have permission to edit this article"},403
        )
    del original["author"] #Extra measure
    # print(dict(validated_data))
    article_cursor = dict_to_model(Article,await merge_objects(dict(validated_data),original),ignore_unknown=True)
    article_cursor.save()
    # print(updated_object)
    # The assumption with a tagList is that it will always be a fresh update
    # The reason is that an update is always done on top of the original list

    #Get the original tag list
    tags_for_article = TagToArticle.select(Tags).join(Tags,on=(Tags.id == TagToArticle.tagid)).where(TagToArticle.articleid ==article.id).dicts()
    original_tags = [row["tag"] for row in tags_for_article]
    article
    tags_to_be_added = [tag for tag in original_tags if tag in validated_data.tagList]
    tags_to_be_removed = [tag for tag in original_tags if tag not in validated_data.tagList]
    try:
        # Ensure that our tags are now updated
        for tag in tags_to_be_removed:
            tid = Tags.get_or_none(tag=tag)
            toaid = TagToArticle.get_or_none(articleid=original["id"],tagid=tid)
            if toaid:
                TagToArticle.delete_by_id(toaid)
        for tag in tags_to_be_added:
            tid = Tags.get_or_none(tag=tag)
            if not tid:
                tid = Tags(tag=tag).save()
            toaid = TagToArticle.get_or_none(articleid=original["id"],tagid=tid)
            if not toaid:
                toaid = TagToArticle(articleid=original["id"],tagid=tid)
                toaid.save()
            

        # Update the article now

        return json(await serialize_output(ArticleOutputType,await get_single_article(user,article_id=original["id"]),"article"))
    except IntegrityError as e:
        print(e)
        return SanicException("internal server error",500)
    

@article_bp.delete("/<slug:str>",name="delete_article")
@validate_authorization_token_exists()
@authorize()
async def delete_article(request,slug):
    user = request.ctx.user
    article = model_to_dict(Article.get_or_none(slug=slug)) if Article.get_or_none(slug=slug) else None
    if not article:
        raise SanicException("Not found",404)
    else:
        #We have the article id here we should now go ahead and delete in three tables
        #TagsToArticle
        #Comments
        #FavoritedArticles
        #Then the article itself
        #There are Cascade options but in the ORM but I have disabled those for simplicity
        if user["id"] != article["author"]["id"]:
            return SanicException("Forbidden",403)
        else:
            try:
                TagToArticle.delete().where(TagToArticle.articleid==article["id"]).execute()
                Comments.delete().where(Comments.articleid==article["id"]).execute()
                FavoritedArticlesByUser.delete().where(FavoritedArticlesByUser.articleid==article["id"]).execute()
                Article.delete().where(Article.slug == slug).execute()
                return json({"status":True})
            except Exception as e:
                print(e)
                raise SanicException("Something went wrong",500)



#These are the calls for comments 

@article_bp.get("/<slug:str>/comments",name="get_comments")
@validate_authorization_token_exists(allow_anonymous=True)
@authorize()
async def get_article(request,slug):
    user = request.ctx.user
    article = Article.get_or_none(slug=slug)
    if not article:
        return SanicException("Not found",404)
    else:
        return json(await serialize_multiple(CommentOutputType,await get_comments(user,article),"comment"))

@article_bp.post("/<slug:str>/comments",name="create_comment")
@validate_request_body_exists
@validate_request_object_exists_in_body("comment")
@validate_authorization_token_exists()
@authorize()
@validate_data(CommentCreateType,"comment")
async def create_comment(request, validated_data:CommentCreateType,slug):
    user = request.ctx.user
    article = Article.get_or_none(slug=slug)
    if article:
        comment = dict_to_model(Comments,{
            "body":validated_data.body,
            "userid":user["id"],
            "articleid":article
        },ignore_unknown=True)
        id = comment.save()
        return json(await serialize_output(CommentOutputType,await get_single_comment(user,id),"comment"))
    else:
        raise SanicException("Not found",404)

@article_bp.delete("<slug:str>/comments/<id:int>",name="delete_comment")
@validate_authorization_token_exists()
@authorize()
async def delete_article(request,slug,id):
    user = request.ctx.user
    article = Article.get_or_none(slug=slug)
    comment = Comments.get_or_none(id=id)
    if not article:
        raise SanicException("Not found",404)
    if not comment:
        raise SanicException("Not found",404)
    comment_object = model_to_dict(comment)
    if user["id"] != comment_object["userid"]["id"]:
        raise SanicException("Forbidden",403)
    try:
        comment.delete()
        return json({"status":"success"})
    except Exception as e:
        print(e)
        raise SanicException("Something went wrong during deleting the data",500)