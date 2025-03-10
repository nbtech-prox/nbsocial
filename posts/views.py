from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Post, Comment, Like, Report
from .forms import PostForm, CommentForm, ReportForm
from hashtags.models import Hashtag

User = get_user_model()

@login_required
def post_list(request):
    posts_list = Post.objects.select_related(
        'author'
    ).prefetch_related(
        'likes',
        'comments',
        'hashtags'
    ).order_by('-created_at')
    
    # Marca os posts que o usuário atual curtiu
    for post in posts_list:
        post.liked_by_user = Like.objects.filter(user=request.user, post=post).exists()
        post.likes_count = post.likes.count()
    
    paginator = Paginator(posts_list, 10)  # 10 posts por página
    page = request.GET.get('page', 1)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'posts': posts,
    }
    return render(request, 'core/home.html', context)

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post.objects.prefetch_related('comments', 'likes', 'hashtags'), pk=pk)
    post.liked_by_user = Like.objects.filter(user=request.user, post=post).exists()
    post.likes_count = post.likes.count()
    
    comments = post.comments.select_related('author').order_by('created_at')
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, _('Comentário adicionado com sucesso!'))
            return redirect('posts:detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'posts/post_detail.html', context)

@login_required
def create_post(request):
    """Criar novo post"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            
            # Processa hashtags após salvar o post
            post.process_hashtags()
            
            messages.success(request, _('Publicação criada com sucesso.'))
            return redirect('core:home')
        else:
            messages.error(request, _('Erro ao criar publicação. Por favor, verifique os dados.'))
            return redirect('core:home')
    else:
        form = PostForm()
    
    return render(request, 'posts/create.html', {'form': form})

@login_required
def edit_post(request, pk):
    """Editar post existente"""
    post = get_object_or_404(Post.objects.select_related('author').prefetch_related('hashtags'), pk=pk)
    
    if post.author != request.user:
        messages.error(request, _('Você não tem permissão para editar esta publicação.'))
        return redirect('posts:detail', pk=post.pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, _('Publicação atualizada com sucesso.'))
            return redirect('posts:detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'posts/post_form.html', {'form': form, 'post': post})

@login_required
def delete_post(request, pk):
    """Deletar post"""
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, _('Você não tem permissão para excluir esta publicação.'))
        return redirect('posts:detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, _('Publicação excluída com sucesso!'))
        return redirect('posts:list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
            messages.success(request, _('Comentário adicionado com sucesso!'))
            return redirect('posts:detail', pk=post.pk)
    return redirect('posts:detail', pk=post.pk)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.author:
        post_pk = comment.post.pk
        comment.delete()
        messages.success(request, _('Comentário excluído com sucesso!'))
        return redirect('posts:detail', pk=post_pk)
    messages.error(request, _('Você não tem permissão para excluir este comentário.'))
    return redirect('posts:detail', pk=comment.post.pk)

@require_POST
@login_required
def like_post(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        like = Like.objects.filter(user=request.user, post=post).first()

        if like:
            like.delete()
            post.liked_by_user = False
        else:
            Like.objects.create(user=request.user, post=post)
            post.liked_by_user = True
        
        # Atualiza o contador de likes
        post.likes_count = post.likes.count()
        
        return render(request, 'posts/partials/post_likes.html', {'post': post})
    except Exception as e:
        print(f"Error in like_post: {str(e)}")
        raise

@require_POST
@login_required
def unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    
    # Remove o like se existir
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        post.liked_by_user = False
        post.likes_count = post.likes.count()
    
    return render(request, 'posts/partials/post_likes.html', {'post': post})

@login_required
def report_content(request, pk):
    """Denunciar conteúdo"""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.post = post
            report.save()
            messages.success(request, _('Conteúdo denunciado com sucesso. Nossa equipe irá analisar.'))
            return redirect('posts:detail', pk=pk)
    else:
        form = ReportForm()
    return render(request, 'posts/report_form.html', {'form': form, 'post': post})

@login_required
def moderate_reports(request):
    """Lista de denúncias para moderadores"""
    if not request.user.is_moderator:
        messages.error(request, _('Você não tem permissão para acessar esta página.'))
        return redirect('posts:list')
    
    reports = Report.objects.select_related('post', 'reporter', 'resolved_by').filter(resolved=False)
    return render(request, 'posts/moderate_reports.html', {'reports': reports})

@login_required
def resolve_report(request, pk):
    """Resolver denúncia"""
    if not request.user.is_moderator:
        messages.error(request, _('Você não tem permissão para realizar esta ação.'))
        return redirect('posts:list')
    
    report = get_object_or_404(Report, pk=pk)
    
    if request.method == 'POST':
        report.resolved = True
        report.resolved_by = request.user
        report.resolution_note = request.POST.get('resolution_note', '')
        report.save()
        
        messages.success(request, _('Denúncia resolvida com sucesso!'))
        return redirect('posts:moderate_reports')
    
    return render(request, 'posts/resolve_report.html', {'report': report})

@login_required
def hashtag_posts(request, hashtag_name):
    hashtag = get_object_or_404(Hashtag, name=hashtag_name.lower())
    posts = Post.objects.filter(hashtags=hashtag).select_related('author').prefetch_related('likes', 'comments')
    
    # Marca os posts que o usuário atual curtiu
    for post in posts:
        post.liked_by_user = Like.objects.filter(user=request.user, post=post).exists()
        post.likes_count = post.likes.count()
    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page', 1)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'hashtag': hashtag,
        'posts': posts,
    }
    return render(request, 'posts/hashtag_posts.html', context)

@login_required
def search(request):
    """Pesquisa posts e hashtags"""
    query = request.GET.get('q', '').strip()
    posts = []
    hashtags = []
    users = []
    
    if query:
        # Pesquisa posts
        posts = Post.objects.filter(
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        ).select_related('author').prefetch_related(
            'likes',
            'comments',
            'hashtags'
        ).order_by('-created_at')
        
        # Marca os posts que o usuário atual curtiu
        for post in posts:
            post.liked_by_user = Like.objects.filter(user=request.user, post=post).exists()
            post.likes_count = post.likes.count()
        
        # Pesquisa hashtags
        if query.startswith('#'):
            query = query[1:]
        hashtags = Hashtag.objects.filter(
            name__icontains=query
        ).annotate(
            post_count=Count('posts', distinct=True)
        ).order_by('-post_count')
        
        # Pesquisa usuários
        users = get_user_model().objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).select_related('profile')
    
    # Paginação dos posts
    paginator = Paginator(posts, 10)
    page = request.GET.get('page', 1)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'posts/search_results.html', {
        'query': query,
        'posts': posts,
        'hashtags': hashtags[:5],  # Limita a 5 hashtags mais relevantes
        'users': users[:5],  # Limita a 5 usuários mais relevantes
        'page_range': paginator.get_elided_page_range(
            posts.number,
            on_each_side=2,
            on_ends=1
        ) if posts else None
    })

def get_trending_hashtags():
    """Retorna as hashtags mais usadas nos últimos 7 dias"""
    seven_days_ago = timezone.now() - timezone.timedelta(days=7)
    return Hashtag.objects.filter(
        posts__created_at__gte=seven_days_ago,
        is_trending=True
    ).annotate(
        total_posts=Count('posts', distinct=True)
    ).order_by('-total_posts')[:5]
