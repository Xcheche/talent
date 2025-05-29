from django.urls import reverse
import pytest
from django.contrib.auth.models import User
from django.test.client import Client
from django.contrib.auth.hashers import check_password

from accounts.models import PendingUser
    


def test_register_user(db, client: Client):
    url = reverse('register')
    data = {
        'password': 'testuser',
        'email': 'testuser@example.com'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    pending_user = PendingUser.objects.filter(email=data['email']).first()
    
    assert pending_user
    assert check_password(data['password'], pending_user.password)


def test_register_user_duplicate_email(client):
    pass


def test_verify_account_valid_code():
    pass


def test_verify_account_invalid_code():
    pass


def test_login_valid_credentials():
    pass


def test_login_invalid_credentials():
    pass
