from prefect import task, Flow, flatten

# @task
# def A():
#     return [1, 2, 3]

# @task
# def B(x):
#     l = list(range(x))
#     l.append(None)
#     return l

# @task
# def C(y):
#     # if y:
#     return y + 100

# @task
# def v(vals):
#     print(vals)

# with Flow('flat map') as f:
#     a = A()
#     b = B.map(x=a)
#     c = C.map(y=flat(b))

#     v(c)

# state = f.run()

# print(state)
# print(state.result[a].result)
# print(state.result[b].result)
# print(state.result[c].result)


@task
def values():
    return [[None]]

@task
def add(v):
    # if v:
    return v + 100

@task
def print_vals(a, b):
    print("here")
    print(a)
    print(b)

with Flow('fm') as f:
    vals = values()
    # a = add.map(flat(vals))
    print_vals.map(a=flatten([1]), b=flatten([[1]]))

state = f.run()