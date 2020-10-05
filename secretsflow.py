# from prefect import task, Flow
# # from prefect.client.secrets import Secret
# from prefect.tasks.secrets import Secret

# @task
# def access_secret(secret_value):
#     # Access your secret and now you can use it however you would like
#     print(secret_value)

# with Flow("secret-retrieval") as flow:
#     secret = Secret("MY_SECRET")
#     access_secret(secret)


# flow.run()

# print(Secret("TEST_SECRET").get())