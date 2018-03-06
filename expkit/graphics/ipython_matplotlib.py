from IPython import get_ipython
from .pdf import save_to_pdf


def magic_available():
    return get_ipython() != None


def show(pyplot_code, magic_arg="inline", fallback_filename=None, save_anyways=False, *args, **kwargs):
    def save_pdf():
        if fallback_filename:
            save_to_pdf(fallback_filename, pyplot_code, *args, **kwargs)

    if magic_available():
        get_ipython().magic("matplotlib {}".format(magic_arg))
        pyplot_code(*args, **kwargs)
        if save_anyways:
            save_pdf()
            return
    else:
        save_pdf()
