from prefect import task
import time

@task
def extract():
    """Get a list of data"""
    time.sleep(10)
    return [1, 2, 3]


@task
def transform(data):
    """Multiply the input by 10"""
    time.sleep(10)
    return [i * 10 for i in data]


@task
def load(data):
    """Print the data to indicate it was received"""
    time.sleep(10)
    print("Here's your data: {}".format(data))


from prefect import Flow

with Flow("ETL") as flow:
    e = extract()
    t = transform(e)
    l = load(t)

from prefect.engine.executors import DaskExecutor
from prefect.environments import LocalEnvironment

flow.environment = LocalEnvironment(labels=["asdf3"])

# flow.run()
# flow.register()
flow.register(project_name="Demo")
# flow.run_agent(show_flow_logs=True)
