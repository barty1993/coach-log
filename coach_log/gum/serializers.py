import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from accounts.models import User
from gum.models import Gum


class UserSerializerForDetailGum(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    birthday = serializers.DateField()
    about_me = serializers.CharField()
    class Meta:
        model = User
        fields = ('id', 'avatar', 'first_name', 'last_name', 'birthday', 'about_me')


class GumListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    city = serializers.StringRelatedField()
    kind_of_sport = serializers.StringRelatedField(many=True)

    class Meta:
        model = Gum
        fields = ('id','owner', 'avatar', 'city', 'title', 'address', 'kind_of_sport')


class GumDetailSerializer(serializers.ModelSerializer):
    owner = UserSerializerForDetailGum()
    city = serializers.StringRelatedField()
    kind_of_sport = serializers.StringRelatedField(many=True)
    coaches = serializers.SerializerMethodField()

    class Meta:
        model = Gum
        fields = ('id', 'city', 'owner', 'avatar', 'title', 'address', 'phone', 'kind_of_sport', 'coaches')

    def get_coaches(self, instance):
        coaches = User.objects.filter(gum=instance, coach__is_agree=True)
        serializer = UserSerializerForDetailGum(coaches, many=True).data
        return serializer


class GumCreateUpdateSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    city = serializers.CharField()
    title = serializers.CharField()
    about_gum = serializers.CharField()
    address = serializers.CharField()
    phone = serializers.CharField()

    def validate_phone(self, value):
        if not re.match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', value) or len(value) > 12:
            raise ValidationError("Phone number must be entered in the format: '+79999999999'. Up to 11 digits allowed")
        return value


class KindOfSportSerializer(serializers.Serializer):
    kind_of_sport = serializers.StringRelatedField()


class InviteCoachSerializer(serializers.Serializer):
    which_gum = serializers.IntegerField()
    which_user = serializers.EmailField()


class DeclineAcceptInviteSerializer(serializers.Serializer):
    is_agree = serializers.BooleanField()

