from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jobs.models import Job
from .models import Proposal

@login_required
def submit_proposal(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Check if user is a freelancer or both
    if request.user.user_type not in ['freelancer', 'both']:
        messages.error(request, 'Only freelancers can submit proposals!')
        return redirect('job_detail', job_id=job.id)
    
    # Check if already applied
    if Proposal.objects.filter(job=job, freelancer=request.user).exists():
        messages.error(request, 'You already submitted a proposal for this job!')
        return redirect('job_detail', job_id=job.id)
    
    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter')
        bid_amount = request.POST.get('bid_amount')
        estimated_days = request.POST.get('estimated_days')
        
        Proposal.objects.create(
            job=job,
            freelancer=request.user,
            cover_letter=cover_letter,
            bid_amount=bid_amount,
            estimated_days=estimated_days
        )
        messages.success(request, 'Proposal submitted successfully!')
        return redirect('job_detail', job_id=job.id)
    
    return render(request, 'submit_proposal.html', {'job': job})
@login_required
def job_proposals(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Check if the logged-in user is the client who posted the job
    if request.user != job.client:
        messages.error(request, 'You are not authorized to view these proposals!')
        return redirect('job_detail', job_id=job.id)
    
    proposals = Proposal.objects.filter(job=job).order_by('-created_at')
    return render(request, 'job_proposals.html', {'job': job, 'proposals': proposals})

@login_required
def my_proposals(request):
    proposals = Proposal.objects.filter(freelancer=request.user).order_by('-created_at')
    return render(request, 'my_proposals.html', {'proposals': proposals})
@login_required
def accept_proposal(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    
    # Check if user is the client who posted the job
    if request.user != proposal.job.client:
        messages.error(request, 'You are not authorized to accept this proposal!')
        return redirect('job_detail', job_id=proposal.job.id)
    
    # Update proposal status
    proposal.status = 'accepted'
    proposal.save()
    
    # Update job status
    job = proposal.job
    job.status = 'in_progress'
    job.hired_freelancer = proposal.freelancer
    job.save()
    
    # Create Project
    from projects.models import Project
    project = Project.objects.create(
        job=job,
        client=job.client,
        freelancer=proposal.freelancer,
        title=job.title,
        description=job.description,
        total_amount=proposal.bid_amount,
        status='active'
    )
    
    messages.success(request, f'Proposal accepted! Project "{project.title}" created successfully!')
    return redirect('project_detail', project_id=project.id)