from .views import get_trending_hashtags

def trending_hashtags(request):
    """Adiciona hashtags em tendência ao contexto global"""
    return {
        'trending_hashtags': get_trending_hashtags()
    }
