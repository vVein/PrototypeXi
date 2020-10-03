from rest_framework import serializers
from .models import Pipes

class PipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipes
        fields = '__all__'
