import json
import os
from tempfile import TemporaryDirectory
from typing import Optional

from prefect import Flow, task
from prefect.engine.executors import Executor, DaskExecutor
from prefect.engine.results import LocalResult
from prefect.engine.serializers import JSONSerializer
from prefect.utilities.configuration import set_temporary_config
from prefect.utilities.debug import raise_on_exception

def test(e: Optional[Executor]):
    with TemporaryDirectory() as tmpdir:
        flow_result = LocalResult(tmpdir, serializer=JSONSerializer(),
                                  location="{task_name}.json")

        with Flow("write_result", result=flow_result) as f:
            _terminal = task(lambda: 42, checkpoint=True, name="magic")()

        with set_temporary_config({"flows.checkpointing": True}), \
             raise_on_exception():
            f.run(executor=e)

        files = os.listdir(tmpdir)
        assert files == ["magic.json"], files
        with open(os.path.join(tmpdir, files[0]), "rb") as file:
            val = json.load(file)
        assert val==42

if __name__ == "__main__":
    print("Local")
    test(None)
    print("DaskExecutor")
    test(DaskExecutor())

