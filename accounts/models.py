from datetime import datetime, timezone
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager
from common.models import BaseModel

# Create your models here.


class User(
    BaseModel, AbstractBaseUser, PermissionsMixin
):  # Inheriting the basemodel abstract class from common folder
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# Email verification
class PendingUser(
    BaseModel
):  # Inheriting the basemodel abstract class from common folder
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    verification_code = models.CharField(max_length=255)

    def is_valid(self) -> bool:
        lifespan_in_seconds = 20 * 60
        now = datetime.now(timezone.utc)

        timediff = now - self.created_at
        timediff = timediff.total_seconds()
        if timediff > lifespan_in_seconds:
            return False
        return True

    def __str__(self):
        return self.email


# For reset


class Token(BaseModel):
    class TokenType(models.TextChoices):
        PASSWORD_RESET = ("PASSWORD_RESET", "PASSWORD_RESET")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=100, choices=TokenType.choices)
   

    def __str__(self):
        return f"{self.user}  {self.token}"
    
    #check if token is valid
    def is_valid(self) -> bool:
        lifespan_in_seconds = 20 * 60  # 20 mins
        now = datetime.now(timezone.utc)
        timediff = now - self.created_at
        timediff = timediff.total_seconds()
        if timediff > lifespan_in_seconds:
            return False
        return True

