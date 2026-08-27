from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import Job

def job_list(request):
    jobs = Job.objects.all().order_by('-created_at')
    
    search_query = request.GET.get('search')
    if search_query:
        jobs = jobs.filter(
            models.Q(title__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(skills_required__icontains=search_query)
        )
    
    return render(request, 'job_list.html', {'jobs': jobs})

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job_detail.html', {'job': job})

@login_required
def post_job(request):
    if request.user.user_type not in ['client', 'both']:
        messages.error(request, 'Only clients can post jobs!')
        return redirect('home')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        budget_min = request.POST.get('budget_min')
        budget_max = request.POST.get('budget_max')
        deadline = request.POST.get('deadline')
        skills = request.POST.get('skills')
        
        job = Job.objects.create(
            client=request.user,
            title=title,
            description=description,
            budget_min=budget_min,
            budget_max=budget_max,
            deadline=deadline,
            skills_required=skills.split(','),
            status='open'
        )
        messages.success(request, 'Job posted successfully!')
        return redirect('job_detail', job_id=job.id)
    
    return render(request, 'post_job.html')