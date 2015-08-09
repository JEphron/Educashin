requirejs.config({
	baseUrl: "js",
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
	], function(
		$
	){


	$( document ).ready(function() {

			$('#clndr_holder').clndr();




	    $('#highcharts_holder').highcharts({
	        chart: {
	            type: 'bar'
	        },
	        title: {
	            text: 'Historic World Population by Region'
	        },
	        subtitle: {
	            text: 'Source: <a href="https://en.wikipedia.org/wiki/World_population">Wikipedia.org</a>'
	        },
	        xAxis: {
	            categories: ['Africa', 'America', 'Asia', 'Europe', 'Oceania'],
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
	            valueSuffix: ' millions'
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
	            name: 'Year 1800',
	            data: [107, 31, 635, 203, 2]
	        }, {
	            name: 'Year 1900',
	            data: [133, 156, 947, 408, 6]
	        }, {
	            name: 'Year 2008',
	            data: [973, 914, 4054, 732, 34]
	        }, {
	            name: 'Year 2012',
	            data: [1052, 954, 4250, 740, 38]
	        }]
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

	$('body').on('click', '#action_list_all_items', function() {

		views.place_loading_gif();

		//get_items.all_data('item_name').then(function(data){
		//});

	});



});
