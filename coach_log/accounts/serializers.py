from rest_framework import serializers

from accounts.models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
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