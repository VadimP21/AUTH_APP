from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, EmailInput, PasswordInput, CharField

from apps.account.models import Profile

User = get_user_model()


class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = "email", "password"
        widgets = {
            "email": EmailInput(
                attrs={
                    "class": "user-input",
                    "placeholder": "E-mail",
                    "id": "email",
                }
            ),
            # "username": TextInput(
            #     attrs={
            #         "class": "user-input",
            #         "placeholder": "Имя",
            #         "id": "username",
            #     }
            # ),
            "password": PasswordInput(
                attrs={
                    "placeholder": "Пароль",
                    "id": "password",
                }
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        profile = Profile(user=user)

        if commit:
            user.save()
            profile.save()

            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user

    def _post_clean(self):
        super()._post_clean()

        password = self.cleaned_data.get("password")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password", error)


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "user-input"
        self.fields["username"].widget.attrs["placeholder"] = "E-mail"
        self.fields["password"].widget.attrs["placeholder"] = "*********"


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = 'username', 'first_name', 'last_name',

    bio = CharField(max_length=500)
