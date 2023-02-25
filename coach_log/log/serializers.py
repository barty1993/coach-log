from rest_framework import serializers

from log.models import Athlete


class CreateUpdateAthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = ('id', 'first_name', 'last_name', 'birthday', 'gum')


class CreateGroupSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    gum_id = serializers.IntegerField()
    coach_id = serializers.IntegerField()
    kind_of_sport_id = serializers.IntegerField()


class UpdateGroupSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    coach_id = serializers.IntegerField()
