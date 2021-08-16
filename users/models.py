from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid

# Create your models here.

GENDER_CHOICES = (
    (0, 'Male'),
    (1, 'Female'),
    (2, 'Not to disclose')
)


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, gender = 1, **extra_fields):  #유저생성
        if not email:
            raise ValueError('This given email must be set')
        email = self.normalize_email(email)
        username = self.normalize_email(username)
        user = self.model(email=email, username=username, gender=gender, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username='', password = None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self._create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(max_length=255, verbose_name="email", unique=True)
    username = models.CharField(max_length=64, verbose_name="username", unique=True)
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name='registered_date')
    phoneNumber = PhoneNumberField(unique=True, null=True, blank=False)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=2)
    last_login = models.DateTimeField(auto_now_add=True, verbose_name="Last Login")
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='media')

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
