from prefect import task

@task
def extract():
    """Get a list of data"""
    return [1, 2, 3]


@task(tags=["testmetag"])
def transform(data):
    """Multiply the input by 10"""
    return [i * 10 for i in data]


@task
def load(data):
    """Print the data to indicate it was received"""
    print("Here's your data: {}".format(data))


from prefect import Flow

with Flow("tags") as flow:
    e = extract()
    t = transform(e)
    l = load(t)

# FlowRunner(flow).run()
flow.register(project_name="Demo")