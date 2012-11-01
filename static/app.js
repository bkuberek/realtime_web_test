
var ws;

$(document).ready(function () {

  $("#connect").click(function (evt) {
    evt.preventDefault();

    var host = $("#host").val();
    var port = $("#port").val();
    var uri = $("#uri").val();

    ws = new WebSocket("ws://" + host + ":" + port + uri);

    ws.onmessage = function(evt) {
      $('#inbox').append(evt.data+'\n');
      $('#inbox')[0].scrollTop = $('#response')[0].scrollHeight;
    };

    ws.onclose = function(evt) {
      $('#inbox').append('Connection Closed\n');
      $('#inbox').append(evt.data+'\n');
      $('#connect').show();
      $("#info").removeClass('connected');
      $('#status').text('Disconnected');
    };

    ws.onopen = function(evt) {
      $("#info").addClass('connected');
      $('#status').text('Connected');
      $('#inbox').append('Connection Open\n');
      $('#inbox').append(evt.data+'\n');
      $('#connect').hide();
    };
  });

//  $('#send').click(function (event) {
//    ws.send($('#message').val());
//    $('#message').val('');
//  });
});
