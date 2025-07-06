from locust import HttpUser, task

class WebAppUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/")