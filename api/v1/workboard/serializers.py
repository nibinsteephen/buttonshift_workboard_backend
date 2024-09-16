from rest_framework import serializers

from django.contrib.auth.models import User

from workboard.models import Workboard,Task

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
    
class workboardSerializer(serializers.ModelSerializer):
    users_list = serializers.SerializerMethodField()
    class Meta:
        model = Workboard
        fields = (
            'id',
            'title',
            'users_list'
        )
        
    def get_users_list(self, instance):
        users_list = []
        users_name = []
        
        tasks = Task.objects.filter(workboard=instance)
        users_from_tasks = User.objects.filter(task__in=tasks).distinct()
        
        for user in users_from_tasks:
            users_list.append(user)
        if instance.created_by and instance.created_by not in users_list:
            users_list.append(instance.created_by)
        
        if users_list:
            for user in users_list:
                users_name.append(user.get_full_name())
                
        return users_name