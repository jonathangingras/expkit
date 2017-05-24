from .makefile import makefile_env_vars_from_config, makefile_path
from ..config import Config
from subprocess import Popen, PIPE
import sys, os


if __name__ == "__main__":
    try:
        config_object = Config.from_configfile()
    except:
        config_object = Config()

    if len(sys.argv) > 1:
        args = sys.argv[1:]
    else:
        args = []

    env = os.environ.copy()
    env.update(makefile_env_vars_from_config(config_object))

    Popen(["make", "-f", makefile_path(), *args], env=env)
