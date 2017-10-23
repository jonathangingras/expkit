def unwrapped(wrapper):
    return wrapper.__wrapped__()

def is_wrapper(obj):
    return callable(getattr(obj, "__is_wrapper__", None)) and (getattr(obj, "__wrapped__", None) is not None)
