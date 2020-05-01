
from prefect import task, Flow

# for each document:
#     for each sink:
#         sink.push(doc)

@task
def documents():
    return [1, 2, 3]

@task
def sinks():
    return [lambda x: print(x * 1), lambda x: print(x * 2), lambda x: print(x * 3)]

@task
def make_push(d, sink):
    return [(sink, d) for sink in sink]

@task
def push(d, sink):
    sink(d)

with Flow("mlm") as f:
    documents = documents()
    sinks = sinks()
    push.map(documents, sinks)
    # sink.map(document)

f.run()