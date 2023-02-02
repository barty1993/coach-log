from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import AllowAny

from gum.models import Gum
from gum.serializers import GumListSerializer


class ListGumAPIView(generics.ListAPIView):
    queryset = Gum.objects.all()
    serializer_class = GumListSerializer
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ['city__name', 'kind_of_sport__name', ]

    def get_queryset(self):
        queryset = Gum.objects.all().prefetch_related('kind_of_sport').prefetch_related('city').select_related('owner')
        return queryset



