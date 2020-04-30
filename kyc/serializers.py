from rest_framework import serializers
from .models import Input, Output


class InputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Input
        fields = '__all__'


class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output
        exclude = ['input', 'id']
