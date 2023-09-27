from sanic import json
from pydantic import ValidationError
from functools import wraps


def validate_data(validator_class, object_entry: str):
    # This is a generic attempt to try and validate as many requests we can in one class
    def decorator(f):
        @wraps(f)
        # Just a little bit of defensive programming
        async def wrapper(request, *args, **kwargs):
            if not request.json.get(object_entry, None):
                return json(
                    {
                        "errors": {
                            f"{object_entry}": "This key did not exist in the request body, make sure to add this"
                        }
                    },
                    422
                )
            else:
                try:
                    validated_data = validator_class(
                        **request.json.get(object_entry))
                    res = await f(request, validated_data, *args, **kwargs) 
                    return res
                except ValidationError as ve:
                    print(ve.errors())
                    return json(
                        {
                            "errors": ",".join([f"{v['type']}-{v['loc'][0]}-{v['msg']}" for v in ve.errors()])
                        }, 422
                    )
                except Exception as e:
                    print(e)
                    return json(
                        {"errors": f"{e}"}, 500)
        return wrapper

    return decorator
