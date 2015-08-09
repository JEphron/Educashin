define(['jquery'], function($) {

Pusher.log = function(message) {
  if (window.console && window.console.log) {
    window.console.log(message);
  }
};

var pusher = new Pusher('c9da65d5b2527ee603e9', {
  encrypted: true
});
var channel = pusher.subscribe('test_channel');
channel.bind('my_event', function(data) {
  alert(data.message);
});

function place_loading_gif() {

  $('#main_content').empty().append('<img id="loading_gif" src="loading.gif" alt="Loading..." />');

}
