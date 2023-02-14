from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from log.serializers import ListCreateAthleteSerializer
from log.models import Athlete
from log.service import get_gum_or_none


class CreateUpdateAthleteAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = ListCreateAthleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        gum = get_gum_or_none(request.data['gum'], request.user)
        if not gum:
            return Response(data={'error': f"нету прав на добавление атлета в зал {request.data['gum']}"})

        new_athlete = Athlete.objects.create(first_name=request.data['first_name'],
                                     last_name=request.data['last_name'],
                                     birthday=request.data['birthday'],
                                     gum=gum)
        return Response(status=status.HTTP_201_CREATED,
                        data=ListCreateAthleteSerializer(new_athlete).data)








