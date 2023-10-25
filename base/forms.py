from django.forms import ModelForm
from .models import Petition

class PetitionForm(ModelForm) :
    class Meta:
         model = Petition
         fields = ["title", "category", "description"]
