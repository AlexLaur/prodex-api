from . import constants


def model_check(func):
    def wrapper(*args, **kwargs):
        model = None
        if kwargs:
            model = kwargs.get("model", None)
        if not model:
            if len(args) > 1:
                model = args[1]  # args[0] is the decorted function
        if not constants.TRANSLATION.get(model, None):
            raise ValueError(
                "'{model}' doesn't exists. Allowed models: {allowed_models}".format(
                    model=model,
                    allowed_models=",\n".join(
                        list(constants.TRANSLATION.keys())
                    ),
                )
            )
        return func(*args, **kwargs)

    return wrapper
