from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from app.models import *
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(min_length=3, widget=forms.PasswordInput())

    def clean_username(self):
        data = self.cleaned_data['username']
        if not User.objects.filter(username=data).exists():
            raise forms.ValidationError("No user with this username")
        return data

    def clean_password(self):
        dataUsername = self.data['username']
        dataPassword = self.cleaned_data['password']

        if User.objects.filter(username=dataUsername).exists() and not authenticate(username=dataUsername, password=dataPassword):
            raise forms.ValidationError("Wrong password")
        return dataPassword

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50, widget=forms.EmailInput())
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=50, label='Repeat Password', widget=forms.PasswordInput())

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
             raise forms.ValidationError("This username is already used")
        return data

    def clean_password(self):
        dataPassword = self.cleaned_data['password']
        if len(dataPassword) < 3:
            raise ValidationError("Password must be longer than 3 symbols")
        return dataPassword

    def clean_password2(self):
        dataPassword = self.data['password']
        dataPassword2 = self.cleaned_data['password2']
        if dataPassword != dataPassword2:
            raise ValidationError("Passwords do not match")
        return dataPassword2

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "text", "tags"]

    def clean_title(self):
        data = self.cleaned_data['title']
        return data

    def clean_text(self):
        data = self.cleaned_data['text']
        return data


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["text"]

    def clean_text(self):
        data = self.cleaned_data['text']
        return data


class SettingsForm(forms.ModelForm):
    nickname = forms.CharField()
    avatar = forms.ImageField()

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if nickname.strip() == '':
            raise forms.ValidationError('Nickname is empty', code='validation_error')
        return nickname

    class Meta:
        model = User
        fields = ['nickname', 'email', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.user.profile.nickname = self.cleaned_data.get('nickname')
        self.user.profile.avatar = self.cleaned_data.get('avatar')
        if commit:
            self.user.profile.save()
        return self.user
