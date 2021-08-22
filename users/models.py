from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.files.storage import FileSystemStorage
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import Thumbnail
from datetime import datetime
from django.utils import timezone
from django.db import models
from django.conf import settings
import uuid
import os

# Create your models here.

GENDER_CHOICES = (
    (0, 'Male'),
    (1, 'Female'),
    (2, 'Not to disclose')
)


# # 파일들 overwrite 되게 하기
# class OverwriteStorage(FileSystemStorage):
#     def get_available_name(self, name, max_length=None):
#         if self.exists(name):
#             os.remove(os.path.join(settings.MEDIA_ROOT, name))
#         return name
#
#
# def profile_upload_to(instance, filename):
#     cls_name = instance.__class__.__name__.lower()
#     file_name = uuid.uuid4().hex
#     ymd_path = timezone.now().strftime('%Y/%m/%d')
#     extension = os.path.splitext(filename)[-1].lower()
#     return '/'.join([
#         'profile_upload',
#         ymd_path,
#         file_name + extension,
#     ])


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, gender=1, **extra_fields):  #유저생성
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(max_length=255, verbose_name="email", unique=True)
    password = models.CharField(max_length=255, verbose_name='password')
    username = models.CharField(null=True, blank=True, max_length=64, verbose_name="username", unique=True)
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name='registered_date')
    phoneNumber = PhoneNumberField(unique=True, null=True, blank=False)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=2)
    last_login = models.DateTimeField(auto_now_add=True, verbose_name="Last Login")
    bio = models.TextField(blank=True, null=True)
    # profile_image = models.ImageField(null=True, blank=True, upload_to=profile_upload_to, storage=OverwriteStorage())
    # image = ImageSpecField(source='profile_image', processors=[Thumbnail(64, 64), ], format='JPEG',
    #                        options={'quality': 90, })



    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

