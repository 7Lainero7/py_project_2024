const weeks = document.querySelectorAll('.week');
let currentWeekIndex = 0;

function updateCalendar() {
    // Скрыть все недели
    weeks.forEach((week, index) => {
        week.style.display = index === currentWeekIndex ? 'block' : 'none';
    });
}

document.getElementById('prev-week').addEventListener('click', () => {
    if (currentWeekIndex > 0) {
        currentWeekIndex--;
        updateCalendar();
    }
});

document.getElementById('next-week').addEventListener('click', () => {
    if (currentWeekIndex < weeks.length - 1) {
        currentWeekIndex++;
        updateCalendar();
    }
});

// Инициализация
updateCalendar();