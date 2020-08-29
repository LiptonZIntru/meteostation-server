var id = document.getElementById('station_id').value;

var graphs = [
    {
        id: '#todayChart',
        url: '/today'
    },
    {
        id: '#yesterdayChart',
        url: '/yesterday'
    },
    {
        id: '#thisWeekChart',
        url: '/week'
    },
    {
        id: '#thisMonthChart',
        url: '/month'
    },
]

graphs.forEach(function (graph){
    var labels = [];
    var dataset = [];
    $.ajax({
        url: '/station/' + id + graph.url,
        async: false,
        success: function (response){
            var data = JSON.parse(response);
            labels = data['labels'];
            dataset = data['dataset'];
        }
    });

    new Chart($(graph.id), {
        // The type of chart we want to create
        type: 'line',
        // The data for our dataset
        data: {
            labels: labels,
            datasets: [{
                fill: true,
                backgroundColor: 'rgba(255,98,33, 0.4)',
                borderColor: 'rgba(255,98,33, 1)',
                label: 'Teplota dnes',
                data: dataset,
            }]
        },
    });
})
