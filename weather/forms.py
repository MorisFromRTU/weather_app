from django import forms

class CityForm(forms.Form):
    city = forms.CharField(
        max_length=100, 
        label='City name',
        widget=forms.TextInput(attrs={'id': 'city-input','class': 'form-control', 'placeholder': 'Enter city name'})
    )

class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=20, 
        label='Никнейм', 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Пароль', 
        required=True)
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Подтвердите пароль', 
        required=True)
    

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20, 
        label='Никнейм', 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Пароль', 
        required=True)