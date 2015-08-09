requirejs.config({
	baseUrl: "js",
	paths: {
		jquery: 'vendor/jquery-1.11.2.min',
		bootstrap: 'vendor/bootstrap.min',
		npm: 'vendor/npm',
		clndr: 'vendor/clndr.min',
		underscore: 'vendor/underscore-min',
		moment: 'vendor/moment.min'
	}
});

require([
		'jquery',
		'views',
		'visuals',
		'clndr',
		'underscore'
	], function(
		$
	){


	$( document ).ready(function() {

			$('#clndr_hold').clndr();


	});

	$('body').on('click', '#action_list_all_items', function() {

		views.place_loading_gif();

		//get_items.all_data('item_name').then(function(data){
		//});

	});



});
