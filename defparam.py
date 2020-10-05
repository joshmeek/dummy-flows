from prefect import task, Flow, Parameter
import prefect

logger = prefect.utilities.logging.get_logger()
@task
def print_plus_one(x):
    print(x + 1)
    logger.warning(x+1)

with Flow('default-param') as flow:
    x = Parameter('x', default = 2)
    print_plus_one(x=x)

flow.register(project_name="Demo")
