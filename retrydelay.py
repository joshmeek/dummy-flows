from prefect import task, Flow
from datetime import timedelta
import time

@task(retry_delay=timedelta(seconds=1), log_stdout=True, max_retries=2)
def fail_me():
    print("I am starting")
    time.sleep(600)
    print("I am done sleeping")

f = Flow("retry-test", tasks=[fail_me])

f.register(project_name="Demo")