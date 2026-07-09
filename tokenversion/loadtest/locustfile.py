import random

from locust import HttpUser, between, task

POST_IDS = list(range(1, 21))


class PostsUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        resp = self.client.post(
            "/login", json={"username": "student", "password": "student123"}
        )
        token = resp.json()["access_token"]
        self.client.headers.update({"Authorization": f"Bearer {token}"})

    @task(3)
    def get_post(self):
        post_id = random.choice(POST_IDS)
        self.client.get(f"/posts/{post_id}", name="/posts/[id]")

    @task(1)
    def create_post(self):
        self.client.post(
            "/posts",
            json={"title": "Load Test Post", "body": "Some body text", "userId": 1},
        )
