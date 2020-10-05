import time

from kubernetes import client, config

from prefect import resource_manager, task, Flow, Parameter


@resource_manager(name="k8s_batch_client")
class K8sBatchClient:
    def __init__(self, job_names=[]):
        self.job_names = job_names

    def setup(self):
        config.load_kube_config()
        return client.BatchV1Api()

    def cleanup(self, api_instance):
        """Clean up all jobs created by this resource"""
        for job_name in self.job_names:
            api_response = api_instance.delete_namespaced_job(
                name=job_name,
                namespace="default",
                body=client.V1DeleteOptions(
                    propagation_policy="Foreground", grace_period_seconds=5
                ),
            )
            print(f"Job deleted. status={api_response.status}")


@task
def create_job_object(job_name):
    # Configureate Pod template container
    container = client.V1Container(
        name="pi",
        image="perl",
        command=["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"],
    )
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "pi"}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]),
    )
    # Create the specification of deployment
    spec = client.V1JobSpec(template=template, backoff_limit=4)
    # Instantiate the job object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=job_name),
        spec=spec,
    )

    return job


@task
def create_job(api_instance, job):
    api_response = api_instance.create_namespaced_job(body=job, namespace="default")
    print(f"Job created. status={api_response.status}")


@task
def update_job(api_instance, job, job_name):
    # Update container image
    job.spec.template.spec.containers[0].image = "perl"
    api_response = api_instance.patch_namespaced_job(
        name=job_name, namespace="default", body=job
    )
    print(f"Job updated. status={str(api_response.status)}")


@task
def get_job_status(api_instance, job_name):
    completed = False
    while not completed:
        api_response = api_instance.read_namespaced_job_status(
            name=job_name, namespace="default"
        )

        if api_response.status.active:
            print("Job still active. Sleeping for 5s...")
            time.sleep(5)
        else:
            completed = True
            print(f"{job_name} has completed!")


with Flow("k8s-job-crud") as flow:
    job_name1 = Parameter("job_name1")
    job1 = create_job_object(job_name1)

    job_name2 = Parameter("job_name2")
    job2 = create_job_object(job_name2)

    job_name3 = Parameter("job_name3")
    job3 = create_job_object(job_name3)

    with K8sBatchClient(job_names=[job_name1, job_name2, job_name3]) as batch_v1:
        create1 = create_job(batch_v1, job1)

        update1 = update_job(batch_v1, job1, job_name1)
        update1.set_upstream(create1)

        status1 = get_job_status(api_instance=batch_v1, job_name=job_name1)
        status1.set_upstream(update1)

        create2 = create_job(batch_v1, job2)

        update2 = update_job(batch_v1, job2, job_name2)
        update2.set_upstream(create2)

        status2 = get_job_status(api_instance=batch_v1, job_name=job_name2)
        status2.set_upstream(update2)

        create3 = create_job(batch_v1, job3)

        update3 = update_job(batch_v1, job3, job_name3)
        update3.set_upstream(create3)

        status3 = get_job_status(api_instance=batch_v1, job_name=job_name3)
        status3.set_upstream(update3)

# flow.run(parameters={"job_name": "pi"})
# flow.visualize()
flow.register(project_name="Demo")