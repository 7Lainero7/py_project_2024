const dateDisplay = document.getElementById('dateDisplay');
const formContainer = document.getElementById('formContainer');
const monthSelect = document.getElementById('monthSelect');
const yearSelect = document.getElementById('yearSelect');
let month = 7; // Август (0 - Январь, 1 - Февраль, ..., 7 - Август)
let year = 2024;

// Заполняем выпадающий список месяцев
const monthNames = [
    "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
];

monthNames.forEach((name, index) => {
    const option = document.createElement('option');
    option.value = index;
    option.textContent = name;
    monthSelect.appendChild(option);
});

// Заполняем выпадающий список годов
for (let i = 2020; i <= 2030; i++) {
    const option = document.createElement('option');
    option.value = i;
    option.textContent = i;
    yearSelect.appendChild(option);
}

// Устанавливаем начальные значения
monthSelect.value = month;
yearSelect.value = year;

// Обработчик клика на элементе dateDisplay
dateDisplay.addEventListener('click', () => {
    formContainer.style.display = 'flex'; // Показываем форму
});

// Обработчик клика на кнопку "Сохранить"
document.getElementById('submitBtn').addEventListener('click', () => {
    month = parseInt(monthSelect.value);
    year = parseInt(yearSelect.value);
    dateDisplay.textContent = `${monthNames[month]}, ${year}`; // Обновляем текст
    formContainer.style.display = 'none'; // Скрываем форму после сохранения
});