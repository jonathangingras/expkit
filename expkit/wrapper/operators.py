def unwrapped(wrapper, *args, **kwargs):
    return wrapper.__wrapped__(*args, **kwargs)

def is_wrapper(obj):
    return callable(getattr(obj, "__is_wrapper__", None)) and getattr(obj, "__wrapped__", None)
