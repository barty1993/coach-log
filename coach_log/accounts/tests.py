from django.test import TestCase
from accounts.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from accounts.serializers import RegisterSerializer


class UserApiTestCase(APITestCase):

    def test_create_user(self):
        path = reverse('registration')
        client = APIClient()
        data = {"password": "HardPassword123",
                "email": "test@test.ru",
                "first_name": "test",
                "last_name": "test",
                "birthday": "1995-12-12"
                }
        response = client.post(path, data=data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        user = User.objects.get(email="test@test.ru")
        serializer_data = RegisterSerializer(user).data
        self.assertEqual(serializer_data, response.data)

