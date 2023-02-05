from django.forms import model_to_dict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from gum.models import Gum, City, KindOfSport
from gum.serializers import GumListSerializer, GumCreateUpdateSerializer, KindOfSportSerializer


class ListGumForAuthUserAPIView(generics.ListAPIView):
    queryset = Gum.objects.all()
    serializer_class = GumListSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = Gum.objects.filter(owner=self.request.user).\
            prefetch_related('kind_of_sport').\
            prefetch_related('city').\
            select_related('owner')
        return queryset


class ListGumAPIView(generics.ListAPIView):
    """Вывожит список залов для не аутентифицированных пользователей с фильтрацией по
    city__name, kind_of_sport__name"""

    queryset = Gum.objects.all()
    serializer_class = GumListSerializer
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ['city__name', 'kind_of_sport__name', ]

    def get_queryset(self):
        queryset = Gum.objects.all().prefetch_related('kind_of_sport').prefetch_related('city').select_related('owner')
        return queryset


class CreateUpdateGumAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = GumCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        city = get_object_or_404(City, name=request.data['city'])
        new_gum = Gum.objects.create(owner=self.request.user,
                                     city=city,
                                     title=request.data['title'],
                                     about_gum=request.data['about_gum'],
                                     address=request.data['address'],
                                     phone=request.data['phone'])
        return Response(status=status.HTTP_201_CREATED,
                        data=GumCreateUpdateSerializer(new_gum).data)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        instance = get_object_or_404(Gum, pk=pk, owner=request.user)
        serializer = GumCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            city = City.objects.get(name=serializer.data['city'])
            instance.city = city
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"error": f"Города {serializer.data['city']} в базе нет"})
        instance.title = serializer.data['title']
        instance.about_gum = serializer.data['about_gum']
        instance.address = serializer.data['address']
        instance.phone = serializer.data['phone']
        instance.save()
        return Response(data=GumCreateUpdateSerializer(instance).data, status=status.HTTP_200_OK)


class AddKindOfSportAPIView(APIView):

    """Добавляет 1 вид спорта переданный в запросе (если он создан в базе данных)"""

    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        serializer = KindOfSportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Method POST not allowed"})
        else:
            gum = get_object_or_404(Gum, pk=pk, owner=request.user)
        if request.data.get('kind_of_sport', None):
            try:
                kind_of_sport = KindOfSport.objects.get(name=request.data['kind_of_sport'])
                gum.kind_of_sport.add(kind_of_sport)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={"message": f"Вида спорта {request.data['kind_of_sport']} в базе нет"})
        return Response(status=status.HTTP_201_CREATED,
                        data={"message": f"Вид спорта {request.data['kind_of_sport']} успешно добавлен"})





class InviteCoachAPIView(APIView):
    pass