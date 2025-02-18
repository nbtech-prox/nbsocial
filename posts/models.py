from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import re
from hashtags.models import Hashtag

class Post(models.Model):
    """Modelo para posts da rede social"""
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('autor')
    )
    content = models.TextField(_('conteúdo'))
    image = models.ImageField(_('imagem'), upload_to='posts/images/', blank=True, null=True)
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('atualizado em'), auto_now=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Like',
        related_name='liked_posts',
        verbose_name=_('gostos')
    )
    hashtags = models.ManyToManyField(
        'hashtags.Hashtag',
        related_name='posts',
        blank=True,
        verbose_name=_('hashtags')
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('publicação')
        verbose_name_plural = _('publicações')
    
    def __str__(self):
        return f'{self.author.username} - {self.created_at.strftime("%d/%m/%Y %H:%M")}'
    
    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Só processa hashtags automaticamente se for uma nova postagem
        # e se não houver hashtags já definidas (evita processamento duplo)
        if is_new and not self.hashtags.exists():
            self.process_hashtags()
    
    def process_hashtags(self):
        """Processa hashtags do conteúdo do post"""
        # Encontra todas as hashtags no conteúdo
        hashtag_pattern = re.compile(r'#(\w+)')
        hashtag_matches = hashtag_pattern.finditer(self.content)
        
        # Para cada hashtag encontrada
        for match in hashtag_matches:
            hashtag_name = match.group(1)
            if hashtag_name:
                # Cria ou obtém a hashtag
                hashtag, _ = Hashtag.objects.get_or_create(name=hashtag_name)
                # Adiciona ao post
                self.hashtags.add(hashtag)
    
    def extract_mentions(self):
        """Extrai menções (@username) do conteúdo do post"""
        mention_pattern = re.compile(r'@(\w+)')
        mention_matches = mention_pattern.finditer(self.content)
        return {match.group(1) for match in mention_matches}

    @property
    def liked_by_user(self):
        """Verifica se o post foi curtido pelo usuário atual"""
        return hasattr(self, '_liked_by_user') and self._liked_by_user

    @liked_by_user.setter
    def liked_by_user(self, value):
        """Define se o post foi curtido pelo usuário atual"""
        self._liked_by_user = value

    @property
    def likes_count(self):
        """Retorna o número de curtidas do post"""
        return self.likes.count()
    
    @likes_count.setter
    def likes_count(self, value):
        """Define o número de curtidas do post (apenas para compatibilidade)"""
        pass  # Não faz nada, apenas para evitar o erro

    @property
    def comments_count(self):
        """Retorna o número de comentários do post"""
        return self.comments.count()
    
    @comments_count.setter
    def comments_count(self, value):
        """Define o número de comentários do post (apenas para compatibilidade)"""
        pass  # Não faz nada, apenas para evitar o erro

class Comment(models.Model):
    """Modelo para comentários em posts"""
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('publicação')
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('autor')
    )
    content = models.TextField(_('conteúdo'))
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('atualizado em'), auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = _('comentário')
        verbose_name_plural = _('comentários')
    
    def __str__(self):
        return f'Comentário de {self.author.username} em {self.post}'

class Like(models.Model):
    """Modelo para likes em posts"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name=_('usuário')
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_likes',
        verbose_name=_('publicação')
    )
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('curtida')
        verbose_name_plural = _('curtidas')
        unique_together = ['user', 'post']
    
    def __str__(self):
        return f'{self.user.username} curtiu {self.post}'

class Hashtag(models.Model):
    """Modelo para hashtags"""
    name = models.CharField(_('nome'), max_length=100, unique=True)
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('hashtag')
        verbose_name_plural = _('hashtags')
        ordering = ['-created_at']
    
    def __str__(self):
        return f'#{self.name}'
    
    @property
    def post_count(self):
        return self.posts.count()

class Report(models.Model):
    """Modelo para denúncias de conteúdo"""
    
    REPORT_TYPES = [
        ('spam', _('Spam')),
        ('inappropriate', _('Conteúdo Inapropriado')),
        ('harassment', _('Assédio')),
        ('other', _('Outro')),
    ]
    
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_made',
        verbose_name=_('denunciante')
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name=_('publicação')
    )
    report_type = models.CharField(
        _('tipo de denúncia'),
        max_length=20,
        choices=REPORT_TYPES
    )
    description = models.TextField(_('descrição'))
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
    resolved = models.BooleanField(_('resolvido'), default=False)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports_resolved',
        verbose_name=_('resolvido por')
    )
    resolution_note = models.TextField(_('nota de resolução'), blank=True)
    
    class Meta:
        verbose_name = _('denúncia')
        verbose_name_plural = _('denúncias')
    
    def __str__(self):
        return f'Denúncia de {self.reporter.username} - {self.get_report_type_display()}'
