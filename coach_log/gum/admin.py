from django.contrib import admin

from gum.models import Gum, KindOfSport, City, CoachInGum

admin.site.register([Gum, KindOfSport, City, CoachInGum])

