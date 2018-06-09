$(function() {
    var socket = new WebSocket("ws://0.0.0.0:8080/ws");
    socket.onopen = function() {
        alert("Соединение установлено.");
    };
    socket.onclose = function(event) {
        if (event.wasClean) {
            alert('Соединение закрыто чисто');
        } else {
            alert('Обрыв соединения');
        }
            alert('Код: ' + event.code + ' причина: ' + event.reason);
        };

    socket.onerror = function(error) {
        alert("Ошибка " + error.message);
    };
    $('#send').on('click', function() {
        var text = document.getElementById("message-field").value;
        socket.send(text);
        document.getElementById("message-field").value = ""
        return false;
    });
    function showMessage(message) {
        var control = $('#chat')
        var data = jQuery.parseJSON(message.data);
        control.html(control.html() + data.name + ': ' + data.text + '<br>')
        control.scrollTop(control.scrollTop() + 1000);
    }
    socket.onmessage = showMessage;
    $('#chat').scrollTop($('chat').scrollTop() + 1000);
    $('#message-field').on('keypress', function(e) {
         if (e.keyCode === 13) {
           $('#send').click();
           return false;
         }
       });
});