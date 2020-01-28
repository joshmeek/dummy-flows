
from prefect import task, Flow

@task
def do_something():
    from prefect import context
    logger = context.get("logger")
    logger.info("I AM HERE AGAIN")
    return "YES!"

with Flow("demo-flow") as f:
    f.chain(do_something(), do_something(), do_something(), do_something())
    # do_something()
    # do_something()

# f.run()
# f.visualize()
f.register(project_name="Demo")