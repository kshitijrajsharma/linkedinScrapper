from rest_framework import serializers
from .models import *

class ScrapperprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = scrapperprofile
        fields = "__all__"