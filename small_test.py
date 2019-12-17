from prefect import Client
import prefect
from prefect import task, Flow

@task(name="Welcome", slug="welcome-task")
def welcome_logger():
    a=1+1
    print(a)

f = Flow("Welcome Flow1", tasks=[welcome_logger])

f.deploy("Demo")