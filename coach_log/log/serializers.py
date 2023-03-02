from rest_framework import serializers

from accounts.models import User
from log.models import Athlete, Group


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


class ListGroupSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    coach = serializers.StringRelatedField()
    title = serializers.CharField(max_length=255)
    kind_of_sport = serializers.StringRelatedField()


class AddAthleteSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    athlete_id = serializers.ListField(child=serializers.IntegerField())


class DetailGroupSerializer(serializers.ModelSerializer):
    gum = serializers.StringRelatedField()
    coach = serializers.SerializerMethodField()
    kind_of_sport = serializers.StringRelatedField()
    athletes = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = '__all__'

    def get_athletes(self, instance):
        athletes = Athlete.objects.filter(group=instance)
        serializer = AthleteSerializer(athletes, many=True).data
        return serializer

    def get_coach(self, instance):
        coach = User.objects.get(groups=instance)
        serializer = CoachSerializer(coach).data
        return serializer


class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = ('id', 'avatar', 'first_name', 'last_name', 'birthday')


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'avatar', 'first_name', 'last_name', 'birthday')
