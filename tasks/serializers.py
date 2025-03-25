from rest_framework import serializers  
from django.contrib.auth.models import User  
from .models import Task  

# Serializer for the Task model
class TaskSerializer(serializers.ModelSerializer):
    # Allows assigning multiple users to a task using their primary keys
    assigned_users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Task
        fields = '__all__'  # Includes all fields from the Task model

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    # Includes the related tasks assigned to the user (read-only)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'tasks']  # Fields to be serialized
