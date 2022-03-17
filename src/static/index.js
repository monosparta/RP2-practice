
var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                datasets: [{
                    label: '平均溫度',
                    data: [20, 22.3, 25, 26, 28, 31.2, 33],
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)',
                }]
            },
        });