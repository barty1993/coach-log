from django.db import models

from accounts.models import User
from gum.validators import phone_regex


class City(models.Model):
    name = models.CharField(unique=True, max_length=255)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class KindOfSport(models.Model):
    name = models.CharField(unique=True, max_length=255)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Gum(models.Model):
    avatar = models.ImageField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="o_gums")
    city = models.ForeignKey(City, related_name="city", on_delete=models.SET_NULL, null=True)
    kind_of_sport = models.ManyToManyField(KindOfSport, related_name="kind_of_sports")
    title = models.CharField(max_length=255)
    about_gum = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    coaches = models.ManyToManyField(User, through='CoachInGum')

    def __str__(self):
        return self.title


class CoachInGum(models.Model):
    gum = models.ForeignKey(Gum, on_delete=models.CASCADE)
    coach = models.ForeignKey(User, on_delete=models.CASCADE)
    is_agree = models.BooleanField(default=False)

