requirejs.config({
    baseUrl: "../static/js",
    paths: {
        jquery: 'vendor/jquery-1.11.2.min',
        bootstrap: 'vendor/bootstrap.min',
        npm: 'vendor/npm',
        clndr: 'vendor/clndr.min',
        underscore: 'vendor/underscore-min',
        moment: 'vendor/moment.min',
        highcharts: 'vendor/highcharts',
        vide: 'vendor/vide.min'
    }
});

require([
    'jquery',
    'views',
    'visuals',
    'clndr',
    'underscore',
    'highcharts',
    'vide'
], function ($) {


    $(document).ready(function () {
        $('#clndr_holder').clndr({
            events: [
                {
                    date: '2015-08-09', title: 'CLNDR GitHub Page Finished', url: 'http://github.com/kylestetz/CLNDR'
                }
            ]
        });

        $('#highcharts_holder').highcharts({
            chart: {
                type: 'bar'
            },
            title: {
                text: 'Subject Scores'
            },
            subtitle: {
                text: 'derp derp'
            },
            xAxis: {
                categories: ['Math', 'Science', 'Philosophy', 'Art', 'History'],
                title: {
                    text: null
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Population (millions)',
                    align: 'high'
                },
                labels: {
                    overflow: 'justify'
                }
            },
            tooltip: {
                valueSuffix: ' '
            },
            plotOptions: {
                bar: {
                    dataLabels: {
                        enabled: true
                    }
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -40,
                y: 80,
                floating: true,
                borderWidth: 1,
                backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
                shadow: true
            },
            credits: {
                enabled: false
            },
            series: [{
                name: 'Videos',
                data: [107, 31, 635, 203, 2]
            }, {
                name: 'Exams',
                data: [133, 156, 947, 408, 6]
            }, {
                name: 'Discussion',
                data: [973, 914, 4054, 732, 34]
            }, {
                name: 'Exercises',
                data: [1052, 954, 4250, 740, 38]
            }]
        });


        Pusher.log = function (message) {
            if (window.console && window.console.log) {
                window.console.log(message);
            }
        };

        var pusher = new Pusher('c9da65d5b2527ee603e9', {
            encrypted: true
        });

        var channel = pusher.subscribe('test_channel');
        channel.bind('my_event', function (data) {
            a = '<div class="alert alert-warning alert-dismissible" role="alert">' +
            '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
            '<strong>Alert!</strong> ' + data.message + '</div>';
            $("body").prepend($(a))
        });


        /*$('#top_container').vide({
         mp4: '../vid/vid1.mp4'
         }, {
         volume: 1,
         playbackRate: 1,
         muted: true,
         loop: true,
         autoplay: true,
         position: '50% 50%', // Similar to the CSS `background-position` property.
         posterType: 'detect', // Poster image type. "detect" — auto-detection; "none" — no poster; "jpg", "png", "gif",... - extensions.
         resizing: true // Auto-resizing, read: https://github.com/VodkaBears/Vide#resizing
         });
         $('#myBlock').vide('extended path as a string', 'options as a string');*/


    });

    $('body').on('click', '#action_list_all_items', function () {

        views.place_loading_gif();

        //get_items.all_data('item_name').then(function(data){
        //});

    });


});
