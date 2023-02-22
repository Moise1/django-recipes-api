from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            "email": "test@example.com",
            "password": "user123",
            "name": "User Tester",
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objets.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_use_with_email_exists_error(self):
        payload = {
            "email": "test@example.com",
            "password": "user123",
            "name": "User Tester",
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        res.assertEqaul(res.status_code, status.HTTP_409_CONFLICT)

    def test_password_too_short_error(self):
        payload = {
            "email": "test@example.com",
            "password": "us",
            "name": "User Tester"
        }

        res = self.client.post(CREATE_USER_URL, payload=payload)
        self.assertEqaul(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().\
            objects.filter(email=payload["email"]).\
            exists()
        self.assertFalse(user_exists)
