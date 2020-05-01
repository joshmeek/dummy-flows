from prefect import task
from prefect.engine.signals import FAIL
from prefect.triggers import some_successful

@task
def extract():
    """Get a list of data"""
    return [1, 2, 3]


@task
def transform(data):
    """Multiply the input by 10"""
    raise FAIL("I am a failure")


@task(trigger=some_successful)
def load(data):
    """Print the data to indicate it was received"""
    print("Here's your data: {}".format(data))


from prefect import Flow

with Flow("trigger-test") as flow:
    e = extract()
    t = transform(e)
    l = load(t)

# FlowRunner(flow).run()
# flow.register(project_name="QA")
flow.run()