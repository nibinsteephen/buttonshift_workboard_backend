import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.

TASK_STATUS_CHOICES = (
    ('to_do','To Do'),
    ('in_progress','In Progress'),
    ('completed','Completed'),
)

class Workboard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    
    class Meta:
        db_table = 'workboard_workboard'
        verbose_name = _('Workboard')
        verbose_name_plural = _('Workboards')
        ordering = ('title',)

    def __str__(self):
        return self.title
    
class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    is_deleted = models.BooleanField(default=False)
    workboard = models.ForeignKey(Workboard,on_delete=models.CASCADE,null=True,blank=True)
    assigned_to = models.ManyToManyField(User,blank=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True, related_name='created_by')
    status = models.CharField(choices=TASK_STATUS_CHOICES,max_length=200,null=True,blank=True)
    
    class Meta:
        db_table = 'workboard_task'
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ('title',)

    def __str__(self):
        return self.title