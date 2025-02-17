from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext as _
from posts.models import Post, Comment, Like
from users.models import CustomUser, UserFollowing
from .models import Notification

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """Cria uma notificação quando um comentário é feito em um post"""
    if created and instance.author != instance.post.author:
        Notification.objects.create(
            recipient=instance.post.author,
            sender=instance.author,
            notification_type='comment',
            text=_('comentou na sua publicação'),
            post=instance.post
        )

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    """Cria uma notificação quando alguém curte um post"""
    if created and instance.user != instance.post.author:
        Notification.objects.create(
            recipient=instance.post.author,
            sender=instance.user,
            notification_type='like',
            text=_('gostou da sua publicação'),
            post=instance.post
        )

@receiver(post_save, sender=UserFollowing)
def create_follow_notification(sender, instance, created, **kwargs):
    """Cria uma notificação quando um usuário começa a seguir outro"""
    if created:
        Notification.objects.create(
            recipient=instance.following_user,
            sender=instance.user,
            notification_type='follow',
            text=_('começou a seguir você')
        )

@receiver(post_delete, sender=UserFollowing)
def delete_follow_notification(sender, instance, **kwargs):
    """Remove a notificação quando um usuário deixa de seguir outro"""
    Notification.objects.filter(
        recipient=instance.following_user,
        sender=instance.user,
        notification_type='follow',
        text=_('começou a seguir você')
    ).delete()

@receiver(post_save, sender=Post)
def create_mention_notification(sender, instance, created, **kwargs):
    """Cria notificações para usuários mencionados em um post"""
    if created:
        mentions = instance.extract_mentions()
        for username in mentions:
            try:
                mentioned_user = CustomUser.objects.get(username=username)
                if mentioned_user != instance.author:
                    Notification.objects.create(
                        recipient=mentioned_user,
                        sender=instance.author,
                        notification_type='mention',
                        text=_('mencionou você em uma publicação'),
                        post=instance
                    )
            except CustomUser.DoesNotExist:
                pass
