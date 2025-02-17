from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Post, Comment, Like, Report

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content_preview', 'created_at', 'likes_count', 'comments_count')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username')
    ordering = ('-created_at',)
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = _('Conteúdo')
    
    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = _('Gostos')
    
    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = _('Comentários')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'post__content')
    ordering = ('-created_at',)
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = _('Conteúdo')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__content')
    ordering = ('-created_at',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'post', 'report_type', 'created_at', 'resolved', 'resolved_by')
    list_filter = ('report_type', 'resolved', 'created_at')
    search_fields = ('reporter__username', 'post__content', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('reporter', 'post', 'report_type', 'description', 'created_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(resolved=False)
