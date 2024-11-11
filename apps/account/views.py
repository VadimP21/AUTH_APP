from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import FormView, TemplateView, UpdateView, DetailView, ListView

from apps.account.forms import RegistrationForm, User, UserProfileForm
from apps.account.mixins import UserIsNotAuthenticated, SuperuserRequiredMixin
from apps.account.models import Profile


class RegisterView(UserIsNotAuthenticated, FormView):
    template_name = "account/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("account:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        login(self.request, user=user)
        return response

    def get_success_url(self):
        return self.success_url


class ProfileView(TemplateView):
    template_name = "account/profile.html"


class ProfileDetailView(DetailView):
    template_name = "account/profile.html"
    queryset = (User.objects
                .select_related("profile")
                .only("username", "email", "last_name", "first_name", "profile__biography")
                )
    context_object_name = 'user'


class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    queryset = (User.objects
                .select_related("profile")
                .only("username")
                )
    form_class = UserProfileForm
    template_name = 'account/profile_update.html'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        self.object = self.get_object()
        update_by_current_user = self.object == self.request.user
        return update_by_current_user

    def get_success_url(self):
        return reverse("account:profile_details",
                       kwargs={"pk": self.object.pk},
                       )

    def form_valid(self, form):
        response = super().form_valid(form)
        bio = form.cleaned_data.get('bio')
        current_profile = Profile.objects.get(user=self.request.user)
        current_profile.biography = bio
        current_profile.save()
        return response


class ProfileListView(SuperuserRequiredMixin, ListView):
    template_name = 'account/profile_llist.html'
    model = User
    context_object_name = 'users'
