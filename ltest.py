
from prefect import task, Flow
from prefect.environments.storage import Docker

def func():
    print(1)

@task
def logging_this(tag="test_log"):
    from prefect import context
    logger = context.get("logger")
    logger.info(func)

with Flow('ltest-docker') as f:
    logging_this()

# f.storage = Docker(registry_url="joshmeek18", image_name="flows")
f.storage = Docker()

f.register(project_name="Demo")
# print(f.register(no_url=True))