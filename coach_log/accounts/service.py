from accounts.models import User


def is_already_exists(request):
    email = request.data.get('email')
    user = User.objects.filter(email=email).exists()
    if user:
        return True
    return False
