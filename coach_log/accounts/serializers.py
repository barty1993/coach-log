from rest_framework import serializers
from accounts.models import User
from gum.serializers import GumListSerializer


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True, min_length=2)
    last_name = serializers.CharField(required=True, min_length=2)
    birthday = serializers.DateField(default=None)
    about_me = serializers.CharField(default=None)
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'birthday', 'about_me', 'password')


    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            birthday=validated_data['birthday'],
            about_me=validated_data['about_me']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    birthday = serializers.DateField()
    about_me = serializers.CharField()
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    gums = GumListSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'birthday', 'about_me', 'user', 'gums')


class UpdateUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(min_length=2)
    last_name = serializers.CharField(min_length=2)
    birthday = serializers.DateField()
    about_me = serializers.CharField()
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'birthday', 'about_me', 'user')