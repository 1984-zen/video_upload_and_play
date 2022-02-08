from django import forms
from django.conf import settings
from accounts.models import Users

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-confirm-password"
            }
        )
    )

class LoginForm(forms.Form):
    username =  forms.CharField(
                    required=True,
                    max_length=255,
                    label='username',
                    widget=forms.TextInput(
                        attrs={
                        "class": "form-control"
                        }
                    )
                )
    password =  forms.CharField(
                    required=True,
                    max_length=255,
                    label='password',
                    widget=forms.PasswordInput( # 這個可以讓輸入的password變隱藏
                        attrs={
                            "class": "form-control",
                            "id": "user-password"
                        }
                    )
                )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = Users.objects.filter(username__iexact=username) # thisIsMyUsername == thisismyusername
        if not qs.exists():
            raise forms.ValidationError("This is an invalid user.")
        if qs.count() != 1:
            raise forms.ValidationError("This is an invalid user.")
        return username