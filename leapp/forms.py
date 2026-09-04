from django import forms
from .models import Car
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'price', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter car name'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter car price'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter car description'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'