import os, sys
import getpass
from subprocess import Popen
import uuid
from ..experiment import ExperimentSetup
from ..experiment import create_experiment_setups
from .program_command import ExpKitExperimentRunCommand


class SlurmExperimentSetup(ExperimentSetup):
    def dispatch_options(self):
        return self.fallback_access(self.configs, {})["dispatch"]


class SlurmJob(object):
    """
    Dispatch a program on a computer using the SLURM scheduler

    example result script:
    #!/bin/bash
    #SBATCH --account=def-someuser
    #SBATCH --time=0-00:05 # time (DD-HH:MM)
    #SBATCH --job-name=test
    #SBATCH --output=%x-%j.out
    #SBATCH --nodes=1
    #SBATCH --ntasks=1
    #SBATCH --cpus-per-task=8
    """

    def __init__(self,
                 program_command,
                 time_in_seconds=60,
                 account=getpass.getuser(),
                 job_name=None,
                 email=None,
                 output='%x-%j.out',
                 mem_per_node='4000M',
                 nodes=1,
                 tasks=1,
                 cpus_per_task=8,
                 gpus_per_node=0,
                 large_gpus=False,
                 modules=[],
                 previous_commands=[]):
        self.program_command = program_command
        self.account = account # raw username
        self.time = time_in_seconds # in seconds
        self.job_name = job_name.replace(' ', '-') if isinstance(job_name, str) else "default-job-name"
        self.email = email
        self.output = output
        self.mem_per_node = mem_per_node
        self.nodes = nodes
        self.tasks = tasks
        self.cpus_per_task = cpus_per_task
        self.gpus_per_node = gpus_per_node
        self.large_gpus = large_gpus
        self.modules = modules
        self.previous_commands = previous_commands

        self.parameters = {}
        self.header_commands = []


    def shebang(self):
        return "#!/bin/bash"


    def hashtag_command(self, keyword, argument):
        return "#SBATCH --{}={}".format(keyword, argument)


    @staticmethod
    def __seconds_to_day_hour_minutes(seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        return d, h, m


    def export_level(self):
        try:
            return int(os.environ["EXPKIT_SLURM_DISPATCH_LEVEL"])
        except KeyError:
            return 0


    def export_level_command(self):
        return "export EXPKIT_SLURM_DISPATCH_LEVEL={}".format(self.export_level() + 1)


    def register_default_parameters(self):
        self.parameters.update({
            'account': 'def-{}'.format(self.account),
            'time': "%d-%02d:%02d" % SlurmJob.__seconds_to_day_hour_minutes(self.time),
            'job-name': self.job_name,
            'output': self.output,
            'cpus-per-task': self.cpus_per_task,
            'mem': self.mem_per_node
        })


    def register_notification_email(self):
        if self.email:
            self.parameters.update({
                'mail-user': self.email,
                'mail-type': 'ALL'
            })


    def register_nodes_and_tasks(self):
        if self.nodes != 1 or self.tasks != 1:
            self.parameters.update({
                'nodes': self.nodes,
                'ntasks': self.tasks,
            })


    def register_gpus(self):
        if self.gpus_per_node > 0:
            self.parameters.update({
                'nodes': self.nodes,
                'ntasks': self.tasks,
                'gres': 'gpu{}:{}'.format(":lgpu" if self.large_gpus else "", self.gpus_per_node)
            })
            if self.large_gpus:
                self.header_commands += ["hostname"]
            self.header_commands += ["nvidia-smi"]


    def header(self, **kwargs):
        self.register_default_parameters()
        self.register_notification_email()
        self.register_nodes_and_tasks()
        self.register_gpus()

        return "\n".join((self.shebang(),
                          "\n".join(map(lambda kv: self.hashtag_command(kv[0], kv[1]), self.parameters.items())),
                          "\n".join(self.header_commands),
                          self.export_level_command()))


    def load_modules(self):
        return "\n".join(map(lambda module: "module load {}".format(module), self.modules))


    def script_content(self):
        return "\n".join((self.header(),
                          "",
                          self.load_modules(),
                          "",
                          *self.previous_commands,
                          self.program_command.format()))


    def launch(self, slurm_dir):
        if not os.path.exists(slurm_dir):
            os.mkdir(slurm_dir)
        launch_script = os.path.join(slurm_dir, str(uuid.uuid4()) + ".slurm.sh")

        with open(launch_script, "w") as f:
            f.write(self.script_content())

        Popen(["sbatch", launch_script])


def dispatch_experiments(data, learners, output_dir='__experiments__', result_dir='__results__', rejected_combinations=(),
                         common_job_options={}, slurm_dir='__slurm__'):
    experiments = create_experiment_setups(data, learners, rejected_combinations, setup_class=SlurmExperimentSetup)

    def launch_job(experiment):
        experiment.save(output_dir)
        SlurmJob(
            ExpKitExperimentRunCommand(experiment, output_dir, result_dir),
            **common_job_options,           # for all jobs
            **experiment.dispatch_options() # for this particular experiment object
        ).launch(slurm_dir)

    tuple(map(launch_job, experiments))
