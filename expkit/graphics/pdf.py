from . import no_display_magic
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def save_to_pdf(filename, pyplot_code, *args, **kwargs):
    try:
        with PdfPages(filename) as pdf:
            pyplot_code(*args, **kwargs)
            pdf.savefig()
            plt.close()
    except Exception as exception:
        try:
            os.unlink(filename)
        except:
            pass
        raise exception
