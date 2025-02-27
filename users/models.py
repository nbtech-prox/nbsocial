from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import os
from PIL import Image

def validate_avatar(value):
    """Validar dimensões e tipo do arquivo de avatar"""
    if value:
        # Validar extensão do arquivo
        ext = os.path.splitext(value.name)[1].lower()
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        if ext not in valid_extensions:
            raise ValidationError(_('Por favor, envie uma imagem válida. Os formatos permitidos são: JPG, JPEG, PNG e GIF.'))
        
        try:
            # Abrir a imagem para validar
            img = Image.open(value)
            img.verify()  # Verificar se é uma imagem válida
            
            # Reabrir a imagem após verify() pois ele fecha o arquivo
            img = Image.open(value)
            
            # Validar tamanho do arquivo
            if value.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError(_('A imagem deve ter no máximo 5MB.'))
            
            # Validar dimensões
            width, height = img.size
            if width < 100 or height < 100:
                raise ValidationError(_('A imagem deve ter no mínimo 100x100 pixels.'))
            if width > 2000 or height > 2000:
                raise ValidationError(_('A imagem deve ter no máximo 2000x2000 pixels.'))
                
        except Exception as e:
            raise ValidationError(_('O arquivo enviado não é uma imagem válida.'))

class CustomUser(AbstractUser):
    """Modelo de usuário personalizado com campos adicionais"""
    
    ROLE_CHOICES = [
        ('user', _('Utilizador')),
        ('moderator', _('Moderador')),
        ('admin', _('Administrador')),
    ]
    
    email = models.EmailField(_('endereço de email'), unique=True)
    avatar = models.ImageField(_('foto de perfil'), 
                             upload_to='avatars/', 
                             null=True, 
                             blank=True,
                             validators=[validate_avatar])
    bio = models.TextField(_('biografia'), max_length=500, blank=True)
    location = models.CharField(_('localização'), max_length=100, blank=True)
    birth_date = models.DateField(_('data de nascimento'), null=True, blank=True)
    role = models.CharField(_('função'), max_length=10, choices=ROLE_CHOICES, default='user')
    facebook = models.URLField(_('perfil do Facebook'), max_length=200, blank=True)
    instagram = models.URLField(_('perfil do Instagram'), max_length=200, blank=True)
    tiktok = models.URLField(_('perfil do TikTok'), max_length=200, blank=True)
    github = models.URLField(_('perfil do GitHub'), max_length=200, blank=True)

    class Meta:
        verbose_name = _('utilizador')
        verbose_name_plural = _('utilizadores')

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role in ['moderator', 'admin']
    
    @property
    def is_admin(self):
        return self.role == 'admin'

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return f"Perfil de {self.user.username}"


class UserFollowing(models.Model):
    """Modelo para representar os relacionamentos de seguidor/seguido"""
    user = models.ForeignKey(CustomUser, related_name='following_relationships', on_delete=models.CASCADE)
    following_user = models.ForeignKey(CustomUser, related_name='follower_relationships', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'following_user')
        
    def __str__(self):
        return f"{self.user.username} segue {self.following_user.username}"
