from django.db import models
from django.contrib.auth.models import User
from voicelt.settings import AUTH_USER_MODEL
import uuid


# The data making up our website
# Everything on the website can mostly like be found here.
# If not here it's built in, or in our custom users dir
class Category(models.Model) :
    category_str = models.CharField(max_length = 100)
    # category class as a String
    def __str__(self) :
        return str(self.category_str)

class Petition(models.Model) :
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE, null = True)
    default_category = Category.objects.get(category_str="Other")
    category = models.ForeignKey(Category,  on_delete = models.CASCADE, null = False, blank = False,default=default_category.pk)
    signature_goal = models.PositiveIntegerField(null = True, blank = True)
    total_signatures = models.PositiveIntegerField(default = 0, null = True, blank = True)
    TITLE_CHAR_LIMIT = 70
    title = models.CharField(max_length = TITLE_CHAR_LIMIT, null=False, blank = False)
    ALLOW_EMPTY_TEXT = False
    description = models.TextField(null = ALLOW_EMPTY_TEXT, blank = ALLOW_EMPTY_TEXT, default="No description given.")
    last_updated = models.DateTimeField(auto_now = True)
    creation_date = models.DateTimeField(auto_now_add = True)
    # Petition class as a String
    def __str__(self) :
        return str(self.title)

class Signature(models.Model) :
    creation_date = models.DateTimeField(auto_now_add = True)
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