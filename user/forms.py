from django import forms

from user.models import RegisterModel


class RegisterForms(forms.ModelForm):
    class Meta:
        model=RegisterModel
        fields=("firstname","lastname","userid","password","mobilenumber","email","gender",)
        widgets = {
            'firstname': forms.TextInput(attrs={'required': 'required'}),
            'lastname': forms.TextInput(attrs={'required': 'required'}),
            'userid': forms.TextInput(attrs={'required': 'required'}),
            'password': forms.PasswordInput(attrs={'required': 'required'}),
            'mobilenumber': forms.TextInput(attrs={
                'type': 'tel',
                'required': 'required',
                'pattern': '[0-9]{10}',
                'title': 'Please enter exactly 10 digits',
                'maxlength': '10',
                'minlength': '10'
            }),
            'email': forms.EmailInput(attrs={'required': 'required'}),
            'gender': forms.TextInput(attrs={'required': 'required'}),
        }