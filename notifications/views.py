from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification

@login_required
def notification_list(request):
    """Lista todas as notificações do usuário"""
    notifications = (
        Notification.objects
        .filter(recipient=request.user)
        .select_related('sender', 'post', 'comment')
        .order_by('-created_at')
    )
    
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications
    })

@login_required
def mark_all_as_read(request):
    """Marca todas as notificações como lidas"""
    if request.method == 'POST':
        Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def get_unread_count(request):
    """Retorna o número de notificações não lidas"""
    count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()
    return JsonResponse({'count': count})
