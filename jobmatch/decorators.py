from functools import wraps
from django.utils.decorators import available_attrs

def public_only(function=None):
    """
    Decorator for views that checks that the user is NOT logged in,
    redirecting to the homepage if necessary.
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated():
                return redirect('jobmatch.views.dashboard')
            else:
                return view_func(request, *args, **kwargs)
        return _wrapped_view
    
    return decorator