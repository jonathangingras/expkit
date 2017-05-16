import os
import glob
from ...utils.iterators import each


def find_intex_files(dirpath):
    return glob.glob(os.path.join(dirpath, "*.in.tex"))


def find_inpdf_files(dirpath):
    return glob.glob(os.path.join(dirpath, "*.in.pdf"))


def write_tex_table(filepath, dataframe, adjust_width=0, **kwargs):
    with open(filepath, "w") as f:
        f.write(r"""\begin{figure}
        \begin{adjustwidth}{""" + str(adjust_width) + r"""cm}{}
        \begin{center}
        """)

        f.write(dataframe.to_latex(**kwargs).replace(r"\_\_", " ").replace("_", " "))

        f.write(r"""
        \end{center}
        \end{adjustwidth}
        \end{figure}
        """)


def include_texinput(filepath, file=None):
    file.write(r"\input{" + filepath + "}\n")


def include_pdfinput(filepath, file=None, adjust_width=0):
    file.write(r"""\begin{figure}
        \begin{adjustwidth}{""" + str(adjust_width) + r"""cm}{}
        \begin{center}
        """)

    file.write(r"\makebox[\textwidth]{\includegraphics[width=\paperwidth]{{" + \
               filepath[:-4] + \
               "}.pdf}}\n")

    file.write(r"""
        \end{center}
        \end{adjustwidth}
        \end{figure}
        """)


def write_default_main_tex(filepath):
    header = r"""
\documentclass{report}
\usepackage{booktabs}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[frenchb]{babel}
\usepackage{hyperref}
\usepackage{amsmath, amssymb}
\usepackage{geometry}
\usepackage{caption,subcaption}
\usepackage{graphicx}
\usepackage{physics}
\usepackage{changepage}
\usepackage{multirow}

\begin{document}
    """

    footer = r"""
\end{document}
    """

    with open(filepath, "w") as f:
        f.write(header)
        each(find_intex_files(os.path.dirname(filepath)))(include_texinput, file=f)
        each(find_inpdf_files(os.path.dirname(filepath)))(include_pdfinput, file=f)
        f.write(footer)
