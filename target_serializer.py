from prefect import task, Flow
from prefect.engine.results import LocalResult
from prefect.engine.serializers import JSONSerializer

@task(target="test.json", result=LocalResult(serializer=JSONSerializer()))
def get_data():
    return {"asdf": "here"}

@task
def print_data(d):
    print(d)

with Flow("target_serializer") as f:
    d = get_data()
    print_data(d)

f.run()