from prefect import task, Flow
from urllib.request import urlopen


@task
def get_and_log():
    from prefect import context
    logger = context.get("logger")
    data = urlopen(
        "https://gist.githubusercontent.com/StevenClontz/4445774/raw/1722a289b665d940495645a5eaaad4da8e3ad4c7/mobydick.txt"
    )

    logger.info(data.read())

with Flow("Log Big Text") as flow:
    get_and_log()

# flow.run()
flow.register(project_name="QA")

