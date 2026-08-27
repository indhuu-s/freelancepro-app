from django.contrib import admin
from .models import Project, Task, Milestone

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'freelancer', 'status', 'total_amount', 'start_date')
    list_filter = ('status', 'start_date')
    search_fields = ('title', 'client__username', 'freelancer__username')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'status', 'priority', 'due_date')
    list_filter = ('status', 'priority', 'due_date')
    search_fields = ('title', 'description', 'project__title')

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'amount', 'is_completed', 'payment_released', 'due_date')
    list_filter = ('is_completed', 'payment_released', 'due_date')
    search_fields = ('title', 'description', 'project__title')