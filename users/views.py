from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model,
    update_session_auth_hash,
)
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from .forms import CustomLoginForm, RegisterForm, ChangePasswordForm
from .mixins import RedirectAuthenticatedUserMixin

User = get_user_model()

# Views


class HomePageView(View):
    def get(self, request):
        return render(request, "home.html")


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect("login")


class LoginView(RedirectAuthenticatedUserMixin, View):
    form_class = CustomLoginForm
    template_name = "users/login.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user and user.is_active:
                login(request, user)
                messages.success(request, "You have logged in successfully.")
                return redirect("home")
            else:
                messages.error(request, "Invalid credentials or inactive account.")
        return render(request, self.template_name, {"form": form})


class RegisterView(View, RedirectAuthenticatedUserMixin):
    form_class = RegisterForm
    template_name = "users/register.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User is inactive until email is verified
            user.save()

            # Send email verification
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            verify_url = reverse(
                "verify_email", kwargs={"uidb64": uidb64, "token": token}
            )
            current_site = get_current_site(request)
            verification_link = f"http://{current_site.domain}{verify_url}"

            # Prepare and send email
            mail_subject = "Activate your account"
            message = render_to_string(
                "users/activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "verification_link": verification_link,
                },
            )

            send_mail(
                mail_subject,
                message,
                "noreply@eventsbooking.com",
                [user.email],
                fail_silently=False,
            )
            messages.success(
                request, "Please check your email to activate your account."
            )
            return redirect("login")
        return render(request, self.template_name, {"form": form})


class VerifyEmailView(View, RedirectAuthenticatedUserMixin):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request, "Email verification successful! You can now log in."
            )
            return redirect("login")
        else:
            messages.error(request, "Invalid verification link.")
            return redirect("home")


class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = "users/change_password.html"
    form_class = ChangePasswordForm
    success_url = reverse_lazy("home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        new_password = form.cleaned_data.get("new_password")
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, "Your password was changed successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your form submission.")
        return super().form_invalid(form)





