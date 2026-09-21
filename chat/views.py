from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from projects.models import Project
from .models import Message

@login_required
def project_chat(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Only client & freelancer allowed
    if request.user not in [project.client, project.freelancer]:
        messages.error(request, "You are not allowed in this chat.")
        return redirect('dashboard')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=project.freelancer if request.user == project.client else project.client,
                project=project,
                content=content
            )
        return redirect('project_chat', project_id=project.id)

    chat_messages = Message.objects.filter(project=project).order_by('created_at')

    return render(request, 'project_chat.html', {
        'project': project,
        'chat_messages': chat_messages
    })