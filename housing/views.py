from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from django.db.models import Count


# ModelViewSet предоставляет полный набор стандартных действий для модели,
# включая создание, чтение, обновление и удаление CRUDՅ. Он объединяет
# функциональность всех миксинов: CreateModelMixin, RetrieveModelMixin,
# UpdateModelMixin, DestroyModelMixin, и ListModelMixin
class HousingViewSet(viewsets.ModelViewSet):
    queryset = Housing.objects.all()
    serializer_class = HousingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # извлечение текущего аутентифицированного пользователя
        return Housing.objects.filter(owner=self.request.user)


