from rest_framework import serializers

from log.models import Athlete


class ListCreateAthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = ('id', 'first_name', 'last_name', 'birthday', 'gum')