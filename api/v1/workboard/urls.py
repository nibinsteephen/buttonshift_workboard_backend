from django.urls import path, re_path
from api.v1.workboard import views

app_name = 'api_v1_workboard'

urlpatterns = [
    re_path(r'^login/$',views.user_login,name="user_login"),
    re_path(r'^Workboards/$',views.Workboards,name="Workboards"),
]