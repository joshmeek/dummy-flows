from prefect import task, Flow, Parameter
from prefect.tasks.database import SQLiteQuery
from prefect.tasks.redis import RedisSet

@task
def a(x):
    print(x)

with Flow("meta_model_flow") as meta_model_flow:
    db = Parameter("db")
    # a(db)
    models = SQLiteQuery(db=db, query="SELECT identifier FROM models")()
    meta_model_flow.add_task(models)
    models.set_upstream(db, key=db)

meta_model_flow.run(db="test")