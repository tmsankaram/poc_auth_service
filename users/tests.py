from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            company_name="TestCo",
            department_code="TST",
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("password123"))
        self.assertEqual(user.company_name, "TestCo")
        self.assertEqual(user.department_code, "TST")
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email="admin@example.com",
            password="password123",
            company_name="AdminCo",
            department_code="ADM",
        )
        self.assertEqual(user.email, "admin@example.com")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class UserAPITest(APITestCase):
    def test_register_user(self):
        url = reverse("register")
        data = {
            "email": "newuser@example.com",
            "password": "password123",
            "company_name": "NewCo",
            "department_code": "NEW",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "newuser@example.com")

    def test_login_user(self):
        # Create user
        User.objects.create_user(
            email="login@example.com",
            password="password123",
            company_name="LoginCo",
            department_code="LOG",
        )
        url = reverse("token_obtain_pair")
        data = {"email": "login@example.com", "password": "password123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
