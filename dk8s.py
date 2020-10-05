from prefect import task, Flow
from prefect.environments import DaskKubernetesEnvironment
from prefect.environments.storage import S3


@task
def get_value():
    return "Example!"


@task
def output_value(value):
    print(value)


flow = Flow("dk8s-debug",)

# set task dependencies using imperative API
output_value.set_upstream(get_value, flow=flow)
output_value.bind(value=get_value, flow=flow)

flow.storage = S3(bucket="my-prefect-flows", secrets=["AWS_CREDENTIALS"])
flow.environment = DaskKubernetesEnvironment(
    metadata={"image": "joshmeek18/flows:all_extras9"}
)
flow.register(project_name="Demo")
