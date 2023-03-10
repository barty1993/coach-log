from django.forms import model_to_dict
from rest_framework import status
from rest_framework.generics import get_object_or_404, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

R = Response({"error": "Method DELETE not allowed"})
from rest_framework.views import APIView

from log.serializers import CreateUpdateAthleteSerializer, CreateGroupSerializer, UpdateGroupSerializer, \
    AddAthleteSerializer, DetailGroupSerializer
from log.models import Athlete, Group, Membership
from log.service import get_gum_or_none, \
    get_athlete_or_none, \
    get_kind_of_sport_or_none, \
    coach_in_gum_or_owner, get_group_or_none


class CreateUpdateAthleteAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CreateUpdateAthleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        gum = get_gum_or_none(request.data['gum'], request.user)
        if not gum:
            return Response(data={'error': f"нету прав на добавление атлета в зал {request.data['gum']}"})
        new_athlete = Athlete.objects.create(first_name=request.data['first_name'],
                                             last_name=request.data['last_name'],
                                             birthday=request.data['birthday'],
                                             gum=gum)
        return Response(status=status.HTTP_201_CREATED,
                        data=CreateUpdateAthleteSerializer(new_athlete).data)

    def put(self, request, *args, **kwargs):

        """изменить данные атлета"""

        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PUT not allowed'})
        serializer = CreateUpdateAthleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        gum = get_gum_or_none(request.data['gum'], request.user)
        if not gum:
            return Response(data={'error': 'нету прав на изменение атлета'},
                            status=status.HTTP_400_BAD_REQUEST)
        athlete = get_athlete_or_none(pk)
        if not athlete:
            return Response(data={'error': f'Невозможно изменить спортсмена {pk}'},
                            status=status.HTTP_400_BAD_REQUEST)
        athlete.first_name = serializer.data['first_name']
        athlete.last_name = serializer.data['last_name']
        athlete.birthday = serializer.data['birthday']
        athlete.gum = gum
        athlete.save()
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):

        """удалить атлета"""

        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'method DELETE not allowed'})
        athlete = get_object_or_404(Athlete, id=pk)
        gum = get_gum_or_none(athlete.gum_id, request.user)
        if not gum:
            return Response(data={'error': f'you cant delete athlete with id:{pk}'},
                            status=status.HTTP_400_BAD_REQUEST)
        athlete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddAthleteInGroup(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = AddAthleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.data['athlete_id']:
            return Response(data={'message': 'внесите id спортсменов в список'},
                            status=status.HTTP_400_BAD_REQUEST)
        group = get_group_or_none(request.data['group_id'], request.user)
        if not group:
            return Response(data={'error': f"Невозможно добавить атлета в группу{request.data['group_id']}"},
                            status=status.HTTP_400_BAD_REQUEST)

        gum_athletes_id = [athlete.id for athlete in Athlete.objects.filter(gum=group.gum)]
        membership_athletes_id = [member.athlete_id for member in Membership.objects.filter(group=group)]
        not_valid_athlete = {}
        valid_athlete = {}
        for id in request.data['athlete_id']:
            if id not in gum_athletes_id:
                not_valid_athlete[id] = f"не числится в зале {group.gum.id}"
                continue
            if id in membership_athletes_id:
                not_valid_athlete[id] = f"уже записан в группе {group.id}"
                continue
            valid = not_valid_athlete.get(id, None)
            already_save = valid_athlete.get(id, None)
            if not valid and not already_save:
                add_athlete = Membership.objects.create(group_id=request.data['group_id'],
                                                        athlete_id=id)
                valid_athlete[id] = f"Добавлен в группу {request.data['group_id']}"
        return Response(data=[{'bad': not_valid_athlete}, {'good': valid_athlete}],
                        status=status.HTTP_200_OK)


class GroupAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CreateGroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        gum = get_gum_or_none(request.data['gum_id'], request.user)
        if not gum:
            return Response(data={'error': f"Невозможно создать группу в зале {request.data['gum']}"},
                            status=status.HTTP_400_BAD_REQUEST)
        kind_of_sport = get_kind_of_sport_or_none(request.data['kind_of_sport_id'])
        if not kind_of_sport:
            return Response(data={'error': f"Вида спорта {request.data['kind_of_sport_id']} не существует"},
                            status=status.HTTP_400_BAD_REQUEST)
        if not coach_in_gum_or_owner(gum, request.data['coach_id']):
            return Response(data={'error': f"Тренер {request.data['coach_id']} не числится в зале {gum.id}"},
                            status=status.HTTP_400_BAD_REQUEST)
        new_group = Group.objects.create(title=request.data['title'],
                                         gum_id=int(request.data['gum_id']),
                                         coach_id=int(request.data['coach_id']),
                                         kind_of_sport_id=int(request.data['kind_of_sport_id']))
        return Response(data=model_to_dict(new_group),
                        status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response(data={'error': 'Method PUT not allowed'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UpdateGroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = get_group_or_none(pk, request.user)
        if not group:
            return Response(data={'error': f"Вы не можете изменить группу {pk}"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not coach_in_gum_or_owner(group.gum, request.data['coach_id']):
            return Response(data={'error': f"Тренер {request.data['coach_id']} не числится в зале {group.gum_id}"},
                            status=status.HTTP_400_BAD_REQUEST)

        group.title = request.data['title']
        group.coach_id = int(request.data['coach_id'])
        group.save()

        return Response(data=model_to_dict(group),
                        status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """удалить группу"""
        pk = kwargs.get('pk', None)
        if not pk:
            return Response(data={'error': 'Method DELETE not allowed'},
                            status=status.HTTP_400_BAD_REQUEST)
        group = get_group_or_none(pk, request.user)
        if not group:
            return Response(data={'error': f"Вы не можете удалить группу {pk}"},
                            status=status.HTTP_400_BAD_REQUEST)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DetailGroupAPIView(RetrieveAPIView):
    queryset = Group.objects.all().select_related('kind_of_sport', 'coach')
    permission_classes = (IsAuthenticated,)
    serializer_class = DetailGroupSerializer

