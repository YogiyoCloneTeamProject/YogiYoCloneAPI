from rest_framework.serializers import ModelSerializer

from tests.models import Test


class TestSerializer(ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'age')
        model = Test
