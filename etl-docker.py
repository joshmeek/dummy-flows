from prefect import task
from prefect.environments.storage import Docker

@task
def extract():
    """Get a list of data"""
    return [1, 2, 3]


@task
def transform(data):
    """Multiply the input by 10"""
    return [i * 10 for i in data]


@task
def load(data):
    """Print the data to indicate it was received"""
    print("Here's your data: {}".format(data))


from prefect import Flow

with Flow("ETL-docker-38", storage=Docker(image_name="flows")) as flow:
    e = extract()
    t = transform(e)
    l = load(t)

# FlowRunner(flow).run()
# flow.register(project_name="Demo")

flow.register(project_name="Demo")