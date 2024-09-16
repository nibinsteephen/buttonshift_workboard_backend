from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('workboard/', include('workboard.urls')),
    
    path('api/v1/workboard/', include('api.v1.workboard.urls', namespace="api_v1_workboard")),
]
