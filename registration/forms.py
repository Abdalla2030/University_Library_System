from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django import forms
from django.contrib.auth import authenticate, get_user_model

from .models import User as UserModel

User = get_user_model()


class UserSignupForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    username = forms.CharField(label="Username", required=False)
    password = forms.CharField(
        widget=forms.PasswordInput, label="Password", required=False)
    confirmPassword = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password", required=False)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password',
            'confirmPassword'
        ]

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        confirmPassword = self.cleaned_data.get('confirmPassword')

        doesUsernameExist = User.objects.filter(username=username).exists()

        if doesUsernameExist:
            raise forms.ValidationError('This username is already exist !')
        if password != confirmPassword:
            raise forms.ValidationError('These passwords are not matched !')

        return super(UserSignupForm, self).clean(*args, **kwargs)


class UserUpdateInfoForm(UserChangeForm):
    first_name = forms.CharField(label='First Name', required=True)
    last_name = forms.CharField(label='Last Name', required=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username'
        ]


class UserUpdatePassForm(PasswordChangeForm):
    def clean(self):
        return super(UserUpdatePassForm, self).clean()


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    userType = forms.CharField(
        disabled=True, label='User Type', widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'userType'
        ]

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        userType = self.cleaned_data.get('userType')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError(
                    'This user does not exist or the password is incorrect !')
            if not user.is_active:
                raise forms.ValidationError('This user does not exist !')

            userQuerySet = UserModel.objects.filter(user=user).values()
            userData = [row for row in userQuerySet]
            storedUserType = userData[0]['userType']

            if userType != storedUserType:
                raise forms.ValidationError(
                    'There is no ' + userType + ' with this username !')

        return super(UserLoginForm, self).clean(*args, **kwargs)
