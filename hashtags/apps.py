from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class HashtagsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hashtags'
    verbose_name = _('hashtags')
