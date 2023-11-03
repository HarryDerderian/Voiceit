from django.db import models
from django.contrib.auth.models import User
from voicelt.settings import AUTH_USER_MODEL
import uuid
# Create your models here.

class Category(models.Model) :
    category_str = models.CharField(max_length = 100)
    # category class as a String
    def __str__(self) :
        return str(self.category_str)

class Petition(models.Model) :
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE, null = True)
    category = models.ForeignKey(Category,  on_delete = models.SET_NULL, null = True)
    signature_goal = models.PositiveIntegerField(null = True, blank = True)
    total_signatures = models.PositiveIntegerField(null = True, blank = True)
    TITLE_CHAR_LIMIT = 150
    title = models.CharField(max_length = TITLE_CHAR_LIMIT)
    ALLOW_EMPTY_TEXT = True
    description = models.TextField(null = ALLOW_EMPTY_TEXT, blank = ALLOW_EMPTY_TEXT)
    last_updated = models.DateTimeField(auto_now = True)
    creation_date = models.DateTimeField(auto_now_add = True)
    # Petition class as a String
    def __str__(self) :
        return str(self.title)

class Signature(models.Model) :
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE, null = True)
    petition = models.ForeignKey(Petition, on_delete = models.CASCADE, null = True)


class PetitionReply(models.Model) :
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    # The author of the reply
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE, null = True)
    # The petition the reply belongs to
    petition = models.ForeignKey(Petition, on_delete = models.CASCADE, null = True)
    # The message of the relpy
    ALLOW_EMPTY_TEXT = False
    description = models.TextField(null = ALLOW_EMPTY_TEXT, blank = ALLOW_EMPTY_TEXT)