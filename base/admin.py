from django.contrib import admin

# Register your models here.
from .models import Petition, Category, PetitionReply

admin.site.register(Petition)
admin.site.register(Category)
admin.site.register(PetitionReply)