from prefect import task, Flow
from prefect.environments.storage import Docker


@task
def test():
    import prefect

    logger = prefect.context.get("logger")
    logger.info(prefect.config.MY_VAR)
    return prefect.config.MY_VAR


with Flow(
    "config-test",
    storage=Docker(
        registry_url="joshmeek18",
        image_name="flows",
        files={
            "/Users/josh/Desktop/code/Dummy-Flows/user_config.toml": "/root/.prefect/user_config.toml"
        },
        env_vars={"PREFECT__USER_CONFIG_PATH": "/root/.prefect/user_config.toml"},
    ),
) as flow:
    test()

flow.deploy(project_name="Demo")
