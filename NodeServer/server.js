var http = require('http');
var Static = require('node-static');
var WebSocketServer = new require('ws');
var fs = require('fs');

// Connected clients
var clients = {};

// Open WebSocketServer port 8888
var WebSocketServer = require('ws').Server;
var wss = new WebSocketServer({port:8888});
var messages = 0;

const server = wss._server;

//var webSocketServer = new WebSocketServer.Server({server: '0.0.0.0', port: 8888});

  
wss.on('connection', function(ws) {

  var id = Math.random();
  clients[id] = ws;
  console.log("New client: " + id);

  ws.on('message', function(message) {
    console.log('Got message: ' + message);
	messages += 1;
	
	fs.writeFile("../heart-rate.txt", message, function(err) {
      if(err) {
        return console.log(err);
      }

      console.log("The file was saved!", messages);
	}); 

    //for(var key in clients) {
    //  clients[key].send(message);
	//  console.log('Connection closed ' + id);
	//  //delete clients[id];
    //}
  });

  ws.on('close', function() {
    //console.log('Connection closed ' + id);
	server.close();
	setTimeout(function(){
        wss = new WebSocketServer({port:8888});
    }, 10000);
    delete clients[id];
  });

});


// статический сервер на 8080
/*var fileServer = new Static.Server('.');
http.createServer(function (req, res) {
  
  fileServer.serve(req, res);

}).listen(8080);*/

console.log("Сервер запущен на порте 8888");

