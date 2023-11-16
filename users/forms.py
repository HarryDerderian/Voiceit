from django.contrib.auth.forms import UserCreationForm
from .models import User
 

 # Input form for user creation, pass it to the front end.
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username')