
from prefect import task, Flow
from prefect.environments.storage import GitHub

@task
def t():
    raise Exception("NONONONO")

f = Flow("filetest", tasks=[t])

# You would still configure storage object on flow
# Maybe we should update storage.add_flow to take a filepath as well as flow object
f.storage = GitHub(repo="joshmeek/flow_storage_test")

# f.serialize(build=True)

# we might want a way to register a file from the command line
# prefect register -f file.py
#   Load flow
#   Register it
# would avoid having to run script directly

# idea: secondary storage where you say "flow is here"
# no need in this case to do the file magic

# possible idea for extra commands, check a flag in env
# which would be set during run and they wouldn't run again

# things that could be paramaterized:
# name of file, where it's currently stored,
# where we want to move it to

# if user says where file is we use that,
# otherwise we try to infer it

# keep git push independent of registration
# finish github storage (no push on build)
# add default secret for github storage
# add register CLI command (works with all storage)
# gate register, run, serialize, etc. with a flag that can be set on `execute cloud-flow`

# one thing to open questions on, this current implementation is single path/flow per storage