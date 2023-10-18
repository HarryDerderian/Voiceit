from django.contrib import admin

# Register your models here.
from .models import Petition, Category

admin.site.register(Petition)
admin.site.register(Category)