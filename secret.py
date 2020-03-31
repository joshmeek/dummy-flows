import os
os.environ["PREFECT__CONTEXT__SECRETS__TEST2"] ="111"

from prefect.tasks.secrets import Secret

Secret("TEST2").run()