var str = document.getElementById("forloop").innerHTML;

var day = new Date();
var day_1 = new Date();
var day_2 = new Date();
var day_3 = new Date();
var day_4 = new Date();
var day_5 = new Date();
var day_6 = new Date();
day_1.setDate(day_1.getDate() - 1);
day_2.setDate(day_2.getDate() - 2);
day_3.setDate(day_3.getDate() - 3);
day_4.setDate(day_4.getDate() - 4);
day_5.setDate(day_5.getDate() - 5);
day_6.setDate(day_6.getDate() - 6);
var options1 = {
  month: 'short',
  day: 'numeric',
  weekday: 'short'
};
var month1 = new Date();
var month2 = new Date();
var month3 = new Date();
var month4 = new Date();
var month5 = new Date();
var month6 = new Date();
var month7 = new Date();
var month8 = new Date();
var month9 = new Date();
var month10 = new Date();
var month11 = new Date();
var month12 = new Date();
month2.setMonth(month2.getMonth() - 1);
month3.setMonth(month3.getMonth() - 2);
month4.setMonth(month4.getMonth() - 3);
month5.setMonth(month5.getMonth() - 4);
month6.setMonth(month6.getMonth() - 5);
month7.setMonth(month7.getMonth() - 6);
month8.setMonth(month8.getMonth() - 7);
month9.setMonth(month9.getMonth() - 8);
month10.setMonth(month10.getMonth() - 9);
month11.setMonth(month11.getMonth() - 10);
month12.setMonth(month12.getMonth() - 11);
var options2 = {
  month: 'short',
  year: 'numeric'
};

const ctx = document.getElementById('sleep_week');

new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [
                day_6.toLocaleString("ru", options1),
                day_5.toLocaleString("ru", options1),
                day_4.toLocaleString("ru", options1),
                day_3.toLocaleString("ru", options1),
                day_2.toLocaleString("ru", options1),
                day_1.toLocaleString("ru", options1),
                day.toLocaleString("ru", options1)
                ],
        datasets: [{
            label: 'Длительность сна, ч.',
            data: [12, 19, 3, 5, 2, 3, 5],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const ctx2 = document.getElementById('sleep_month');

new Chart(ctx2, {
    type: 'bar',
    data: {
        labels: [
                month12.toLocaleString("ru", options2),
                month11.toLocaleString("ru", options2),
                month10.toLocaleString("ru", options2),
                month9.toLocaleString("ru", options2),
                month8.toLocaleString("ru", options2),
                month7.toLocaleString("ru", options2),
                month6.toLocaleString("ru", options2),
                month5.toLocaleString("ru", options2),
                month4.toLocaleString("ru", options2),
                month3.toLocaleString("ru", options2),
                month2.toLocaleString("ru", options2),
                month1.toLocaleString("ru", options2)
                ],
        datasets: [{
            label: 'Длительность сна, ч.',
            data: [12, 19, 3, 5, 2, 3, 3, 12, 30, 22, 11, 28],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const ctx3 = document.getElementById('sleep_start_week');

new Chart(ctx3, {
    type: 'bar',
    data: {
        labels: [
                day_6.toLocaleString("ru", options1),
                day_5.toLocaleString("ru", options1),
                day_4.toLocaleString("ru", options1),
                day_3.toLocaleString("ru", options1),
                day_2.toLocaleString("ru", options1),
                day_1.toLocaleString("ru", options1),
                day.toLocaleString("ru", options1),
                ],
        datasets: [{
            label: 'Время начала сна',
            data: [12, 19, 3, 5, 2, 3, 5],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const ctx4 = document.getElementById('sleep_start_month');

new Chart(ctx4, {
    type: 'bar',
    data: {
        labels: [
                month12.toLocaleString("ru", options2),
                month11.toLocaleString("ru", options2),
                month10.toLocaleString("ru", options2),
                month9.toLocaleString("ru", options2),
                month8.toLocaleString("ru", options2),
                month7.toLocaleString("ru", options2),
                month6.toLocaleString("ru", options2),
                month5.toLocaleString("ru", options2),
                month4.toLocaleString("ru", options2),
                month3.toLocaleString("ru", options2),
                month2.toLocaleString("ru", options2),
                month1.toLocaleString("ru", options2)
                ],
        datasets: [{
            label: 'Время начала сна',
            data: [12, 19, 3, 5, 2, 3, 3, 12, 30, 22, 11, 28],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const ctx5 = document.getElementById('sleep_end_week');

new Chart(ctx5, {
    type: 'bar',
    data: {
        labels: [
                day_6.toLocaleString("ru", options1),
                day_5.toLocaleString("ru", options1),
                day_4.toLocaleString("ru", options1),
                day_3.toLocaleString("ru", options1),
                day_2.toLocaleString("ru", options1),
                day_1.toLocaleString("ru", options1),
                day.toLocaleString("ru", options1),
                ],
        datasets: [{
            label: 'Время окончания сна',
            data: [12, 19, 3, 5, 2, 3, 5],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const ctx6 = document.getElementById('sleep_end_month');

new Chart(ctx6, {
    type: 'bar',
    data: {
        labels: [
                month12.toLocaleString("ru", options2),
                month11.toLocaleString("ru", options2),
                month10.toLocaleString("ru", options2),
                month9.toLocaleString("ru", options2),
                month8.toLocaleString("ru", options2),
                month7.toLocaleString("ru", options2),
                month6.toLocaleString("ru", options2),
                month5.toLocaleString("ru", options2),
                month4.toLocaleString("ru", options2),
                month3.toLocaleString("ru", options2),
                month2.toLocaleString("ru", options2),
                month1.toLocaleString("ru", options2)
                ],
        datasets: [{
            label: 'Время окончания сна',
            data: [12, 19, 3, 5, 2, 3, 3, 12, 30, 22, 11, 28],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const ctx7 = document.getElementById('condition_change_week');

new Chart(ctx7, {
    type: 'bar',
    data: {
        labels: [
                day_6.toLocaleString("ru", options1),
                day_5.toLocaleString("ru", options1),
                day_4.toLocaleString("ru", options1),
                day_3.toLocaleString("ru", options1),
                day_2.toLocaleString("ru", options1),
                day_1.toLocaleString("ru", options1),
                day.toLocaleString("ru", options1),
                ],
        datasets: [{
            label: 'Изменение состояния во время сна',
            data: [12, 19, 3, 5, 2, 3, 5],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const ctx8 = document.getElementById('condition_change_month');

new Chart(ctx8, {
    type: 'bar',
    data: {
        labels: [
                month12.toLocaleString("ru", options2),
                month11.toLocaleString("ru", options2),
                month10.toLocaleString("ru", options2),
                month9.toLocaleString("ru", options2),
                month8.toLocaleString("ru", options2),
                month7.toLocaleString("ru", options2),
                month6.toLocaleString("ru", options2),
                month5.toLocaleString("ru", options2),
                month4.toLocaleString("ru", options2),
                month3.toLocaleString("ru", options2),
                month2.toLocaleString("ru", options2),
                month1.toLocaleString("ru", options2)
                ],
        datasets: [{
            label: 'Изменение состояния во время сна',
            data: [12, 19, 3, 5, 2, 3, 3, 12, 30, 22, 11, 28],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const ctx9 = document.getElementById('condition_before_week');

new Chart(ctx9, {
    type: 'bar',
    data: {
        labels: [
                day_6.toLocaleString("ru", options1),
                day_5.toLocaleString("ru", options1),
                day_4.toLocaleString("ru", options1),
                day_3.toLocaleString("ru", options1),
                day_2.toLocaleString("ru", options1),
                day_1.toLocaleString("ru", options1),
                day.toLocaleString("ru", options1),
                ],
        datasets: [{
            label: 'Оценка состояния перед сном',
            data: [12, 19, 3, 5, 2, 3, 5],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const ctx10 = document.getElementById('condition_before_month');

new Chart(ctx10, {
    type: 'bar',
    data: {
        labels: [
                month12.toLocaleString("ru", options2),
                month11.toLocaleString("ru", options2),
                month10.toLocaleString("ru", options2),
                month9.toLocaleString("ru", options2),
                month8.toLocaleString("ru", options2),
                month7.toLocaleString("ru", options2),
                month6.toLocaleString("ru", options2),
                month5.toLocaleString("ru", options2),
                month4.toLocaleString("ru", options2),
                month3.toLocaleString("ru", options2),
                month2.toLocaleString("ru", options2),
                month1.toLocaleString("ru", options2)
                ],
        datasets: [{
            label: 'Оценка состояния перед сном',
            data: [12, 19, 3, 5, 2, 3, 3, 12, 30, 22, 11, 28],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const ctx11 = document.getElementById('condition_after_week');

new Chart(ctx11, {
    type: 'bar',
    data: {
        labels: [
                day_6.toLocaleString("ru", options1),
                day_5.toLocaleString("ru", options1),
                day_4.toLocaleString("ru", options1),
                day_3.toLocaleString("ru", options1),
                day_2.toLocaleString("ru", options1),
                day_1.toLocaleString("ru", options1),
                day.toLocaleString("ru", options1),
                ],
        datasets: [{
            label: 'Оценка состояния после сна',
            data: [12, 19, 3, 5, 2, 3, 5],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const ctx12 = document.getElementById('condition_after_month');

new Chart(ctx12, {
    type: 'bar',
    data: {
        labels: [
                month12.toLocaleString("ru", options2),
                month11.toLocaleString("ru", options2),
                month10.toLocaleString("ru", options2),
                month9.toLocaleString("ru", options2),
                month8.toLocaleString("ru", options2),
                month7.toLocaleString("ru", options2),
                month6.toLocaleString("ru", options2),
                month5.toLocaleString("ru", options2),
                month4.toLocaleString("ru", options2),
                month3.toLocaleString("ru", options2),
                month2.toLocaleString("ru", options2),
                month1.toLocaleString("ru", options2)
                ],
        datasets: [{
            label: 'Оценка состояния после сна',
            data: [12, 19, 3, 5, 2, 3, 3, 12, 30, 22, 11, 28],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
