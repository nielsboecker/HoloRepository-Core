import random
from locust import HttpLocust, TaskSet, task

HEADER = {"Content-Type": "application/json"}


class UserBehavior(TaskSet):
    @task
    def getSingleAuthor(self):
        self.client.get("/api/v1/authors/a100")

    @task
    def getMultipleAuthors(self):
        self.client.get("/api/v1/authors?aids=a1000,a100,a101,a102")

    @task
    def getSinglePatient(self):
        self.client.get("/api/v1/patients/p100")

    @task
    def getMultiplePatients(self):
        self.client.get("/api/v1/patients?pids=p1000,p100,p101,p102,p103")

    @task
    def getSingleHologram(self):
        self.client.get("/api/v1/holograms/h100")

    @task
    def getMultipleHolograms(self):
        url = random.choice(
            [
                "/api/v1/holograms?hids=h100,h101,h102,h103,h104",
                "/api/v1/holograms?pids=p101,p102,p103,p104",
                "/api/v1/holograms?pids=p100&creationmode=UPLOAD_EXISTING_MODEL",
            ]
        )
        self.client.get(url)

    @task
    def putAuthor(self):
        json_body = """{
            "aid": "a1000",
            "name": {
                "full": "Roy Campbell",
                "title": "Mr.",
                "given": "Roy",
                "family": "Campbell"
            }
        }
        """
        self.client.put("/api/v1/authors/a1000", data=json_body, headers=HEADER)

    @task
    def putPatient(self):
        json_body = """{
            "pid": "p1000",
            "name": {
                "title": "Mr.",
                "given": "Timothy",
                "family": "Jones",
                "full": "Timothy Jones"
            },
            "gender": "male",
            "birthDate": "1990-10-10"
        }
        """
        self.client.put("/api/v1/patients/p1000", data=json_body, headers=HEADER)


class AccessorLocust(HttpLocust):
    task_set = UserBehavior
    min_wait = 2000
    max_wait = 5000
