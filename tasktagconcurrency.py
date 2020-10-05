from prefect import task, Flow
from prefect.environments.storage import Docker
from datetime import timedelta
import time

@task(tags=["test"])
def fail_me():
    print("I am starting")
    time.sleep(600)
    print("I am done sleeping")

f = Flow("Tag1-Flow", tasks=[fail_me], storage=Docker(prefect_version="q-schedule"))

f.register(project_name="Demo")