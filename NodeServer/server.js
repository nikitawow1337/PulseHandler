var http = require('http');
var Static = require('node-static');
var WebSocketServer = new require('ws');
var fs = require('fs');

// подключенные клиенты
var clients = {};

// WebSocket-сервер на порту 8888
var webSocketServer = new WebSocketServer.Server({server: '0.0.0.0', port: 8888});
webSocketServer.on('connection', function(ws) {

  var id = Math.random();
  clients[id] = ws;
  console.log("новое соединение " + id);

  ws.on('message', function(message) {
    console.log('получено сообщение ' + message);
	
	fs.writeFile("../heart-rate.txt", message, function(err) {
      if(err) {
        return console.log(err);
      }

      console.log("The file was saved!");
	}); 

    for(var key in clients) {
      clients[key].send(message);
    }
  });

  ws.on('close', function() {
    console.log('соединение закрыто ' + id);
    delete clients[id];
  });

});


// статический сервер на 8080
/*var fileServer = new Static.Server('.');
http.createServer(function (req, res) {
  
  fileServer.serve(req, res);

}).listen(8080);*/

console.log("Сервер запущен на порте 8888");

