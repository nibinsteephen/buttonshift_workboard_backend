from django.contrib import admin
from workboard.models import Workboard, Task

# Register your models here.
@admin.register(Workboard)
class WorkboardAdmin(admin.ModelAdmin):
    list_display = ('title','description','is_deleted','created_by')
    search_fields = ('title','description')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','description','workboard','is_deleted','created_by')
    search_fields = ('title','description')
