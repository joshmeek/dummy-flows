from prefect import Flow, task
from prefect.runtimes import FlowCLI


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



def main():
    with Flow("Runtime") as flow:
        e = extract()
        t = transform(e)
        l = load(t)

        runtime = FlowCLI(flow=flow)
        runtime.run()

if __name__ == '__main__':
    main()
