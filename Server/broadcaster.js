process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
var socket = require('socket.io');
var express = require('express');
var http = require('http');
var https = require('https');
var request = require('request');
var obj = require("../Shared/config.json");
var url=obj.url;
var port=obj.port;

var app = express();
app.use(express.static('../Client/UI'));

var server = http.createServer(app);
var io = socket.listen(server);

var allClients = [];
var botClientStatus = "Not connected";
var robot;
var manchesterUrl = 'https://132.203.14.228/';

io.on('connection', function (client) {
    allClients.push(socket);
    io.emit('sendBotClientStatus', botClientStatus);
    client.on('sendBotClientStatus', function(status){
        console.log(status);
        robot = client;
        botClientStatus = status;
        io.emit('sendBotClientStatus', status);
    });
    client.on('disconnect', function() {
        console.log('A client got disconnected');
        if(client == robot){
            console.log('Bad news, it\'s the bot');
            botClientStatus = "Not connected";
            io.emit('sendBotClientStatus', botClientStatus);
        }
        var i = allClients.indexOf(client);
        allClients.splice(i, 1);
    });

    client.on('sendInfo', function(data){
        io.emit('sendInfo', data);
    });

    client.on('startSignal', function(){
        io.emit('startSignal');
    });

    client.on('startSignalRobot', function(data){
        console.log("Start signal robot");
        io.emit('startSignalRobot', data);
    });

    client.on('needNewCoordinates', function(){
        io.emit('needNewCoordinates');
    });
    client.on('sendNextCoordinates', function(data){
        console.log(data);
        io.emit('sendNextCoordinates', data);
    });

    client.on('sendEndSignal', function(){
        console.log("END");
        io.emit('sendEndSignal');
    });

    client.on('sendRefusingOrderSignal', function(){
        io.emit('sendRefusingOrderSignal');
    });

    client.on('sendManchesterCode', function(data){
        request(manchesterUrl+'?code='+data, function(error, response, body) {
            manchesterInfo = {"decryptedCharacter":data, "target":JSON.parse(body)};
            io.emit('sendManchesterInfo', manchesterInfo);
        });
    });

    client.on('readManchester', function(){
        console.log('readManchester');
        io.emit('readManchester');
    });

    client.on('startFromTarget', function(){
        io.emit('startFromTarget');
    });

    client.on('startFromTreasure', function(){
        console.log("retransmitting start treasure command");
        io.emit('startFromTreasure');
    });

    client.on('sendBotIP', function(data){
        console.log(data);
    });
    client.on('alignPositionToChargingStation', function(json){
        io.emit('alignPositionToChargingStation', json);
    });
    client.on('alignPositionToTreasure', function(json){
        io.emit('alignPositionToTreasure', json);
    });
    client.on('alignPositionToTarget', function (json){
        console.log('align position to target ' + json['angleToGo'])
        io.emit('alignPositionToTarget', json);
    });
    client.on('detectTreasure', function(jsonAngles){
        console.log(jsonAngles);
        io.emit('detectTreasure', jsonAngles);
    });
    client.on('setTreasures', function(data){
        console.log("sending treasures ");
        io.emit('setTreasures', data);
    });
    client.on('rotateToChargingStation', function(angles){
        io.emit('rotateToChargingStation', angles);
    });
    client.on('rotateDoneToChargingStation', function(isInSequence){
        io.emit('rotateDoneToChargingStation', isInSequence);
    });
    client.on('rotateToTreasure', function(angles){
        io.emit("rotateToTreasure", angles);
    });
    client.on("rotateDoneToTreasure", function(){
        io.emit('rotateDoneToTreasure');
    });





    //debug section
    client.on("debugAlignBotToTarget", function(){
        io.emit('debugAlignBotToTarget');
    });
    client.on("debugSendBotToTarget", function(){
        io.emit('debugSendBotToTarget');
    });
    client.on("debugAlignBotToTreasure", function(){
        io.emit('debugAlignBotToTreasure');
    });
    client.on("debugSendBotToTreasure", function(){
        io.emit('debugSendBotToTreasure');
    });
    client.on("debugSearchAllTreasure", function(){
        io.emit('debugSearchAllTreasure');
    });
    client.on("debugAlignBotToChargingStation", function(){
        io.emit('debugAlignBotToChargingStation');
    });
    client.on("debugSendBotToChargingStation", function(){
        io.emit('debugSendBotToChargingStation');
    });
    client.on("initializeWorld", function(){
        io.emit('initializeWorld');
    });
});

server.listen(port, url);


