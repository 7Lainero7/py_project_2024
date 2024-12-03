document.getElementById('homeWorkHeaderOption').addEventListener('click', function() {
    // Получаем содержимое homeWork-category-body
    const bodyContent = document.getElementById('homeWorkBodyOption').innerHTML;
    // Вставляем содержимое в поп-ап
    document.getElementById('popupBody').innerHTML = bodyContent;
    // Показываем поп-ап
    document.getElementById('popup').style.display = 'flex';
});

document.getElementById('homeWorkHeaderPractice').addEventListener('click', function() {
    // Получаем содержимое homeWork-category-body
    const bodyContent = document.getElementById('homeWorkBodyPractice').innerHTML;
    // Вставляем содержимое в поп-ап
    document.getElementById('popupBody').innerHTML = bodyContent;
    // Показываем поп-ап
    document.getElementById('popup').style.display = 'flex';
});

document.getElementById('homeWorkHeaderDop').addEventListener('click', function() {
    // Получаем содержимое homeWork-category-body
    const bodyContent = document.getElementById('homeWorkBodyDop').innerHTML;
    // Вставляем содержимое в поп-ап
    document.getElementById('popupBody').innerHTML = bodyContent;
    // Показываем поп-ап
    document.getElementById('popup').style.display = 'flex';
});

document.getElementById('homeWorkHeaderTheory').addEventListener('click', function() {
    // Получаем содержимое homeWork-category-body
    const bodyContent = document.getElementById('homeWorkBodyTheory').innerHTML;
    // Вставляем содержимое в поп-ап
    document.getElementById('popupBody').innerHTML = bodyContent;
    // Показываем поп-ап
    document.getElementById('popup').style.display = 'flex';
});

document.getElementById('closePopup').addEventListener('click', function() {
    // Скрываем поп-ап
    document.getElementById('popup').style.display = 'none';
});