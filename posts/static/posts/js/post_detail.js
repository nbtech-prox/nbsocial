document.addEventListener('DOMContentLoaded', function() {
    // Like Button
    const likeButtons = document.querySelectorAll('.like-button');
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.dataset.postId;
            fetch(`/posts/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            })
            .then(response => response.json())
            .then(data => {
                const likesCount = this.querySelector('.likes-count');
                likesCount.textContent = data.likes_count;
                this.classList.toggle('text-blue-600');
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Report Button
    const reportButtons = document.querySelectorAll('.report-button');
    reportButtons.forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.closest('.card').dataset.postId;
            // Implemente a lógica do modal de denúncia aqui
        });
    });

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
