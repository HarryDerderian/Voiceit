from django.contrib import admin

# This file registers classes, (data on the webpage) to our admin page
# It allows us to edit or remove anything that is registered here.
from .models import Petition, Category, PetitionReply, Signature

admin.site.register(Petition)
admin.site.register(Category)
admin.site.register(PetitionReply)
admin.site.register(Signature)