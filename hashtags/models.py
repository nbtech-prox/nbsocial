from django.db import models
from django.utils.translation import gettext_lazy as _

class Hashtag(models.Model):
    """Modelo para hashtags"""
    name = models.CharField(_('nome'), max_length=100, unique=True)
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
    description = models.TextField(_('descrição'), blank=True)
    is_trending = models.BooleanField(_('em tendência'), default=False)
    last_used = models.DateTimeField(_('último uso'), auto_now=True)
    
    class Meta:
        verbose_name = _('hashtag')
        verbose_name_plural = _('hashtags')
        ordering = ['-created_at']
    
    def __str__(self):
        return f'#{self.name}'
    
    @property
    def post_count(self):
        return self.posts.count()
    
    def update_trending_status(self):
        """Atualiza o status de tendência baseado no número de posts recentes"""
        from django.utils import timezone
        from datetime import timedelta
        
        recent_posts = self.posts.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        self.is_trending = recent_posts >= 5  # Exemplo: 5 posts em 7 dias
        self.save(update_fields=['is_trending'])
