from prefect import Client
from prefect.utilities.graphql import with_args

c = Client()

name = "my_flow"
c.graphql({"query": {with_args("flow", {"where": {"name": {"_eq": name}}}): "id"}})

# c.graphql({"query": "'query' {'flow'('where': { 'name': { '_eq': 'ltest' } }) {'id'}}"})
