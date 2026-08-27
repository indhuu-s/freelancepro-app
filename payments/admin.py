from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('project', 'amount', 'status', 'is_escrow', 'created_at')
    list_filter = ('status', 'is_escrow', 'created_at')
    search_fields = ('project__title', 'stripe_payment_intent_id')