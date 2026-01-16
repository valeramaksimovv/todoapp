from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()

class FirstRunSetupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not User.objects.filter(is_superuser=True).exists():
            allowed_prefixes = ("/setup/", "/static/", "/media/")
            if not request.path.startswith(allowed_prefixes):
                return redirect("/setup/")
        return self.get_response(request)

        
