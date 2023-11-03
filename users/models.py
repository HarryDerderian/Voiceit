from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
  def _create_user(self, email, username, password, is_staff, is_superuser, **extra_fields):
    if not email or not username:
        raise ValueError('Users must have an email and username')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        username = username,
        is_staff = is_staff, 
        is_active = True,
        is_superuser = is_superuser, 
        last_login = now,
        date_joined = now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using = self._db)
    return user

  def create_user(self, email, username, password, **extra_fields):
    return self._create_user(email, username, password, False, False, **extra_fields)

  def create_superuser(self, email, username, password, **extra_fields):
    user=self._create_user(email, username, password, True, True, **extra_fields)
    return user

class User(AbstractBaseUser, PermissionsMixin) :
    # Require both email and username
    # We only want @csu.fullerton emails...
    # Lets work on that, the docs talk about a EmailValidator...
    def csuf_email_validator(value):
      if not value.endswith('@csu.fullerton.edu'):
        raise ValidationError("Only @csu.fullerton.edu email addresses are allowed.")
  
    email = models.EmailField(max_length=254, unique=True, validators = [csuf_email_validator])
    username = models.CharField(max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    # Gives access to data control and various methods...
    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)