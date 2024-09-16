import requests
import json

from workboard.models import Workboard,Task
from .serializers import LoginSerializer, UserDetailsSerializer
from django.contrib.auth.models import User

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
                            'data': {
                                'title': 'Success',
                                'response': response.json(),
                                'user-details' : serializers.data,

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