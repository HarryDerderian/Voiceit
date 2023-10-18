from django.db import models

# Create your models here.

class Petition(models.Model) :
    #author = ?
    
    TITLE_CHAR_LIMIT = 150
    title = models.CharField(max_length = TITLE_CHAR_LIMIT)
    # category = ?

    ALLOW_EMPTY_TEXT = True
    description = models.TextField(null = ALLOW_EMPTY_TEXT, blank = ALLOW_EMPTY_TEXT)
    # signatures = ?

    last_updated = models.DateTimeField(auto_now = True)
    creation_date = models.DateTimeField(auto_now_add = True)

    # Petition class as a String
    def __str__(self) :
        return str(self.title)