from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    # def on_start(self):
    #     self.client.post("/login", {"username": "test_user", "password": ""})

    @task
    def users(self):
        self.client.get("/users")

    @task
    def subscriptions(self):
        self.client.get("/subscriptions")
