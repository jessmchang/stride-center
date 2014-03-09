from functools import wraps
from django.utils.decorators import available_attrs
from django.shortcuts import redirect

def public_only(function=None):
    """
    Decorator for views that checks that the user is NOT logged in,
    redirecting to the homepage if necessary.
    """

    def wrapper(request, *args, **kw):
        if request.user.is_authenticated():
            return redirect('jobmatch.views.dashboard')
        else:
            return function(request, *args, **kw)
    return wrapper