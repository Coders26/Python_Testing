from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def load_main(self):
        self.client.get("/")

    @task
    def load_showSummary(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task
    def load_book(self):
        self.client.get("/book/Spring Festival/Simply Lift")

    @task
    def load_purchasePlaces(self):
        self.client.post("/purchasePlaces", {"competition": "Spring Festival", "club": "Simply Lift", "places": "1"})