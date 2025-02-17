from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from posts.models import Post
from users.models import CustomUser
from hashtags.models import Hashtag
from posts.views import get_trending_hashtags

def home(request):
    """Página inicial"""
    return render(request, 'core/home.html')

@login_required
def explore(request):
    """Página de exploração com busca, posts populares e usuários sugeridos"""
    query = request.GET.get('q', '')
    posts = []
    users = []
    hashtags = []
    
    if query:
        # Busca por hashtags
        hashtags = Hashtag.objects.filter(
            name__icontains=query.replace('#', '')
        ).annotate(
            total_posts=Count('posts')
        ).order_by('-total_posts')

        # Busca por posts
        posts = Post.objects.select_related('author').prefetch_related(
            'likes', 'comments', 'hashtags'
        ).filter(
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query) |
            Q(hashtags__name__icontains=query.replace('#', ''))
        ).distinct()
        
        # Busca por usuários
        users = CustomUser.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).annotate(
            followers_count=Count('followers')
        ).order_by('-followers_count')
    
    # Sempre buscar posts populares e usuários sugeridos para a sidebar
    popular_posts = Post.objects.select_related('author').prefetch_related(
        'likes', 'comments'
    ).annotate(
        interaction_count=Count('likes') + Count('comments')
    ).order_by('-interaction_count')[:10]
    
    # Usuários sugeridos (excluindo os que o usuário já segue)
    following_ids = request.user.following.values_list('id', flat=True)
    suggested_users = CustomUser.objects.exclude(
        Q(id__in=following_ids) | Q(id=request.user.id)
    ).annotate(
        followers_count=Count('followers')
    ).order_by('-followers_count')[:5]
    
    # Hashtags em tendência
    trending_hashtags = get_trending_hashtags()
    
    return render(request, 'core/explore.html', {
        'query': query,
        'posts': posts,
        'users': users,
        'hashtags': hashtags,
        'popular_posts': popular_posts,
        'suggested_users': suggested_users,
        'trending_hashtags': trending_hashtags,
    })

@login_required
def search(request):
    """Página de busca por posts e usuários"""
    query = request.GET.get('q', '')
    posts = []
    users = []
    
    if query:
        posts = Post.objects.select_related('author').filter(
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        )
        
        users = CustomUser.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    
    return render(request, 'core/search.html', {
        'query': query,
        'posts': posts,
        'users': users
    })
