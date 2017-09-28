##Connect
Connect is a framework which uses modular components called "middleware" to implement web application logic in a reusable manner.

    npm install connect

###Middleware that does logging

```js
function logger(req,res,next){
    console.log('%s %s',req.method,req.url)
    next();
}

var connect = require('connect');
var app = connect();
app.use(logger);
app.listen(300);
```

***********************************

###A middleware that responses with "hello world"
```js
function hello(req,res){
    res.setHeader('Content-Type','text/plain');
    res.end("hello world");
}

var connect = require('connect');
connect().use(logger).use(hello).listen(3000);
```

the moral here is that when a middleware does not call next() then any remaining middleware after it in the chain of command will not be invoked

###Mounting Middleware & Server
```js
var connenct = require('connect');
connect().use(logger)
.use('/admin',restrict)
.use('/admin',admin)
.use(hello)
.listen(3000)
```

###Creating configurable middleware
####Creating a configurable logger middleware
```js
in the logger.js
function setup(format){
    var regexp = /:(\w)+/g;
    return function logger(req,res,next){
        var str = format.replace(regexp,function(match,property){
            return req[property];
            });
        console.log(str);
    }
}
module.exports = setup;
```

###Cross-site request forgery protection

    connect()
    .use(connect.bodyParser())
    .use(connect.cookieParser('secret'))
    .use(connect.session())
    .use(connect.csrf());

