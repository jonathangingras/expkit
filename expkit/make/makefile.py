import pkg_resources
from ..config import Config


def makefile_path():
    return pkg_resources.resource_filename('expkit.resources', 'expkit_makefile.mk')


def makefile_vars_from_config(config):
    return filter(lambda key_val: not key_val[0].startswith(Config.USER_ADDED_PREFIX), config)


def makefile_env_vars_from_config(config):
    return {"EXPKIT_" + key.upper(): val for key, val in makefile_vars_from_config(config)}


def formatted_makefile_vars_from_config(config, joiner="\n"):
    return joiner.join(["=".join([key.upper(), '"' + val + '"' ]) for key, val in \
            sorted(makefile_vars_from_config(config))])


def export_makefile(config_object=None):
    if config_object is None:
        try:
            config_object = Config.from_configfile()
        except FileNotFoundError:
            config_object = Config()

    with open("Makefile", "w") as f:
        f.write(formatted_makefile_vars_from_config(config_object) + "\n" + \
                "".join(open(makefile_path(), "r").readlines()))
