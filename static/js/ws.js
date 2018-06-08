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
    socket.onmessage = function(event) {
        alert("Получены данные " + event.data);
    };
    socket.onerror = function(error) {
        alert("Ошибка " + error.message);
    };
    $('#send').on('click', function() {
        var text = document.getElementById("message-field").value;
        socket.send(text);
        return false;
    });
});