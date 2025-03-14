var str = document.getElementById("forloop").innerHTML.split(",");
var values = new Array(str.length);
for (var i = 0; i < str.length; i++)
{
    values[i] = str[i].split(" ");
}

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
                day.toLocaleString("ru", options1),
                ],
        datasets: [{
            label: 'Длительность сна, ч.',
            data: [
                parseFloat(values[0][0]),
                parseFloat(values[0][1]),
                parseFloat(values[0][2]),
                parseFloat(values[0][3]),
                parseFloat(values[0][4]),
                parseFloat(values[0][5]),
                parseFloat(values[0][6])
                ],
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
            data: [
                parseFloat(values[1][0]),
                parseFloat(values[1][1]),
                parseFloat(values[1][2]),
                parseFloat(values[1][3]),
                parseFloat(values[1][4]),
                parseFloat(values[1][5]),
                parseFloat(values[1][6]),
                parseFloat(values[1][7]),
                parseFloat(values[1][8]),
                parseFloat(values[1][9]),
                parseFloat(values[1][10]),
                parseFloat(values[1][11]),
                ],
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
            data: [
                parseFloat(values[2][0]),
                parseFloat(values[2][1]),
                parseFloat(values[2][2]),
                parseFloat(values[2][3]),
                parseFloat(values[2][4]),
                parseFloat(values[2][5]),
                parseFloat(values[2][6])
                ],
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
            data: [
                parseFloat(values[3][0]),
                parseFloat(values[3][1]),
                parseFloat(values[3][2]),
                parseFloat(values[3][3]),
                parseFloat(values[3][4]),
                parseFloat(values[3][5]),
                parseFloat(values[3][6]),
                parseFloat(values[3][7]),
                parseFloat(values[3][8]),
                parseFloat(values[3][9]),
                parseFloat(values[3][10]),
                parseFloat(values[3][11]),
                ],
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
            data: [
                parseFloat(values[4][0]),
                parseFloat(values[4][1]),
                parseFloat(values[4][2]),
                parseFloat(values[4][3]),
                parseFloat(values[4][4]),
                parseFloat(values[4][5]),
                parseFloat(values[4][6])
                ],
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
            data: [
                parseFloat(values[5][0]),
                parseFloat(values[5][1]),
                parseFloat(values[5][2]),
                parseFloat(values[5][3]),
                parseFloat(values[5][4]),
                parseFloat(values[5][5]),
                parseFloat(values[5][6]),
                parseFloat(values[5][7]),
                parseFloat(values[5][8]),
                parseFloat(values[5][9]),
                parseFloat(values[5][10]),
                parseFloat(values[5][11]),
                ],
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
            data: [
                parseFloat(values[6][0]),
                parseFloat(values[6][1]),
                parseFloat(values[6][2]),
                parseFloat(values[6][3]),
                parseFloat(values[6][4]),
                parseFloat(values[6][5]),
                parseFloat(values[6][6])
                ],
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
            data: [
                parseFloat(values[7][0]),
                parseFloat(values[7][1]),
                parseFloat(values[7][2]),
                parseFloat(values[7][3]),
                parseFloat(values[7][4]),
                parseFloat(values[7][5]),
                parseFloat(values[7][6]),
                parseFloat(values[7][7]),
                parseFloat(values[7][8]),
                parseFloat(values[7][9]),
                parseFloat(values[7][10]),
                parseFloat(values[7][11]),
                ],
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
            data: [
                parseFloat(values[8][0]),
                parseFloat(values[8][1]),
                parseFloat(values[8][2]),
                parseFloat(values[8][3]),
                parseFloat(values[8][4]),
                parseFloat(values[8][5]),
                parseFloat(values[8][6])
                ],
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
            data: [
                parseFloat(values[9][0]),
                parseFloat(values[9][1]),
                parseFloat(values[9][2]),
                parseFloat(values[9][3]),
                parseFloat(values[9][4]),
                parseFloat(values[9][5]),
                parseFloat(values[9][6]),
                parseFloat(values[9][7]),
                parseFloat(values[9][8]),
                parseFloat(values[9][9]),
                parseFloat(values[9][10]),
                parseFloat(values[9][11]),
                ],
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
            data: [
                parseFloat(values[10][0]),
                parseFloat(values[10][1]),
                parseFloat(values[10][2]),
                parseFloat(values[10][3]),
                parseFloat(values[10][4]),
                parseFloat(values[10][5]),
                parseFloat(values[10][6])
                ],
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
            data: [
                parseFloat(values[11][0]),
                parseFloat(values[11][1]),
                parseFloat(values[11][2]),
                parseFloat(values[11][3]),
                parseFloat(values[11][4]),
                parseFloat(values[11][5]),
                parseFloat(values[11][6]),
                parseFloat(values[11][7]),
                parseFloat(values[11][8]),
                parseFloat(values[11][9]),
                parseFloat(values[11][10]),
                parseFloat(values[11][11]),
                ],
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
