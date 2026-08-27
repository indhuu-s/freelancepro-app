from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.urls import path
from django.views.generic import TemplateView
from users import views as user_views
from jobs import views as job_views
from proposals import views as proposals_views
from projects import views as projects_views

urlpatterns = [
    path('admin/', user_passes_test(lambda u: u.is_superuser)(admin.site.urls)),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('jobs/', job_views.job_list, name='job_list'),
    path('jobs/post/', job_views.post_job, name='post_job'),  # 👈 ADD THIS
    path('jobs/<int:job_id>/', job_views.job_detail, name='job_detail'),
    path('proposals/submit/<int:job_id>/', proposals_views.submit_proposal, name='submit_proposal'),
    path('proposals/my/', proposals_views.my_proposals, name='my_proposals'),
    path('jobs/<int:job_id>/proposals/', proposals_views.job_proposals, name='job_proposals'),
    path('proposals/accept/<int:proposal_id>/', proposals_views.accept_proposal, name='accept_proposal'),
    path('projects/<int:project_id>/', projects_views.project_detail, name='project_detail'),
    path('dashboard/', projects_views.dashboard, name='dashboard'),
]