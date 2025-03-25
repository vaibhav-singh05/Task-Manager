from django.shortcuts import render, redirect, get_object_or_404  
from rest_framework import viewsets  
from rest_framework.permissions import IsAuthenticated  
from django.contrib.auth.models import User  
from .models import Task  
from .serializers import TaskSerializer, UserSerializer
from django.http import JsonResponse

# API ViewSet for managing tasks
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users

    def get_queryset(self):
        # Filter tasks by assigned user if user_id is provided in query params
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Task.objects.filter(assigned_users__id=user_id)
        return Task.objects.all()

# API ViewSet for managing users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# View to display the task list
def task_list(request):
    tasks = Task.objects.all()
    users = User.objects.all()
    return render(request, 'tasks.html', {'tasks': tasks, 'users': users})

# View to add a new task
def add_task(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        assigned_users_ids = request.POST.getlist('assigned_users')  

        # Create a new task and assign users
        task = Task.objects.create(name=name, description=description)
        task.assigned_users.set(assigned_users_ids)  
        return redirect('task_list')

    return redirect('task_list')

# View to delete a task
def delete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)
        task.delete()
    return redirect('task_list')

# View to show task details page with optional search functionality
def details(request):
    search_query = request.GET.get('search', '')

    if 'clear' in request.GET:  
        request.session.pop('search_query', None)  # Clear search filter
        return redirect('details')

    if search_query:
        request.session['search_query'] = search_query  
        tasks = Task.objects.filter(assigned_users__username__icontains=search_query)
    else:
        search_query = request.session.get('search_query', '')
        tasks = Task.objects.filter(assigned_users__username__icontains=search_query) if search_query else Task.objects.all()

    return render(request, 'details.html', {'tasks': tasks, 'search_query': search_query})

# View to update task status
def update_task_status(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)
        new_status = request.POST.get("status")

        if new_status:
            task.status = new_status
            task.save()
            return JsonResponse({"success": True, "status": task.status})  # JSON response
        return JsonResponse({"success": False, "error": "Invalid status"})
    return JsonResponse({"success": False, "error": "Invalid request"})