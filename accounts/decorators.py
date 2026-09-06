from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def super_admin_required(view_func):
    """Decorator to ensure only SUPER_ADMIN can access the view."""
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == "SUPER_ADMIN":
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view
