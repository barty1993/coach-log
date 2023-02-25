from django.db import models

from accounts.models import User
from gum.models import KindOfSport, Gum


class Group(models.Model):
    title = models.CharField(max_length=255)
    gum = models.ForeignKey(Gum, related_name='groups', on_delete=models.CASCADE)
    coach = models.ForeignKey(User, related_name='groups', null=True, on_delete=models.SET_NULL)
    kind_of_sport = models.ForeignKey(KindOfSport, related_name='groups',null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class Athlete(models.Model):
    avatar = models.ImageField(blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday = models.DateField()
    gum = models.ForeignKey(Gum, on_delete=models.CASCADE)
    group = models.ManyToManyField(Group, through='Membership')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"группа: {self.group.title}, спортсмен: {self.athlete.last_name}"



