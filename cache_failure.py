from datetime import timedelta
import random

from prefect import task, Flow
from prefect.engine import FlowRunner
from prefect.engine.cache_validators import duration_only

@task(cache_for=timedelta(seconds=10), 
      cache_validator=duration_only)
def rand_inc(r, x):
    rand = random.randint(0, r)
    print("RAND", rand)
    return rand + x

with Flow("Cache") as f:
    a1 = rand_inc(10, 0)


# this fails:
runner = FlowRunner(f)
state1 = runner.run()

# this would pass:
f.run()