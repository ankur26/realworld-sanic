def check_object(type, keys, multiple=False, response=None):
    if not response:
        return False
    if multiple:
        if f"{type}s" not in response:
            return False
        if f"{type}sCount" not in response:
            return False
        for entry in response:
            if not check_object(type, keys, response=entry):
                return False
    else:
        if type not in response:
            return False
        for key in keys:
            if key not in response[type]:
                return False
    return True
