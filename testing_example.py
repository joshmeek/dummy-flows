from prefect import Task, Flow
from prefect.core.edge import Edge

class Extract(Task):
    def run(self):
        return 10

class Transform(Task):
    def run(self, x):
        return x + 10

class Load(Task):
    def run(self, x):
        print(x)

flow = Flow("testing-example")

e = Extract()
t = Transform()
l = Load()

flow.add_edge(upstream_task=e, downstream_task=t, key="x")
flow.add_edge(upstream_task=t, downstream_task=l, key="x")

state = flow.run()

# Testing state

assert state.is_successful
assert state.result[e].is_successful
assert state.result[t].is_successful
assert state.result[l].is_successful

# Testing results

assert state.result[e].result == 10
assert state.result[t].result == 20
assert state.result[l].result == None

# Flow composition

assert e in flow.tasks
assert t in flow.tasks
assert l in flow.tasks
assert len(flow.tasks) == 3

assert flow.root_tasks() == set([e])
assert flow.terminal_tasks() == set([l])

assert len(flow.edges) == 2
assert Edge(upstream_task=e, downstream_task=t, key="x") in flow.edges
assert Edge(upstream_task=t, downstream_task=l, key="x") in flow.edges