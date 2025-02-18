document.addEventListener('DOMContentLoaded', function() {
    // Função para fazer a mensagem desaparecer suavemente
    function fadeOut(element) {
        let opacity = 1;
        const timer = setInterval(function() {
            if (opacity <= 0.1) {
                clearInterval(timer);
                element.style.display = 'none';
                element.remove();
            }
            element.style.opacity = opacity;
            opacity -= 0.1;
        }, 50);
    }

    // Pegar todas as mensagens
    const messages = document.querySelectorAll('.message-container > div');
    
    // Para cada mensagem, configurar o temporizador para desaparecer
    messages.forEach(function(message) {
        // Definir a opacidade inicial como 1
        message.style.opacity = '1';
        message.style.transition = 'opacity 0.5s ease-in-out';
        
        // Fazer a mensagem desaparecer após 3 segundos
        setTimeout(function() {
            fadeOut(message);
        }, 3000);
    });
});
