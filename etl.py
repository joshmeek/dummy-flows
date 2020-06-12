from prefect import task
import time

@task
def extract():
    """Get a list of data"""
    time.sleep(5)
    return [1, 2, 3]


@task
def transform(data):
    """Multiply the input by 10"""
    time.sleep(5)
    return [i * 10 for i in data]


@task
def load(data):
    """Print the data to indicate it was received"""
    time.sleep(5)
    print("Here's your data: {}".format(data))


from prefect import Flow

with Flow("ETL-2") as flow:
    e = extract()
    t = transform(e)
    l = load(t)

# flow.run()
flow.register()
# flow.register(project_name="Demo")
# flow.run_agent(show_flow_logs=True)