from accounts.models import User
from gum.models import Gum, KindOfSport, CoachInGum
from log.models import Athlete, Group


def get_gum_or_none(gum_id: int, owner: User):
    try:
        gum = Gum.objects.get(id=gum_id, owner=owner)
        return gum
    except:
        return None


def get_athlete_or_none(athlete_id: int):
    try:
        athlete = Athlete.objects.get(id=athlete_id)
        return athlete
    except:
        return None

def get_kind_of_sport_or_none(pk: int):
    try:
        kind_of_sport = KindOfSport.objects.get(id=pk)
        return kind_of_sport
    except:
        return None

def coach_in_gum_or_owner(gum: Gum, coach_id: int):
    if coach_id == gum.owner_id:
        return True
    try:
        coach_in_gum = CoachInGum.objects.get(gum=gum, coach_id=coach_id, is_agree=True)
        return True
    except:
        return False

def get_group_or_none(pk: int, user: User):
    try:
        group = Group.objects.get(pk=pk, gum__owner=user)
        return group
    except:
        return None
