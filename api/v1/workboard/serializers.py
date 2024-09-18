import json

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
    number_of_tasks = serializers.SerializerMethodField()
    class Meta:
        model = Workboard
        fields = (
            'id',
            'title',
            'number_of_tasks',
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
    
    def get_number_of_tasks(self, instance):
        if Task.objects.filter(workboard=instance,is_deleted=False).exists():
            task_count = Task.objects.filter(workboard=instance,is_deleted=False).count()
        else:
            task_count = 0
        return task_count
    
class CreateWorkboardSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()

class AddTaskSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(required=False)
    workboard_id = serializers.CharField()
    assigned_to = serializers.CharField()
    status = serializers.CharField()
    
    
    assigned_users_name = serializers.SerializerMethodField()
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     assigned_to_users = instance.assigned_to.values_list('id', flat=True)
    #     representation['assigned_to'] = list(assigned_to_users) 
    #     return representation
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.workboard_id = validated_data.get('workboard', instance.workboard_id)
        instance.status = validated_data.get('status', instance.status)
        
        assigned_to = validated_data.get('assigned_to')
        
        if isinstance(assigned_to, str):
            assigned_to = json.loads(assigned_to)
        if assigned_to:
            user_objects = User.objects.filter(id__in=assigned_to)
            if user_objects.exists():
                instance.assigned_to.set(user_objects)
        
        instance.save()
        return instance

    def get_assigned_users_name(self, instance):
        users_name = []
        if instance.assigned_to.exists():
            for user in instance.assigned_to.all():
                users_name.append(user.get_full_name())
        return users_name