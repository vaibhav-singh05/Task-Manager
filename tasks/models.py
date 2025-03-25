from django.contrib.auth.models import User  
from django.db import models  

# Task model to store task details
class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    # Task status with choices
    status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pending'), ('completed', 'Completed')], 
        default='pending'
    )  
    # Many-to-Many relation: A task can be assigned to multiple users
    assigned_users = models.ManyToManyField(User, related_name='tasks')  

    def __str__(self):
        return self.name  # Return task name as string representation
