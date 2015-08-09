define(['jquery'], function($) {

	function place_loading_gif() {

		$('#main_content').empty().append('<img id="loading_gif" src="loading.gif" alt="Loading..." />');

	}


	return {
		place_loading_gif: place_loading_gif
  }

});
