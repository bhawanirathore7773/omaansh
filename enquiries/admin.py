from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(ModelAdmin):
    list_display = ['name', 'phone', 'city', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'city']
    search_fields = ['name', 'phone', 'email', 'city']
    readonly_fields = ['created_at', 'updated_at', 'product', 'name', 'phone', 'email', 'city', 'message']
    
    fieldsets = (
        ('Enquiry Details', {
            'fields': ('name', 'phone', 'email', 'city', 'product')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Admin Notes', {
            'fields': ('status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Allow deletion only for superusers
        return request.user.is_superuser
