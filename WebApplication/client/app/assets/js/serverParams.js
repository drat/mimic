var server = null;
/*
if(window.location.protocol === 'http:')
	server = "http://" + window.location.hostname + ":8088/janus";
else
	server = "https://" + window.location.hostname + ":8089/janus";
*/

const ec2 = "18.235.63.230";

const ext= "/janus";

var ws_server = "ws://" + ec2 + ":8188/";
var http_server = "http://" + ec2 + ":8088" + ext;
var servers= [ws_server, http_server];

var server = servers[1];
