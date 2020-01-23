require('rootpath')();
var express = require('express');
var app = express();
const https = require('https');
const fs = require('fs');
var cors = require('cors');
var bodyParser = require('body-parser');
var expressJwt = require('express-jwt');
var config = require('config.json');


//const TelegramBot = require('node-telegram-bot-api');
//const token = '921969059:AAHEsjXkp10M3JOZyhiRoODIyWFpQ_dCUYs';
//const bot = new TelegramBot(token, {polling: true});
//c/onst chatId = '941853127';
//bot.sendVideo(chatId, '../client/app/assets/video/video.mp4')


app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// use JWT auth to secure the api, the token can be passed in the authorization header or querystring
app.use(expressJwt({
    secret: config.secret,
    getToken: function (req) {
        if (req.headers.authorization && req.headers.authorization.split(' ')[0] === 'Bearer') {
            return req.headers.authorization.split(' ')[1];
        } else if (req.query && req.query.token) {
            return req.query.token;
        }
        return null;
    }
}).unless({ path: ['/users/authenticate', '/users/register'] }));

// routes
app.use('/users', require('./controllers/users.controller'));

// error handler
app.use(function (err, req, res, next) {
    if (err.name === 'UnauthorizedError') {
        res.status(401).send('Invalid Token');
    } else {
        throw err;
    }
});

// start server (NOT HTTPS)
var port = process.env.NODE_ENV === 'production' ? 80 : 4000;
//var server = app.listen(port, function () { console.log('Server listening on port ' + port); });



// we will pass our 'app' to 'https' server (HTTPS)
https.createServer({
    key: fs.readFileSync('C:\\Users\\tony\\Documents\\projects\\HTTPSforProjects\\client-1.local.key'),
    cert: fs.readFileSync('C:\\Users\\tony\\Documents\\projects\\HTTPSforProjects\\client-1.local.crt'),
    passphrase: 'tony'
}, app)
.listen(port);