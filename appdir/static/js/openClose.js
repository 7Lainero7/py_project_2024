function toggleCategory(header) {
    const body = header.nextElementSibling;
    body.classList.toggle('hidden');

    // Меняем стили заголовка при сворачивании/разворачивании
    header.classList.toggle('collapsed');
}