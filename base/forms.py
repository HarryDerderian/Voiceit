from django.forms import ModelForm
from .models import Petition, PetitionReply

# This file is used for input forms that can be passed to the front end

class PetitionForm(ModelForm) :
    class Meta:
         model = Petition
         fields = ["title", "category", "description", "signature_goal"]

class PetitionReplyForm(ModelForm) :
    class Meta:
        model = PetitionReply
        fields = ['description']