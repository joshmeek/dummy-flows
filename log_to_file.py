import logging

import prefect
from prefect import task, Flow

@task
def log_to_file():
    logger = prefect.context.get("logger")
    file_handler = logging.FileHandler('my.log')
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    logger.info("I am log.")

f = Flow("log-file", tasks=[log_to_file])
f.run()