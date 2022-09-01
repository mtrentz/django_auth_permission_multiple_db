from rest_framework.serializers import ModelSerializer
from .models import SampleModel

class SampleSerializer(ModelSerializer):
    class Meta:
        model = SampleModel
        fields = ('name',)