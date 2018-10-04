from rest_framework import serializers

from .models import LogoEntries
class LogoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogoEntries
        fields = "__all__"