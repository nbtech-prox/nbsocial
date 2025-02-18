document.addEventListener('DOMContentLoaded', function() {
    const rightSidebar = document.querySelector('.right-sidebar');
    if (!rightSidebar) return;

    let lastScrollPosition = window.scrollY;
    const offset = 16; // equivalente ao top-4 do Tailwind

    function updateSidebarPosition() {
        const currentScroll = window.scrollY;
        const sidebarRect = rightSidebar.getBoundingClientRect();
        const parentRect = rightSidebar.parentElement.getBoundingClientRect();

        // Ajusta a posição apenas se estiver dentro dos limites do pai
        if (parentRect.top <= offset && parentRect.bottom >= sidebarRect.height + offset) {
            rightSidebar.style.position = 'fixed';
            rightSidebar.style.top = offset + 'px';
            rightSidebar.style.width = parentRect.width + 'px';
        } else if (parentRect.top > offset) {
            rightSidebar.style.position = 'static';
        } else {
            rightSidebar.style.position = 'absolute';
            rightSidebar.style.bottom = '0';
            rightSidebar.style.top = 'auto';
        }

        lastScrollPosition = currentScroll;
    }

    window.addEventListener('scroll', updateSidebarPosition);
    window.addEventListener('resize', updateSidebarPosition);
    updateSidebarPosition();
});
