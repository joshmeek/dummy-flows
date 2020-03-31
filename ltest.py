
from prefect import task, Flow
from prefect.environments.storage import Docker

def func():
    print(1)

@task
def logging_this():
    from prefect import context
    logger = context.get("logger")
    logger.info(func)

with Flow('My first flow!') as f:
    logging_this()

f.register()
# f.register("Demo")