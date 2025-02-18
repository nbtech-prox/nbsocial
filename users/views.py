from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.utils.translation import gettext as _
from .models import CustomUser, UserFollowing
from .forms import CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.db.models import Q

@login_required
def profile(request, username=None):
    """Exibe o perfil do usuário"""
    if username is None:
        return redirect('users:profile', username=request.user.username)
    
    profile_user = get_object_or_404(CustomUser, username=username)
    followers = UserFollowing.objects.filter(following_user=profile_user)
    following = UserFollowing.objects.filter(user=profile_user)
    posts = profile_user.posts.all()
    
    is_following = UserFollowing.objects.filter(
        user=request.user,
        following_user=profile_user
    ).exists() if request.user.is_authenticated and request.user != profile_user else False
    
    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'is_following': is_following,
        'followers_count': int(followers.count()),
        'following_count': int(following.count()),
        'posts_count': int(posts.count()),
        'posts': posts.order_by('-created_at')[:10]  # Últimos 10 posts
    })

@login_required
def profile_edit(request):
    """Editar perfil do usuário"""
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, _('Perfil atualizado com sucesso!'))
                return redirect('users:profile', username=request.user.username)
            except Exception as e:
                messages.error(request, _('Erro ao salvar o perfil. Por favor, tente novamente.'))
        else:
            # Mostrar erros específicos do formulário
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'users/profile_edit.html', {'form': form})

@login_required
def toggle_follow(request, username):
    """Alternar entre seguir/deixar de seguir um usuário"""
    if request.method != 'POST':
        return JsonResponse({'error': _('Método não permitido')}, status=405)
        
    user_to_follow = get_object_or_404(CustomUser, username=username)
    
    if request.user == user_to_follow:
        return JsonResponse({'error': _('Você não pode seguir a si mesmo.')}, status=400)
    
    try:
        # Tenta encontrar uma relação de seguir existente
        following = UserFollowing.objects.get(
            user=request.user,
            following_user=user_to_follow
        )
        # Se encontrou, remove a relação (deixa de seguir)
        following.delete()
        is_following = False
    except UserFollowing.DoesNotExist:
        # Se não encontrou, cria uma nova relação (começa a seguir)
        UserFollowing.objects.create(
            user=request.user,
            following_user=user_to_follow
        )
        is_following = True
    
    # Retorna o HTML atualizado do botão
    return render(request, 'users/partials/follow_button.html', {
        'profile_user': user_to_follow,
        'is_following': is_following
    })

@login_required
def get_profile_stats(request, username):
    """Retorna estatísticas atualizadas do perfil"""
    user = get_object_or_404(CustomUser, username=username)
    followers = UserFollowing.objects.filter(following_user=user).select_related('user')
    following = UserFollowing.objects.filter(user=user).select_related('following_user')
    posts = user.posts.all()
    
    html = render(request, 'users/partials/profile_stats.html', {
        'profile_user': user,
        'followers': followers,
        'following': following,
        'posts': posts
    }).content.decode('utf-8')
    
    return HttpResponse(html)

@login_required
def follow_toggle(request, username):
    """Alterna o status de seguir/deixar de seguir um usuário"""
    if request.method != 'POST':
        return redirect('users:profile', username=username)
        
    user_to_follow = get_object_or_404(CustomUser, username=username)
    
    if user_to_follow == request.user:
        messages.error(request, "Você não pode seguir a si mesmo")
        return redirect('users:profile', username=username)
    
    following = UserFollowing.objects.filter(
        user=request.user,
        following_user=user_to_follow
    ).first()
    
    if following:
        following.delete()
        messages.success(request, f"Você deixou de seguir {user_to_follow.username}")
    else:
        UserFollowing.objects.create(
            user=request.user,
            following_user=user_to_follow
        )
        messages.success(request, f"Você está seguindo {user_to_follow.username}")
    
    return redirect('users:profile', username=username)

@login_required
def followers_list(request, username):
    """Lista de seguidores do usuário"""
    user = get_object_or_404(CustomUser, username=username)
    followers = user.follower_relationships.all().select_related('user')
    
    return render(request, 'users/followers_list.html', {
        'profile_user': user,
        'followers': followers,
    })

@login_required
def following_list(request, username):
    """Lista de usuários que o usuário segue"""
    user = get_object_or_404(CustomUser, username=username)
    following = user.following_relationships.all().select_related('following_user')
    
    return render(request, 'users/following_list.html', {
        'profile_user': user,
        'following': following,
    })

@login_required
def user_list(request):
    """Lista de usuários com busca"""
    search_query = request.GET.get('q', '')
    users = CustomUser.objects.all()
    
    if search_query:
        users = users.filter(username__icontains=search_query)
    
    return render(request, 'users/user_list.html', {
        'users': users,
        'search_query': search_query,
    })
