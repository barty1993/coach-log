from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase

from accounts.models import User
from accounts.serializers import RegisterSerializer, UserSerializer, UpdateUserSerializer
from accounts.service import is_already_exists


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        if is_already_exists(request):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "email already exists"})
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GetAuthUserAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def get_queryset(self):
        user = User.objects.filter(id=self.request.user.id).prefetch_related('gums__city', 'gums__kind_of_sport')
        return user


class UpdateUserAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = UpdateUserSerializer

    def get_queryset(self):
        user = User.objects.filter(pk=self.request.user.pk)
        return user


class CustomTokenViewBase(TokenViewBase):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        user = User.objects.get(email=request.data['email'])
        serialize_user = UserSerializer(user).data
        return Response([serializer.validated_data, serialize_user], status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView, CustomTokenViewBase):
    pass