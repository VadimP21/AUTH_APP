from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "user-input"
        self.fields["username"].widget.attrs["placeholder"] = "E-mail"
        self.fields["password"].widget.attrs["placeholder"] = "*********"
