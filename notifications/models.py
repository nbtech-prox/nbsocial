from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Notification(models.Model):
    """Modelo para notificações"""
    NOTIFICATION_TYPES = [
        ('like', _('Gosto')),
        ('comment', _('Comentário')),
        ('follow', _('Seguir')),
        ('mention', _('Menção')),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications_received',
        verbose_name=_('destinatário')
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications_sent',
        verbose_name=_('remetente')
    )
    notification_type = models.CharField(
        _('tipo'),
        max_length=20,
        choices=NOTIFICATION_TYPES
    )
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
        verbose_name=_('publicação')
    )
    comment = models.ForeignKey(
        'posts.Comment',
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
        verbose_name=_('comentário')
    )
    text = models.CharField(_('texto'), max_length=255)
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
    read = models.BooleanField(_('lido'), default=False)
    read_at = models.DateTimeField(_('lido em'), null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('notificação')
        verbose_name_plural = _('notificações')

    def __str__(self):
        return f'{self.get_notification_type_display()} - {self.recipient.username}'

    def mark_as_read(self):
        """Marca a notificação como lida"""
        if not self.read:
            self.read = True
            self.read_at = timezone.now()
            self.save()
