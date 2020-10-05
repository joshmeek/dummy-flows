from prefect import Flow, Parameter, unmapped, task
from prefect.tasks.shell import ShellTask
from prefect.environments.storage import Docker
from prefect.utilities.tasks import defaults_from_attrs
from prefect.tasks.secrets.base import Secret


class TFTask(ShellTask):
    def __init__(self, tf_env=None, stack=None, version=None, tf_args=None, **kwargs):
        self.tf_env = tf_env
        self.stack = stack
        self.version = version
        self.tf_args = tf_args
        helper_script = "cd terraform"
        return_all = True
        env = {"TF_INPUT": "false", "TF_IN_AUTOMATION": "true"}
        super().__init__(
            helper_script=helper_script, return_all=return_all, env=env, **kwargs
        )

    @defaults_from_attrs("tf_env", "stack", "version", "tf_args")
    def run(self, component, tf_env=None, stack=None, version=None, tf_args=None):
        command = f"bash tf.sh -e {tf_env} -c k8s/{component} -s {stack} -v {version} -- {tf_args}"
        print(command)
        return super(TFTask, self).run(command=command)


storage = Docker(
    dockerfile="Dockerfile",
    prefect_version="master",
    registry_url="reg",
    image_name="foo",
    image_tag="bar",
)

components = ["apollo", "auth", "batch-writer", "graphql", "hasura", "stripe", "towel"]
tf = TFTask()

with Flow(name="deploy-k8s", storage=storage) as flow:
    tf_env = Parameter("tf_env")
    version = Parameter("version")
    stack = Parameter("stack")
    plan = tf.map(
        components,
        tf_env=unmapped(tf_env),
        version=unmapped(version),
        stack=unmapped(stack),
        tf_args=unmapped("plan"),
    )

flow.register(project_name="Demo", build=False)