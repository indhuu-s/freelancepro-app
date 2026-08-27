from django.contrib import admin
from .models import Proposal

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('job', 'freelancer', 'bid_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('job__title', 'freelancer__username', 'cover_letter')