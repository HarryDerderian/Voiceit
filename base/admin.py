from django.contrib import admin

# Register your models here.
from .models import Petition

admin.site.register(Petition)