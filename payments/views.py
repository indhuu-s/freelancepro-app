import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from projects.models import Project
from .models import Transaction

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_checkout_session(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.user != project.client:
        messages.error(request, 'Only the client can make payments for this project!')
        return redirect('project_detail', project_id=project.id)
    
    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': project.title,
                            'description': f'Payment for project: {project.title}',
                        },
                        'unit_amount': int(project.total_amount * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('payment_success', args=[project.id])),
                cancel_url=request.build_absolute_uri(reverse('payment_cancel', args=[project.id])),
                metadata={
                    'project_id': project.id,
                    'user_id': request.user.id,
                }
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            messages.error(request, f'Payment error: {str(e)}')
            return redirect('project_detail', project_id=project.id)
    
    return render(request, 'create_payment.html', {'project': project})

@login_required
def payment_success(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    Transaction.objects.create(
        project=project,
        amount=project.total_amount,
        status='completed',
        is_escrow=True
    )
    
    messages.success(request, 'Payment successful! Funds are held in escrow.')
    return render(request, 'payment_success.html', {'project': project})

@login_required
def payment_cancel(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    messages.warning(request, 'Payment was cancelled.')
    return render(request, 'payment_cancel.html', {'project': project})