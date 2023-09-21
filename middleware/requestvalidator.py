from sanic import json
from functools import wraps
from helpers.jwt_token_helper import check_token_and_return_status


def validate_request_body_exists(func):
    @wraps(func)
    async def wrapper(request, *args,**kwargs):
        if not request.body:
            return json(
                {
                    "errors":{
                        "body":"Cannot be empty"
                    }
                },
                422
            )
        return await func(request,*args,**kwargs)
    return wrapper

def validate_request_object_exists_in_body(key):
    # def validate_request_user_exists_in_body():
    def decorator(func):
        @wraps(func)
        async def wrapper(request, *args, **kwargs):
            if not request.json.get(key,None):
                return json(
                    {
                        "errors":{
                            "body":f"{key} cannot be empty"
                        }
                    }
                    ,422
                )
            res = await func(request, *args, **kwargs)
            return res
        return wrapper
    return decorator
    


def validate_authorization_token_exists(allow_anonymous_context=False):
    def dec(func):
        @wraps(func)
        async def wrapper(request, *args,**kwargs):
            if allow_anonymous_context:
                res = await func(request,*args,**kwargs)
                return res
            
            auth_header = request.headers.get("Authorization",None)
            # print(auth_header)
            if not auth_header:
                return json({
                    "errors":{
                        "headers":"Missing Bearer token"
                    }
                },403)
            if not auth_header.startswith("Bearer ") and not auth_header.startswith("Token "):
                return json({
                    "errors":{
                        "header":"Authorization missing bearer or token prefix"
                    }
                },403)
            res = await func(request,*args,**kwargs)
            return res
        return wrapper
    return dec


def authorize(allow_anonymous_context=False):
    def decorator(func):
        @wraps(func)
        async def wrapper(request,*args,**kwargs):
            if allow_anonymous_context:
                request.ctx.user = None
                res = await func(request,*args,**kwargs)
                return res
            bearer_token = request.headers.get("Authorization").replace("Bearer ","").replace("Token ","")
            token_check_output = await check_token_and_return_status(bearer_token)
            if token_check_output["valid_token"]:
                user = token_check_output["token_user"]
                user["token"] = bearer_token
                request.ctx.user = user
                res = await func(request,*args,**kwargs)
                return res
            else:
                return json({
                    "error":token_check_output["error"]
                },token_check_output["return_status_code"])

        return wrapper
    return decorator

