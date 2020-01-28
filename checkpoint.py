from prefect import Flow, task
from prefect.engine.result_handlers import LocalResultHandler

@task
def result_here():
    return "result"

@task
def get_it(x):
    print(x)

with Flow("test-checkpoint", result_handler=LocalResultHandler()) as f:
    r = result_here()
    get_it(r)

f.run()
# print(f.result_handler)