
from prefect import task, Flow

@task
def get_token():
    from prefect import context, config
    logger = context.get("logger")
    logger.info(config.cloud.agent.auth_token)

with Flow("env") as f:
    get_token()

f.register("Demo")