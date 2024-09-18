from django.urls import path, re_path
from api.v1.workboard import views

app_name = 'api_v1_workboard'

urlpatterns = [
    re_path(r'^login/$',views.user_login,name="user_login"),
    re_path(r'^workboards/$',views.Workboards,name="Workboards"),
    re_path(r'^workboard-details/(?P<workboard_id>.*)/$',views.workboard_details,name="workboard_details"),
    re_path(r'^workboard-tasks/(?P<workboard_id>.*)/$',views.workboard_tasks,name="workboard_tasks"),
    re_path(r'^create-workboard/$',views.create_workboard,name="create_workboard"),
    re_path(r'^assign-users-list/$',views.assign_users_list,name="assign_users_list"),
    re_path(r'^add-task/$',views.add_task,name="add_task"),
    re_path(r'^edit-task/$',views.edit_task,name="edit_task"),
]