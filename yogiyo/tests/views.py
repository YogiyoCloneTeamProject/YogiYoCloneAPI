from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from tests.models import Test
from tests.serializers import TestSerializer


class TestViewSet(ModelViewSet):
    serializer_class = TestSerializer
    queryset = Test.objects.all()
