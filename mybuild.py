from myflows.thisflow import flow as tflow1
# from myflows.thisflow import flow as tflow2


# tflow.storage.build()

from prefect.environments.storage import Docker
import copy
tflow2 = copy.deepcopy(tflow1)
tflow2.name = "222"

d = Docker()
d.add_flow(tflow1)
d.add_flow(tflow2)

d.build()