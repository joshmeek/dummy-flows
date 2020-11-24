import prefect
from prefect import Flow, task
from prefect.engine.results import LocalResult
from prefect.engine.signals import LOOP

@task()
def log_output(result):
    logger = prefect.context.get('logger')
    logger.info(result)


@task(result=LocalResult(dir='./results', location='test-{task_loop_count}.prefect'))
def loop_test():
    loop_payload = prefect.context.get("task_loop_result", {})

    n = loop_payload.get("n", 1)
    print(n)

    if n > 5:
        return n

    raise LOOP(f'Iteration {n}', result=dict(n=n+1))


with Flow("Postgres -&gt; BigQuery") as flow:
    x = loop_test()
    log_output(x)

flow.run()