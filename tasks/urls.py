from django.urls import path, include  
from rest_framework.routers import DefaultRouter  
from . import views

# Creating a router for ViewSets
router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename="tasks")  # API endpoint for Task operations
router.register(r'users', views.UserViewSet)  # API endpoint for User operations

# Defining URL patterns
urlpatterns = [
    path('api/', include(router.urls)),  # Including API routes from router
    path('', views.task_list, name='task_list'),  # Displays the list of tasks
    path('add/', views.add_task, name='add_task'),  # Adds a new task
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),  # Deletes a task by ID
    path('details', views.details, name='details'),  # Displays task details
]
