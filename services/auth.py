from sanic import Blueprint, json, SanicException
from middleware.requestcontentvalidator import validate_data
from middleware.requestvalidator import validate_request_body_exists, validate_request_object_exists_in_body, validate_authorization_token_exists, authorize
from helpers.serializer_helper import serialize_output, merge_objects
from schemas.UserValidationAndSerializationSchemas import UserRegistration, UserOutput, UserLogin, UserUpdate
from models.User import User
from playhouse.shortcuts import model_to_dict, dict_to_model
from bcrypt import hashpw, checkpw, gensalt
from helpers.jwt_token_helper import get_token
from peewee import PeeweeException


auth_bp = Blueprint("auth", url_prefix="/users")


@auth_bp.post("/", name="register")
@validate_request_body_exists
@validate_request_object_exists_in_body("user")
@validate_data(UserRegistration, "user")
async def register(request, validated_data: UserRegistration):
    # check if a user already exists
    user = User.get_or_none(username=validated_data.username)
    if user:
        return json({"error": "user already exists"}, 422)
    # Get a model dump so that we can hash the password
    user_data = validated_data.model_dump()
    user_data["password"] = hashpw(password=bytes(
        user_data["password"], encoding='utf-8'), salt=gensalt())
    id = User.create(**user_data)
    if id:
        # We will create a user object and return it.
        # This will be done via a serializer defined in the schemas folder
        output_data = model_to_dict(User.get_by_id(id), exclude=["password"])
        status, output_data["token"] = await get_token(output_data)
        if status:
            return json(await serialize_output(UserOutput, output_data, "user"))
        else:
            return json({"error": "Something went wrong, please check logs"}, 500)
    else:
        return json({"error": "Something went wrong"}, 500)
    # return text("You are the register route")


@auth_bp.get("/", name="get_user")
@validate_authorization_token_exists()
@authorize()
async def get_user(request):
    return json(await serialize_output(UserOutput, request.ctx.user, "user")) if request.ctx.user else SanicException("Something is wrong",500)


@auth_bp.post("/login", name="login")
@validate_request_body_exists
@validate_request_object_exists_in_body("user")
@validate_data(UserLogin, "user")
async def login(request, validated_data: UserLogin):
    user = User.get_or_none(email=validated_data.email)
    if user:
        if checkpw(bytes(validated_data.password, encoding='utf-8'), user.password):
            output_data = model_to_dict(user, exclude=["password"])
            status, output_data["token"] = await get_token(output_data)
            if status:
                return json(await serialize_output(UserOutput, output_data, "user"))
            else:
                return json({"error": "Something went wrong during token generation"}, 500)
        else:
            return json({
                "errors": "Password does not match"
            },403)
    else:
        return json({
            "error": "username does not exist"
        }, 422)


@auth_bp.put("/", name="update_user")
@validate_request_body_exists
@validate_request_object_exists_in_body("user")
@validate_authorization_token_exists()
@authorize()
@validate_data(UserUpdate, "user")
async def update_user(request, validated_data: UserUpdate):
    # Get the user id which was set inside the context by the authorization
    # And set it inside our validated model
    updated_user = await merge_objects(request.ctx.user, dict(validated_data))
    if "password" in updated_user:
        # password needs to encrypted and then changed
        updated_user["password"] = hashpw(
            bytes(updated_user["password"], encoding="utf-8"), gensalt())
    user_cursor = dict_to_model(User, updated_user, ignore_unknown=True)
    try:
        user_cursor.save()
        output_data = model_to_dict(user_cursor, exclude=["password"])
        status, output_data["token"] = await get_token(output_data)
        if status:
            return json(await serialize_output(UserOutput, output_data, "user"))
        else:
            return json({"error": "Something went wrong"}, 500)
    except PeeweeException as pe:
        return json({"errors": pe}, 422)
    except Exception as e:
        return json({"errors": e}, 500)
