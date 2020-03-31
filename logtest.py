from prefect import task, Flow
import boto3


@task
def log_me():
    import logging
    logger = logging.getLogger('ltest')
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)

    logger.debug("DEBUG")
    logger.info("INFO")
    logger.critical("CRITICAL")


with Flow("extra-log-test") as f:
    log_me()

# f.run()
f.register("QA")
