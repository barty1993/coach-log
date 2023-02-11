from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from gum.models import Gum, City, KindOfSport, CoachInGum
from gum.serializers import GumListSerializer, GumCreateUpdateSerializer, KindOfSportSerializer, InviteCoachSerializer, \
    GumDetailSerializer, DeclineAcceptInviteSerializer


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
    """Выводит список залов для не аутентифицированных пользователей с фильтрацией по
    city__name, kind_of_sport__name"""

    queryset = Gum.objects.all()
    serializer_class = GumListSerializer
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ['city__name', 'kind_of_sport__name', ]

    def get_queryset(self):
        queryset = Gum.objects.all().prefetch_related('kind_of_sport').prefetch_related('city').select_related('owner')
        return queryset


class DetailGumAPIView(generics.RetrieveAPIView):
    queryset = Gum.objects.all().select_related('owner')
    serializer_class = GumDetailSerializer
    permission_classes = (AllowAny, )


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
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = InviteCoachSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            gum = Gum.objects.get(owner=self.request.user, id=request.data['which_gum'])
        except:
            return Response(data={'error': f"зал с id {request.data['which_gum']} не принадлежит этому юзеру"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            coach = User.objects.get(email=request.data['which_user'])
        except:
            return Response(data={'error': f"user with email {request.data['which_user']} does no exist"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            coach_in_gum = CoachInGum.objects.get(gum=gum, coach=coach)
        except:
            coach_in_gum = None
        if coach_in_gum:
            if coach_in_gum.is_agree is False:
                return Response(data={'error': f"заявка тренеру {coach.email} в обработке"},
                                status=status.HTTP_200_OK)
            else:
                return Response(data={'error': f"тренер {coach.email} числится в вашем зале {gum.id}"},
                                status=status.HTTP_200_OK)
        else:
            add_coach_in_gum = CoachInGum.objects.create(gum=gum,
                                                         coach=coach)
            add_coach_in_gum.save()
        return Response(data={'message': f"заявка тренеру {coach.email} в зал {gum.id} - отправлена"},
                        status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        serializer = DeclineAcceptInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            coach_in_gum = CoachInGum.objects.get(gum_id=pk, coach_id=request.user.id, is_agree=False)
        except:
            return Response(data={'error': f'заявки в зал {pk} не существует'},
                            status=status.HTTP_400_BAD_REQUEST)
        coach_in_gum.is_agree = serializer.data['is_agree']
        coach_in_gum.save()
        if serializer.data['is_agree']:
            return Response(data={'message': f'заявка на вступение в зал {pk} принята'},
                            status=status.HTTP_200_OK)
        return Response(data={'message': f'заявка на вступление в зал {pk} осталась неизменной'},
                        status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})
        try:
            coach_in_gum = CoachInGum.objects.get(gum_id=pk, coach_id=request.user.id, is_agree=False)
        except:
            return Response(data={'error': f'приглашения в зал {pk} не существует'},
                            status=status.HTTP_400_BAD_REQUEST)
        coach_in_gum.delete()
        return Response(data={'message': f'приглашение из зала {pk} отклонено'},
                        status=status.HTTP_204_NO_CONTENT)

