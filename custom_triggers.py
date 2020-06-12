from prefect import task, Flow
import prefect
from prefect.core import Edge
from prefect.triggers import any_failed, any_successful


def aggregation_failure_trigger(upstream_states: Dict["core.Edge", "state.State"]):
    """Custom trigger for aggregation step failure"""
    if upstream_states[
        Edge(upstream_task=aggregate_metrics, downstream_task=store_metrics)
    ].is_failed():
        datadog.api.Event.create(
            title="Metric Aggregation Failure",
            text=aggregate_metrics.result,
            tags=["flow:failure"],
        )
        raise TRIGGERFAIL("Unable to store metrics due to aggregation failure.")

    return True


@task
def a1():
    pass


@task
def b1():
    pass


@task
def c1():
    pass


@task
def d1():
    pass


@task
def e1():
    pass


@task
def a2():
    raise prefect.engine.signals.FAIL


@task(trigger=any_failed)
def b2():
    pass


@task
def c2():
    pass


@task
def d2():
    pass


@task
def e2():
    pass


@task(trigger=custom_trigger)
def f():
    pass


with Flow("custom_triggers") as flow:
    a1 = a1()
    b1 = b1()
    c1 = c1()
    d1 = d1()
    e1 = e1()

    b1.set_upstream(a1)
    d1.set_upstream(c1)
    e1.set_upstream(b1)
    e1.set_upstream(d1)

    a2 = a2()
    b2 = b2()
    c2 = c2()
    d2 = d2()
    e2 = e2()

    b2.set_upstream(a2)
    d2.set_upstream(c2)
    e2.set_upstream(b2)
    e2.set_upstream(d2)

    f.set_upstream(e1)
    f.set_upstream(e2)

flow.run()
