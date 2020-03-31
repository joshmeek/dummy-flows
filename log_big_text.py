from prefect import task, Flow
from urllib.request import urlopen


@task
def get_and_log():
    from prefect import context
    logger = context.get("logger")
    data = urlopen(
        "https://gist.githubusercontent.com/StevenClontz/4445774/raw/1722a289b665d940495645a5eaaad4da8e3ad4c7/mobydick.txt"
    )

    my_big_log = data.read().decode("utf-8")
    my_small_log = my_big_log[:len(my_big_log)//2]

    for i in range(10):
        logger.info(my_small_log)
        import time
        time.sleep(6)

with Flow("Log Big Text UTF") as flow:
    get_and_log()

# flow.run()
flow.register(project_name="Demo")

