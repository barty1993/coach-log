from django.contrib import admin

from log.models import Group, Athlete, Membership

admin.site.register([Group, Athlete, Membership])
