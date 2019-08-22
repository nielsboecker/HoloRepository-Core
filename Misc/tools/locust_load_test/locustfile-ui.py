from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
    @task
    def getPatients(self):
        self.client.get("/api/v1/patients")

    @task
    def getMultiplePatients(self):
        self.client.get("/api/v1/patients?pids=p100,p102")

    @task
    def getSpecificPatient(self):
        self.client.get("/api/v1/patients/p100")

    @task
    def getPractitioner(self):
        self.client.get("/api/v1/practitioners/a100")

    @task
    def getImagingStudies(self):
        self.client.get("/api/v1/imagingStudies")

    @task
    def getImagingStudiesOfPatients(self):
        self.client.get("/api/v1/imagingStudies?pids=p100,p102")

    @task
    def getSpecificImagingStudies(self):
        self.client.get("/api/v1/imagingStudies/i100")

    @task
    def getMultipleHolograms(self):
        self.client.get("/api/v1/holograms?pids=p100,p102")


class AccessorLocust(HttpLocust):
    task_set = UserBehavior
    min_wait = 2000
    max_wait = 5000
