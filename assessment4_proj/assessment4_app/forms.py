from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


# django models forms
class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    


class UserForm(UserCreationForm):
    is_superuser = forms.BooleanField(required=True)
    
    
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'state', 'password1', 'password2',)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        
        # exclude = [] includes all the fields
        fields = ['food_name', 'food_groups', 'bio_degradable']
        
        #changing the labels on the forms
        labels = {
        }

class WasteAuditForm(forms.ModelForm):
    class Meta:
        model = WasteAudit
        fields = ['entry_date', 'user', 'food_item', 'waste_type', 'amount']