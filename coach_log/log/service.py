from accounts.models import User
from gum.models import Gum


def get_gum_or_none(gum_id: int, owner: User):
    try:
        gum = Gum.objects.get(id=gum_id, owner=owner)
        return gum
    except:
        return None