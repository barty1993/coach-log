from rest_framework import serializers

from gum.models import Gum


class GumListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    city = serializers.StringRelatedField()
    kind_of_sport = serializers.StringRelatedField(many=True)

    class Meta:
        model = Gum
        fields = ('id','owner', 'avatar', 'city', 'title','address', 'about_gum', 'phone', 'kind_of_sport')




