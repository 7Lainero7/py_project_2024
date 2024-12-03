
    document.addEventListener('DOMContentLoaded', function() {
        const toggleButton = document.querySelector('.toggle-sidebar');
        const sidebar = document.querySelector('.option_sidebar_wrapper');
        const closeButton = document.querySelector('.close-sidebar');

        toggleButton.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });

        closeButton.addEventListener('click', function() {
            sidebar.classList.remove('active');
        });
    });