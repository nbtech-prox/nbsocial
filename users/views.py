from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils.translation import gettext as _
from .models import CustomUser, UserFollowing
from .forms import CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.db.models import Q

@login_required
def profile(request, username=None):
    """Perfil do usuário"""
    if username is None:
        return redirect('users:profile', username=request.user.username)
    
    user = get_object_or_404(CustomUser, username=username)
    posts = user.posts.select_related('author').prefetch_related('likes', 'comments').all()
    followers = UserFollowing.objects.filter(following_user=user).select_related('user')
    following = UserFollowing.objects.filter(user=user).select_related('following_user')
    
    # Verifica se o usuário logado está seguindo o usuário do perfil
    is_following = UserFollowing.objects.filter(
        user=request.user,
        following_user=user
    ).exists() if request.user.is_authenticated and request.user != user else False
    
    return render(request, 'users/profile.html', {
        'profile_user': user,
        'posts': posts,
        'followers': followers,
        'following': following,
        'is_following': is_following
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
        messages.error(request, _('Você não pode seguir a si mesmo.'))
        return redirect('users:profile', username=username)
    
    try:
        # Tenta encontrar uma relação de seguir existente
        following = UserFollowing.objects.get(
            user=request.user,
            following_user=user_to_follow
        )
        # Se encontrou, remove a relação (deixa de seguir)
        following.delete()
        messages.success(request, _('Você deixou de seguir %(username)s.') % {'username': username})
    except UserFollowing.DoesNotExist:
        # Se não encontrou, cria uma nova relação (começa a seguir)
        UserFollowing.objects.create(
            user=request.user,
            following_user=user_to_follow
        )
        messages.success(request, _('Você agora está seguindo %(username)s.') % {'username': username})
    
    return redirect('users:profile', username=username)

@login_required
def follow_toggle(request, username):
    """Seguir/deixar de seguir usuário"""
    if request.method == 'POST' and request.is_ajax():
        user_to_follow = get_object_or_404(CustomUser, username=username)
        
        if user_to_follow == request.user:
            return JsonResponse({
                'error': _('Você não pode seguir a si mesmo.')
            }, status=400)
        
        following = UserFollowing.objects.filter(
            user=request.user,
            following_user=user_to_follow
        )
        
        if following.exists():
            following.delete()
            is_following = False
        else:
            UserFollowing.objects.create(
                user=request.user,
                following_user=user_to_follow
            )
            is_following = True
        
        return JsonResponse({
            'is_following': is_following,
            'followers_count': UserFollowing.objects.filter(following_user=user_to_follow).count()
        })
    
    return JsonResponse({'error': _('Método não permitido')}, status=405)

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
