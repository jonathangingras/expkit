import os


class MakefileConfig(object):
    def __init__(self,
                 python="python",
                 latex="pdflatex",
                 result_dir="__results__",
                 experiments_cfg="experiments.py",
                 results_cfg="results.py",
                 open_cmd="open",
                 target="$(RESULT_DIR)/document.pdf"):
        self.mk_variables = {key.upper(): val for key, val in filter(lambda key_val: id(key_val[1]) != id(self), locals().items())}

    def __str__(self):
        return "\n".join(["=".join([key, val]) for key, val in sorted(self.mk_variables.items())])

    def to_makefile(self):
        return str(self) + "\n" + \
            "".join(open(os.path.join(os.path.dirname(__file__),
                              "..", "..", "resources", "expkit_makefile")).readlines())


def export_makefile(**kwargs):
    with open("Makefile", "w") as f:
        f.write(MakefileConfig(**kwargs).to_makefile())
