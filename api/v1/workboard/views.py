import requests
import json

from django.db.models import Q

from django.contrib.auth.models import User

from workboard.models import Workboard,Task
from .serializers import LoginSerializer, UserDetailsSerializer, workboardSerializer, CreateWorkboardSerializer, AddTaskSerializer


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
    view for user_login
    """
    serialized_data = LoginSerializer(data=request.data)
    
    if serialized_data.is_valid():
        username = request.data.get('username')
        password = request.data.get('password')
        
        if User.objects.filter(username=username).exists():
            user_profile = User.objects.get(username=username)
            serializers = UserDetailsSerializer(user_profile, context={'request': request})
            
            if user_profile.check_password(password):
            
                headers = {"Content-Type": "application/json"}

                protocol = "http://"
                if request.is_secure():
                    protocol = "https://"

                web_host = request.get_host()
                request_url = protocol + web_host + "/workboard/token/"

                data = {
                    'username': username,
                    'password': password,
                }

                print(data,"-------------------------------------")
                
                response = requests.post(request_url, headers=headers, data=json.dumps(data))
                print(response,"+++++++++++++++++++++++++++++++++++++")
                
                if response.status_code == 200:
                        response_data = {
                            'StatusCode': 6000,
                            'message': 'Login Success',
                            'data': {
                                'title': 'Success',
                                'response': response.json(),
                                'userDetails' : serializers.data,
                            }
                        }
                else:
                    response_data = {
                        "StatusCode": 6001,
                        "message": "Token Generation Failed",
                    }   
            else:
                response_data = {
                    "StatusCode": 6001,
                    "message": "Password does not match",
                }      
        else:
            response_data = {
                "StatusCode": 6001,
                "message": "User does not exist",
            }
    else:
        response_data = {
            "StatusCode": 6001,
            "message": "Enter valid data",
            "data": serialized_data.errors
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Workboards(request):
    """
    views for showing all workboard wither created by the user of assigned to the user
    """
    current_user = request.user
    if Workboard.objects.filter(Q(created_by=current_user) | Q(task__assigned_to=current_user)).distinct().exists():
        user_workboard = Workboard.objects.filter(Q(created_by=current_user) | Q(task__assigned_to=current_user)).distinct()
        serialized_data = workboardSerializer(user_workboard, many=True, context={'request': request})
        
        response_data = {
            "StatusCode": 6000,
            "data": {
                'title': 'Success',
                'workboard': serialized_data.data,
            }
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "message": "Workboard does not exist",
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def workboard_tasks(request,workboard_id):
    """
    views for showing tasks of each workboard
    """

    if Task.objects.filter(workboard__id=workboard_id,is_deleted=False).exists():
        task = Task.objects.filter(workboard__id=workboard_id,is_deleted=False)
        serialized_data = AddTaskSerializer(task, many=True, context={'request': request})
        
        response_data = {
            "StatusCode": 6000,
            "data": {
                'title': 'Success',
                'tasks': serialized_data.data,
            }
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "message": "No task found",
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def create_workboard(request):
    """
    view for creating a workboard including task
    """
    
    current_user = request.user
    serialized_data = CreateWorkboardSerializer(data=request.data)
    
    if serialized_data.is_valid():
        title = request.data.get('title')
        description = request.data.get('description')
        tasks = request.data.get('tasks')
        
        if isinstance(tasks, str):
            tasks = json.loads(tasks)
        
        new_workboard = Workboard.objects.create(
            title = title,
            description = description,
            created_by = current_user
        )
       
        if tasks:
            for task in tasks:           
                new_task = Task.objects.create(
                    title = task['title'],
                    description = task['description'],
                    workboard = new_workboard,
                    created_by = current_user,
                    status = task.get('status', None)  
                )

                assigned_users = task.get('assigned_to',[])
                if assigned_users:
                    user_ids = [user['id'] for user in assigned_users]
                    user_objects = User.objects.filter(id__in=user_ids)
                    new_task.assigned_to.add(*user_objects)
                    
                new_task.save()
                
        response_data = {
            'StatusCode': 6000,
            'data': {
                'title': 'Success',
                'message': 'Workboard created successfully',
            }
        }
    else:
        response_data = {
            'StatusCode': 6001,
            'message': 'Invalid data',
            'data': serialized_data.errors
        }
    return Response(response_data, status=status.HTTP_200_OK)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def assign_users_list(request):
    """
    view for getting list of users
    """
    if User.objects.all().exclude(is_superuser=True).exists():
        
        users = User.objects.all().exclude(is_superuser=True).order_by('first_name')
        serialized_data = UserDetailsSerializer(users, many=True)

        response_data = {
            'StatusCode': 6000,
            'data': {
                'title': 'Success',
                'data': serialized_data.data
            }
        }
    else:
        response_data = {
            'StatusCode': 6001,
            'message': 'Users does not exist',
        }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_task(request):
    """
    view for adding task in workboard page
    """
    current_user = request.user
    
    serialized_data = AddTaskSerializer(data=request.data)
    
    if serialized_data.is_valid():
    
        title = request.data.get('title')
        description = request.data.get('description')
        workboard_id = request.data.get('workboard_id')
        assigned_to = request.data.get('assigned_to')
        task_status = request.data.get('status')
        
        if isinstance(assigned_to, str):
                assigned_to = json.loads(assigned_to)
                
        if workboard_id:
            if Workboard.objects.filter(pk=workboard_id).exists():
                workboard = Workboard.objects.get(pk=workboard_id)
            else:
                workboard = None
        
            new_task = Task.objects.create(
                title = title,
                description = description,
                workboard = workboard,
                created_by = current_user,
                status = task_status
            )
        
            if assigned_to:
                user_ids = [user['id'] for user in assigned_to]
                user_objects = User.objects.filter(id__in=user_ids)
                new_task.assigned_to.add(*user_objects)
        
            new_task.save()
            
            response_data = {
                'StatusCode': 6000,
                'data': {
                    'title': 'Success',
                    'message': 'Task created successfully',
                }
            }
        else:
            response_data ={
                'StatusCode': 6001,
                'message': 'Workboard does not exist',
            }
    else:
        response_data = {
            'StatusCode': 6001,
            'message': 'Invalid data',
            'data': serialized_data.errors
        }
        
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_task(request):
    """
    view for adding task in workboard page
    """
    
    task_id = request.data.get('task_id')
    print(task_id,"TASKKKK ID")
    
    if Task.objects.filter(pk=task_id).exists():
        task = Task.objects.get(pk=task_id)
                    
        serializer = AddTaskSerializer(task, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.update(serializer.instance, serializer.validated_data)
            
        response_data = {
            'StatusCode': 6000,
            'data': {
                'title': 'Success',
                'message': 'Task Updated successfully',
                'data': serializer.data
            }
        }
    else:
        response_data = {
            'StatusCode': 6001,
            'message': 'Task does not exist',
        }
        
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def workboard_details(request, workboard_id):
    if Workboard.objects.filter(pk=workboard_id).exists():
        workboard = Workboard.objects.get(pk=workboard_id)
        
        response_data = {
            'StatusCode': 6000,
            'data': {
                'title': 'Success',
                'workboard_title': workboard.title,
                'workboard_description': workboard.description
            }
        }
    else:
        response_data = {
            'StatusCode': 6001,
            'message': 'Workboard does not exist',
        }
    return Response(response_data, status=status.HTTP_200_OK)