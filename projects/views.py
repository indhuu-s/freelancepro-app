from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Task

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Check if user is part of this project
    if request.user not in [project.client, project.freelancer]:
        messages.error(request, 'You are not authorized to view this project!')
        return redirect('home')
    
    # Handle task creation
    if request.method == 'POST' and 'add_task' in request.POST:
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')
        
        Task.objects.create(
            project=project,
            assigned_to=request.user,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date
        )
        messages.success(request, 'Task added successfully!')
        return redirect('project_detail', project_id=project.id)
    
    tasks = project.tasks.all()
    return render(request, 'project_detail.html', {'project': project, 'tasks': tasks})

@login_required
def dashboard(request):
    client_projects = Project.objects.filter(client=request.user)
    freelancer_projects = Project.objects.filter(freelancer=request.user)
    
    # For tasks count
    total_tasks = Task.objects.filter(project__in=client_projects) | Task.objects.filter(project__in=freelancer_projects)
    
    context = {
        'client_projects': client_projects,
        'freelancer_projects': freelancer_projects,
        'total_tasks': total_tasks.count(),
        'active_projects': client_projects.filter(status='active').count() + freelancer_projects.filter(status='active').count(),
    }
    return render(request, 'dashboard.html', context)