
from prefect import Flow
from prefect.environments.storage import Docker

flow = Flow("thisflow", storage=Docker())