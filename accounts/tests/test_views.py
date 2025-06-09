from django.urls import reverse
import pytest
from django.contrib.auth import get_user_model



from django.test.client import Client
from django.contrib.auth.hashers import check_password
from django.contrib.messages import get_messages
from accounts.models import PendingUser
from django.contrib.messages.storage.base import Message


User = get_user_model()
    
pytestmark = pytest.mark.django_db

def test_register_user(client: Client):
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
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].tags == 'success'
    # Assuming the success message is set in the view
    assert "verification code sent to" in str(messages[0]).lower()



def test_register_user_duplicate_email(client: Client, user_instance):
    url = reverse('register')
    data = {
        'password': 'testuser',
        'email': user_instance.email  # already exists
    }
    response = client.post(url, data)

    assert response.status_code == 302 # Redirect to register page
    # Check if the user is redirected to the register page
    assert response.url == reverse('register')

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].tags == 'error'
    assert "email exists" in messages[0].message.lower()




def test_verify_account_valid_code():
    pass


def test_verify_account_invalid_code():
    pass


def test_login_valid_credentials():
    pass


def test_login_invalid_credentials():
    pass
