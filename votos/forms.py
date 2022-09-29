from django import forms 
from django.contrib.auth.models import User
from .models import Poll, Choice

class AddPollForm(forms.ModelForm):
    choice1 = forms.CharField(
        label='C1',
        max_length=200,
        min_length=1,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    choice2 = forms.CharField(
        label='C2',
        max_length=200,
        min_length=1,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    
    class Meta:
        model = Poll
        fields = ['text', 'choice1', 'choice2']
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'cols': 20
                }
            ),
        }
    
class EditPollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['text',]
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'cols': 20
                }
            ),
        }
        
class AddChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text',]
        widgets = {
            'choice-text': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }
        
class SignupUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password',]
        widgets = {
            'password': forms.PasswordInput()
        }
    
class SignupStaffForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password',]
        widgets = {
            'password': forms.PasswordInput()
        }