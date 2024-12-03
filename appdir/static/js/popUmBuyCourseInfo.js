document.getElementById('homeWorkHeaderLection').addEventListener('click', function() {
    // Получаем содержимое homeWork-category-body
    const bodyContent = document.getElementById('homeWorkBodyLection').innerHTML;
    // Вставляем содержимое в поп-ап
    document.getElementById('popupBody').innerHTML = bodyContent;
    // Показываем поп-ап
    document.getElementById('popup').style.display = 'flex';
});

document.getElementById('closePopup').addEventListener('click', function() {
    // Скрываем поп-ап
    document.getElementById('popup').style.display = 'none';
});