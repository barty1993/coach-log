import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from gum.models import Gum


class GumListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    city = serializers.StringRelatedField()
    kind_of_sport = serializers.StringRelatedField(many=True)

    class Meta:
        model = Gum
        fields = ('id','owner', 'avatar', 'city', 'title','address', 'about_gum', 'phone', 'kind_of_sport')


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




