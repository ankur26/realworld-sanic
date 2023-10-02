from bcrypt import checkpw, gensalt, hashpw
from peewee import PeeweeException
from playhouse.shortcuts import dict_to_model, model_to_dict
from sanic import BadRequest, Blueprint, Forbidden, SanicException, json
from sanic.log import logger

from ..helpers.jwt_token_helper import get_token
from ..helpers.serializer_helper import merge_objects, serialize_output
from ..middleware.request_content_validator import validate_data
from ..middleware.request_header_and_body_validator import (
    authorize,
    validate_authorization_token_exists,
    validate_request_body_exists,
    validate_request_object_exists_in_body,
)
from ..models.user import User
from ..schemas.user_schema import UserLogin, UserOutput, UserRegistration, UserUpdate

auth_bp = Blueprint("auth", url_prefix="/users")
user_bp = Blueprint("user", url_prefix="/user")


@auth_bp.post("/", name="register")
@validate_request_body_exists
@validate_request_object_exists_in_body("user")
@validate_data(UserRegistration, "user")
async def register(request, validated_data: UserRegistration):
    # check if a user already exists
    logger.info("Registering user")
    user = User.get_or_none(username=validated_data.username)
    if user:
        return SanicException("user already exists", 422)
    # Get a model dump so that we can hash the password
    user_data = validated_data.model_dump()
    user_data["password"] = hashpw(
        password=bytes(user_data["password"], encoding="utf-8"), salt=gensalt()
    )
    id = User.create(**user_data)
    if id:
        logger.info("Registered user")
        # We will create a user object and return it.
        # This will be done via a serializer defined in the schemas folder
        output_data = model_to_dict(User.get_by_id(id), exclude=["password"])
        status, output_data["token"] = await get_token(output_data)
        if status:
            logger.info("Returning user")
            return json(await serialize_output(UserOutput, output_data, "user"))
        else:
            raise SanicException(
                "Something went wrong, please check logs {}".format(
                    output_data["error"]
                ),
                500,
            )
    else:
        raise SanicException("There was an error while creating the user", 500)
    # return text("You are the register route")


@user_bp.get("/", name="get_user")
@validate_authorization_token_exists()
@authorize()
async def get_user(request):
    logger.info("get_user")
    if request.ctx.user:
        logger.info("returning user")
        return json(await serialize_output(UserOutput, request.ctx.user, "user"))
    else:
        raise SanicException("Something went wrong while serialzingt the user", 500)


@auth_bp.post("/login", name="login")
@validate_request_body_exists
@validate_request_object_exists_in_body("user")
@validate_data(UserLogin, "user")
async def login(request, validated_data: UserLogin):
    logger.info("login")
    user = User.get_or_none(email=validated_data.email)
    # logger.info(validated_data)
    logger.info(user)
    if user:
        user = model_to_dict(user)
        logger.info("User found")
        if checkpw(bytes(validated_data.password, encoding="utf-8"), user["password"]):
            output_data = user
            logger.info("Password validated")
            status, output_data["token"] = await get_token(output_data)
            if status:
                logger.info("User validated")
                return json(await serialize_output(UserOutput, output_data, "user"))
            else:
                raise SanicException(
                    "Something went wrong during token generation", 500
                )
        else:
            raise Forbidden("Password does not match")
    else:
        raise SanicException("username does not exist", 422)


@user_bp.put("/", name="update_user")
@validate_request_body_exists
@validate_request_object_exists_in_body("user")
@validate_authorization_token_exists()
@authorize()
@validate_data(UserUpdate, "user")
async def update_user(request, validated_data: UserUpdate):
    # Get the user id which was set inside the context by the authorization
    # And set it inside our validated model
    logger.info("update_user")

    updated_user = await merge_objects(dict(validated_data), request.ctx.user)
    # print(updated_user)
    if validated_data.password:
        # password needs to encrypted and then changed
        logger.info("hashing updated password")
        updated_user["password"] = hashpw(
            bytes(updated_user["password"], encoding="utf-8"), gensalt()
        )
    user_cursor = dict_to_model(User, updated_user, ignore_unknown=True)
    try:
        logger.info("updating_user")
        user_cursor.save()
        output_data = model_to_dict(user_cursor, exclude=["password"])
        status, output_data["token"] = await get_token(output_data)
        if status:
            logger.info("Returning token")
            return json(await serialize_output(UserOutput, output_data, "user"))
        else:
            raise SanicException(
                "Something went wrong {}".format(output_data["error"]), 500
            )
    except PeeweeException as pe:
        raise SanicException(f"{pe}", 422)
    except Exception as e:
        raise SanicException(f"{e}", 500)
