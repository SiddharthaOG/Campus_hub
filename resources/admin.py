from django.contrib import admin
from .models import Resource, Comment


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'branch', 'subject', 'semester', 'resource_type', 'download_count', 'is_featured', 'created_at')
    list_filter = ('branch', 'semester', 'resource_type', 'is_featured')
    search_fields = ('title', 'description', 'subject', 'tags')
    date_hierarchy = 'created_at'
    list_select_related = True
    actions = ['mark_as_featured']

    @admin.action(description='Mark selected resources as featured')
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} resource(s) marked as featured.')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'resource', 'created_at')
    list_filter = ('created_at', 'resource')
    search_fields = ('author_name', 'body', 'resource__title')
    readonly_fields = ('created_at',)