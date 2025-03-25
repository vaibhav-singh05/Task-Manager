from django.contrib import admin  
from .models import Task  

# Register Task model in the admin panel
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'created_at')  # Display fields in the admin list view
    list_filter = ('status',)  # Enable filtering by status
    search_fields = ('name', 'description')  # Enable search by name and description
