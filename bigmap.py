from prefect import task, Flow

@task
def values():
    return [i for i in range(100)]

@task
def pvals(x):
    print(x)

with Flow('bigmap') as f:
    vals = values()
    pvals.map(vals)

f.register("Demo")

# f.run()