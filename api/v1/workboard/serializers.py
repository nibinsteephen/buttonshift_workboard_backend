from rest_framework import serializers

from django.contrib.auth.models import User

from workboard.models import Workboard

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserDetailsSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",          
            "full_name",
        )
        
    def get_full_name(self, instance):
        if (instance.last_name):    
            name = instance.first_name+' '+instance.last_name
        else:
            name = instance.first_name

        return name