from django.shortcuts import redirect


class RedirectAuthenticatedUserMixin:
    """Redirect authenticated users to home if they try to access login/register."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")  # Redirect authenticated users to home page
        return super().dispatch(request, *args, **kwargs)
