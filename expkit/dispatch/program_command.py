import os, sys


def super_init(pyobject, *args, **kwargs):
    super(pyobject.__class__, pyobject).__init__(*args, **kwargs)


class ProgramCommand(object):
    def format(self):
        return ""


class PythonProgramCommand(ProgramCommand):
    def __init__(self, script_path):
        self.path = os.path.realpath(script_path)


    def format(self):
        return "{} {}".format(sys.executable, self.path)


class ExpKitExperimentRunCommand(ProgramCommand):
    def __init__(self, experiment, output_dir, result_dir, interpreter=sys.executable):
        self.interpreter = interpreter
        self.experiment = experiment
        self.output_dir = output_dir
        self.result_dir = result_dir


    def format(self):
        return "{} -m expkit.dispatch {} {}".format(self.interpreter,
                                                    os.path.realpath(self.experiment.output_filepath(self.output_dir)),
                                                    os.path.realpath(self.result_dir))
