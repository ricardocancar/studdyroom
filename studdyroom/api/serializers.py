from rest_framework import serializers
from base.models import Room

class roomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'