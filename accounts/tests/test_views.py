from django.urls import reverse
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user


from django.test.client import Client
from django.contrib.auth.hashers import check_password
from django.contrib.messages import get_messages
from accounts.models import PendingUser
from django.contrib.messages.storage.base import Message

from conftest import client


User = get_user_model()  # Ensure that the User model is imported correctly

pytestmark = (
    pytest.mark.django_db
)  # Ensure that all tests run with a database transaction


# Test for registering a new user
def test_register_user(client: Client):
    url = reverse("register")
    data = {"password": "testuser", "email": "testuser@example.com"}
    response = client.post(url, data)
    assert response.status_code == 200
    pending_user = PendingUser.objects.filter(email=data["email"]).first()

    assert pending_user
    assert check_password(data["password"], pending_user.password)
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].tags == "success"
    # Assuming the success message is set in the view
    assert "verification code sent to" in str(messages[0]).lower()


# Test for registering a user with an existing email
def test_register_user_duplicate_email(client: Client, user_instance):
    url = reverse("register")
    data = {"password": "testuser", "email": user_instance.email}  # already exists
    response = client.post(url, data)

    assert response.status_code == 302  # Redirect to register page
    # Check if the user is redirected to the register page
    assert response.url == reverse("register")

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].tags == "error"
    assert "email exists" in messages[0].message.lower()


# Test for verify account with valid code
def test_verify_account_valid_code(client: Client):
    pending_user = PendingUser.objects.create(
        email="abc@gmail.com", verification_code="123456", password="testpassword"
    )
    url = reverse("verify_account")

    data = {"email": pending_user.email, "code": pending_user.verification_code}
    response = client.post(url, data)
    assert response.status_code == 302  # for redirection
    assert response.url == reverse(
        "home"
    )  # Assuming the user is redirected to login after verification
    user = get_user(response.wsgi_request)
    assert user.is_authenticated


# Test for verify account with invalid code
def test_verify_account_invalid_code():
    client = Client()
    pending_user = PendingUser.objects.create(
        email="abc@gmail.com", verification_code="123456", password="testpassword"
    )

    url = reverse("verify_account")
    data = {"email": pending_user.email, "code": "wrongcode"}  # Invalid code
    response = client.post(url, data)
    assert response.status_code == 400  # Assuming the view returns 200 for invalid code
    assert User.objects.count() == 0  # No user should be created


# Test for login with valid credentials
def test_login_valid_credentials(client: Client, user_instance):
    url = reverse("login")

    data = {
        "email": user_instance.email,
        "password": "testpassword123",  # Plaintext password
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect after login
    assert response.url == reverse("home")

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].tags == "success"
    assert "you are now logged in" in messages[0].message.lower()


def test_login_invalid_credentials(client: Client, user_instance):
    url = reverse("login")
    data = {"email": user_instance.email, "password": "randominvalidpass"}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse("login")

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].level_tag == "error"
    assert "invalid" in str(messages[0]).lower()
