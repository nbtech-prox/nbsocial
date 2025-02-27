/**
 * Gerenciador de Notificações em tempo real
 * Este script gerencia a conexão WebSocket para notificações em tempo real
 */
document.addEventListener('DOMContentLoaded', function() {
    const notificationBadge = document.getElementById('notification-badge');
    const notificationDropdown = document.getElementById('notification-dropdown');
    const notificationList = document.getElementById('notification-list');
    const markAllReadBtn = document.getElementById('mark-all-read');
    
    // Verifica se os elementos existem antes de prosseguir
    if (!notificationBadge) {
        console.warn('Elemento de badge de notificação não encontrado');
        return;
    }
    
    let notificationsSocket = null;
    
    // Inicializa a conexão WebSocket
    function connectWebSocket() {
        // Protocolo WebSocket (wss:// para HTTPS, ws:// para HTTP)
        const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        const wsUrl = `${protocol}${window.location.host}/ws/notifications/`;
        
        notificationsSocket = new WebSocket(wsUrl);
        
        notificationsSocket.onopen = function(e) {
            console.log('Conexão WebSocket estabelecida');
            // Solicitar lista de notificações recentes ao conectar
            requestRecentNotifications();
        };
        
        notificationsSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            console.log('Mensagem recebida:', data);
            
            if (data.type === 'notification') {
                // Nova notificação recebida
                handleNewNotification(data.notification);
            } else if (data.type === 'unread_count') {
                // Atualizar contagem de notificações não lidas
                updateUnreadCount(data.count);
            } else if (data.type === 'notifications_list') {
                // Atualizar lista de notificações
                renderNotificationsList(data.notifications);
            }
        };
        
        notificationsSocket.onclose = function(e) {
            console.log('Conexão WebSocket fechada');
            // Tentar reconectar após um tempo
            setTimeout(function() {
                connectWebSocket();
            }, 3000);
        };
        
        notificationsSocket.onerror = function(e) {
            console.error('Erro na conexão WebSocket:', e);
        };
    }
    
    // Solicitar notificações recentes
    function requestRecentNotifications(limit = 10) {
        if (notificationsSocket && notificationsSocket.readyState === WebSocket.OPEN) {
            notificationsSocket.send(JSON.stringify({
                'command': 'get_notifications',
                'limit': limit
            }));
        }
    }
    
    // Atualizar contagem de notificações não lidas
    function updateUnreadCount(count) {
        if (notificationBadge) {
            if (count > 0) {
                notificationBadge.textContent = count > 99 ? '99+' : count;
                notificationBadge.classList.remove('hidden');
            } else {
                notificationBadge.classList.add('hidden');
            }
        }
    }
    
    // Lidar com novas notificações
    function handleNewNotification(notification) {
        // Tocar som de notificação (opcional)
        playNotificationSound();
        
        // Atualizar contagem de notificações não lidas
        const currentCount = parseInt(notificationBadge.textContent) || 0;
        updateUnreadCount(currentCount + 1);
        
        // Atualizar lista de notificações se o dropdown estiver aberto
        if (notificationDropdown && !notificationDropdown.classList.contains('hidden')) {
            requestRecentNotifications();
        }
        
        // Mostrar notificação do navegador (se permissão concedida)
        showBrowserNotification(notification);
    }
    
    // Renderizar lista de notificações
    function renderNotificationsList(notifications) {
        if (!notificationList) return;
        
        // Limpar lista atual
        notificationList.innerHTML = '';
        
        if (notifications.length === 0) {
            notificationList.innerHTML = '<div class="p-4 text-center text-gray-500">Nenhuma notificação recente</div>';
            return;
        }
        
        // Adicionar notificações à lista
        notifications.forEach(notification => {
            const notificationItem = document.createElement('div');
            notificationItem.className = `p-3 border-b border-gray-200 hover:bg-gray-50 transition cursor-pointer ${!notification.read ? 'bg-blue-50' : ''}`;
            notificationItem.setAttribute('data-notification-id', notification.id);
            
            notificationItem.innerHTML = `
                <a href="${notification.url}" class="block">
                    <div class="flex items-center">
                        <div class="flex-shrink-0 mr-3">
                            <div class="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white">
                                ${getNotificationIcon(notification.type)}
                            </div>
                        </div>
                        <div class="flex-grow min-w-0">
                            <p class="text-sm font-medium text-gray-900 truncate">
                                ${notification.sender}
                            </p>
                            <p class="text-sm text-gray-600 truncate">
                                ${notification.content}
                            </p>
                            <p class="text-xs text-gray-500 mt-1">
                                ${formatDate(notification.created_at)}
                            </p>
                        </div>
                        ${!notification.read ? '<div class="flex-shrink-0 ml-2"><span class="w-2 h-2 rounded-full bg-blue-600"></span></div>' : ''}
                    </div>
                </a>
            `;
            
            // Adicionar evento para marcar como lida ao clicar
            notificationItem.addEventListener('click', function() {
                markAsRead(notification.id);
            });
            
            notificationList.appendChild(notificationItem);
        });
    }
    
    // Marcar notificação como lida
    function markAsRead(notificationId) {
        if (notificationsSocket && notificationsSocket.readyState === WebSocket.OPEN) {
            notificationsSocket.send(JSON.stringify({
                'command': 'mark_as_read',
                'notification_id': notificationId
            }));
        }
    }
    
    // Marcar todas as notificações como lidas
    function markAllAsRead() {
        if (notificationsSocket && notificationsSocket.readyState === WebSocket.OPEN) {
            notificationsSocket.send(JSON.stringify({
                'command': 'mark_all_as_read'
            }));
        }
    }
    
    // Obter ícone para tipo de notificação
    function getNotificationIcon(type) {
        switch (type) {
            case 'like':
                return '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z"></path></svg>';
            case 'comment':
                return '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zM7 8H5v2h2V8zm2 0h2v2H9V8zm6 0h-2v2h2V8z" clip-rule="evenodd"></path></svg>';
            case 'follow':
                return '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"></path></svg>';
            case 'mention':
                return '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M14.243 5.757a6 6 0 10-.986 9.284 1 1 0 111.087 1.678A8 8 0 1118 10a3 3 0 01-4.8 2.401A4 4 0 1114 10a1 1 0 102 0c0-1.537-.586-3.07-1.757-4.243zM12 10a2 2 0 10-4 0 2 2 0 004 0z" clip-rule="evenodd"></path></svg>';
            default:
                return '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>';
        }
    }
    
    // Formatar data
    function formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diff = (now - date) / 1000; // diferença em segundos
        
        if (diff < 60) {
            return 'agora mesmo';
        } else if (diff < 3600) {
            const minutes = Math.floor(diff / 60);
            return `${minutes} ${minutes === 1 ? 'minuto' : 'minutos'} atrás`;
        } else if (diff < 86400) {
            const hours = Math.floor(diff / 3600);
            return `${hours} ${hours === 1 ? 'hora' : 'horas'} atrás`;
        } else if (diff < 604800) {
            const days = Math.floor(diff / 86400);
            return `${days} ${days === 1 ? 'dia' : 'dias'} atrás`;
        } else {
            return date.toLocaleDateString('pt-PT', { 
                day: '2-digit', 
                month: '2-digit', 
                year: 'numeric' 
            });
        }
    }
    
    // Tocar som de notificação
    function playNotificationSound() {
        // Adicionar som de notificação (opcional)
        // const sound = new Audio('/static/sounds/notification.mp3');
        // sound.play();
    }
    
    // Mostrar notificação do navegador
    function showBrowserNotification(notification) {
        if (Notification.permission === 'granted') {
            const title = 'NBSocial';
            const options = {
                body: `${notification.sender} ${notification.content}`,
                icon: '/static/img/logo.png'
            };
            new Notification(title, options);
        }
    }
    
    // Inicializar solicitação de permissão para notificações
    function requestNotificationPermission() {
        if ('Notification' in window && Notification.permission !== 'granted' && Notification.permission !== 'denied') {
            Notification.requestPermission();
        }
    }
    
    // Eventos
    if (markAllReadBtn) {
        markAllReadBtn.addEventListener('click', function(e) {
            e.preventDefault();
            markAllAsRead();
        });
    }
    
    // Conectar WebSocket
    connectWebSocket();
    
    // Solicitar permissão para notificações do navegador
    requestNotificationPermission();
});
