
from prefect.client import Client
# from prefect.client.flow import Flow

c = Client()
flow = c.flow(name="case-based-flow")
print(flow.name)
print(flow.id)
print(flow.version)
print(flow)
# print(flow.archived)
# print(flow.core_version)
# print(flow.bleh)
# print(flow.query("tasks { id }"))
# flow.run()