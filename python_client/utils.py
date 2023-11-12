def command(auth=False):
    def decorator(func):
        func.is_command = True
        func.requires_auth = auth
        return func

    return decorator

TEXT_ENCODING = "utf-8"