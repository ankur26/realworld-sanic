from sanic import Blueprint,json
from models.Tags import Tags
tag_bp = Blueprint("tags",url_prefix="/tags")

@tag_bp.get("/",name="get_tags")
async def get_tags(request):
    return json({"tags":[row["tag"] for row in Tags.select().dicts()]})