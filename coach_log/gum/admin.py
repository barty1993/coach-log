from django.contrib import admin

from gum.models import Gum, KindOfSport, City

admin.site.register([Gum, KindOfSport, City])

