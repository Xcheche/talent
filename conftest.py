from django.test.client import Client
import pytest

from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

User = get_user_model()



@pytest.fixture
def client():
    return Client()


# pytest fixture to create a user instance for testing

@pytest.fixture
def user_instance(db):
    return User.objects.create_user(
        email='testuser@example.com',
        password='testpassword123'
    )