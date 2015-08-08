requirejs.config({
	baseUrl: "js",
	paths: {
		jquery: 'vendor/jquery-1.11.2.min',
		bootstrap: 'vendor/bootstrap.min',
		npm: 'vendor/npm'
	}
});

require([
		'jquery',
		'views',
		'visuals'
	], function(
		$,
		views
	){



	$('body').on('click', '#action_list_all_items', function() {

		views.place_loading_gif();

		//get_items.all_data('item_name').then(function(data){
		//});

	});



});
