def unread_notifications(request):
    """
    Context processor que adiciona o número de notificações não lidas ao contexto
    para estar disponível em todos os templates.
    """
    unread_count = 0
    
    if request.user.is_authenticated:
        unread_count = request.user.notifications_received.filter(read=False).count()
    
    return {
        'unread_notifications_count': unread_count,
    }
