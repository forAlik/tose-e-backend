from rest_framework import serializers
from .models import Subnews

class SubnewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subnews
        fields = '__all__'