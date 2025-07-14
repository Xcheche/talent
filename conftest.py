"""
For adding fixtures to a Django test environment.
This file contains pytest fixtures for setting up a Django test environment.
It includes a client fixture for making requests, a user instance fixture for creating a test user,
and an authentication user password fixture for testing purposes.
"""

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
        email="testuser@example.com", password="testpassword123"
    )


@pytest.fixture
def auth_user_password() -> str:
    return "testpassword123"
