from django.test import Client
from django.urls import reverse
from rest_framework.test import APITestCase


class CommonAPITestCase(APITestCase):
    def setUp(self):
        register_data = {
            "email": "a@mail.ru",
            "password": "310QWERTy"
        }

        self.register_response = self.client.post(reverse("register"), data=register_data)
        token = self.client.post(reverse("token_obtain_pair"), data=register_data).json()["access"]
        self.client = Client(headers={"Authorization": f"Bearer {token}"})
