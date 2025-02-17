from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from .models import Hashtag

# Create your views here.

@login_required
def hashtag_list(request):
    """Lista todas as hashtags"""
    hashtags = Hashtag.objects.annotate(
        total_posts=Count('posts')
    ).order_by('-total_posts')
    
    paginator = Paginator(hashtags, 20)
    page = request.GET.get('page')
    hashtags = paginator.get_page(page)
    
    return render(request, 'hashtags/hashtag_list.html', {
        'hashtags': hashtags
    })

@login_required
def hashtag_detail(request, name):
    """Mostra detalhes de uma hashtag específica"""
    hashtag = get_object_or_404(Hashtag, name=name)
    posts = hashtag.posts.select_related('author').order_by('-created_at')
    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, 'hashtags/hashtag_detail.html', {
        'hashtag': hashtag,
        'posts': posts
    })

def get_trending_hashtags():
    """Retorna as hashtags mais usadas nos últimos 7 dias"""
    seven_days_ago = timezone.now() - timedelta(days=7)
    return Hashtag.objects.filter(
        posts__created_at__gte=seven_days_ago,
        is_trending=True
    ).annotate(
        total_posts=Count('posts')
    ).order_by('-total_posts')[:5]
