####AngularJS 扩展了 HTML

AngularJS 通过 ng-directives 扩展了 HTML。
__ng-app__ 指令定义一个 AngularJS 应用程序。
__ng-model__ 指令把元素值（比如输入域的值）绑定到应用程序。
__ng-bind__ 指令把应用程序数据绑定到 HTML 视图。

####AngularJS 表达式

AngularJS 表达式写在双大括号内：{{ expression }}。
AngularJS 表达式把数据绑定到 HTML，这与 ng-bind 指令有异曲同工之妙。
AngularJS 将在表达式书写的位置"输出"数据。
AngularJS 表达式 很像 JavaScript 表达式：它们可以包含文字、运算符和变量。
实例 {{ 5 + 5 }} 或 {{ firstName + " " + lastName }}

####AngularJS 应用

AngularJS 模块（Module） 定义了 AngularJS 应用。
AngularJS 控制器（Controller） 用于控制 AngularJS 应用。
ng-app指令定义了应用, ng-controller 定义了控制器。

```js
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="http://cdn.static.runoob.com/libs/angular.js/1.4.6/angular.min.js"></script> 
</head>
<body>

<p>尝试修改以下表单。</p>

<div ng-app="myApp" ng-controller="myCtrl">

名: <input type="text" ng-model="firstName"><br>
姓: <input type="text" ng-model="lastName"><br>
<br>
姓名: {{firstName + " " + lastName}}

</div>

<script>
var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope) {
    $scope.firstName= "John";
    $scope.lastName= "Doe";
});
</script>

</body>
```

###创建自定义的指令
除了 AngularJS 内置的指令外，我们还可以创建自定义指令。
你可以使用 .directive 函数来添加自定义的指令。
要调用自定义指令，HTML 元素上需要添加自定义指令名。
使用驼峰法来命名一个指令， runoobDirective, 但在使用它时需要以 - 分割, runoob-directive:
```js
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="http://cdn.static.runoob.com/libs/angular.js/1.4.6/angular.min.js"></script> 
</head>
<body ng-app="myApp">


<runoob-directive/>
<script>
var app = angular.module("myApp", []);
app.directive("runoobDirective", function() {
    return {
        template : "<h1>自定义指令!</h1>"
    };
});
```

调用：
```
<runoob-directive></runoob-directive>
<div runoob-directive></div>
<div class="runoob-directive"></div>
<!-- directive: runoob-directive -->
```

限制使用：
```js
var app = angular.module("myApp", []);
app.directive("runoobDirective", function() {
    return {
        restrict : "A",
        template : "<h1>自定义指令!</h1>"
    };
});
```
restrict：
* E 元素名
* A 属性名
* C 类名
* M 注释

####验证用户输入
```js
<form ng-app="" name="myForm">
    Email:
    <input type="email" name="myAddress" ng-model="text">
    <span ng-show="myForm.myAddress.$error.email">不是一个合法的邮箱地址</span>
</form>
```


ng-model 指令根据表单域的状态添加/移除以下类：

* ng-empty
* ng-not-empty
* ng-touched
* ng-untouched
* ng-valid
* ng-invalid
* ng-dirty
* ng-pending
* ng-pristine

###作用域
Scope(作用域) 是应用在 HTML (视图) 和 JavaScript (控制器)之间的纽带。
Scope 是一个对象，有可用的方法和属性。
Scope 可应用在视图和控制器上。

####AngularJS 过滤器
currency    格式化数字为货币格式。
filter      从数组项中选择一个子集。
lowercase   格式化字符串为小写。
orderBy     根据某个表达式排列数组。
uppercase   格式化字符串为大写。

#####向指令添加过滤器
```
 <div ng-app="myApp" ng-controller="namesCtrl">

<ul>
  <li ng-repeat="x in names | orderBy:'country'">
    {{ x.name + ', ' + x.country }}
  </li>
</ul>

</div> 
```

#####自定义过滤器
```

var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope) {
    $scope.msg = "Runoob";
});
app.filter('reverse', function() { //可以注入依赖
    return function(text) {
        return text.split("").reverse().join("");
    }
});
```

#####AngularJS 服务(Service) 
在 AngularJS 中，服务是一个函数或对象，可在你的 AngularJS 应用中使用。
AngularJS 内建了30 多个服务。
有个 $location 服务，它可以返回当前页面的 URL 地址。

$http 是 AngularJS 应用中最常用的服务。 服务向服务器发送请求，应用响应服务器传送过来的数据。
```
var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope, $http) {
    $http.get("welcome.htm").then(function (response) {
        $scope.myWelcome = response.data;
    });
});
```
AngularJS $timeout 服务对应了 JS window.setTimeout 函数。
AngularJS $interval 服务对应了 JS window.setInterval 函数
```
var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope, $interval) {
    $scope.theTime = new Date().toLocaleTimeString();
    $interval(function () {
        $scope.theTime = new Date().toLocaleTimeString();
    }, 1000);
});
```

你可以创建访问自定义服务，链接到你的模块中：
```
app.service('hexafy', function() {
    this.myFunc = function (x) {
        return x.toString(16);
    }
});
```

####HTTP

    $http.get
    $http.head
    $http.post
    $http.put
    $http.delete
    $http.jsonp
    $http.patch

####AngularJS Select(选择框)
在 AngularJS 中我们可以使用 ng-option 指令来创建一个下拉列表，列表项通过对象和数组循环输出，如下实例:
```

<div ng-app="myApp" ng-controller="myCtrl">
 
<select ng-init="selectedName = names[0]" ng-model="selectedName" ng-options="x for x in names">
</select>
 
</div>
 
<script>
var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope) {
    $scope.names = ["Google", "Runoob", "Taobao"];
});
</script>
```

我们也可以使用ng-repeat 指令来创建下拉列表：
```
<select>
<option ng-repeat="x in names">{{x}}</option>
</select>
```
ng-repeat 有局限性，选择的值是一个字符串:
使用 ng-options 指令，选择的值是一个对象：
```
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="http://cdn.static.runoob.com/libs/angular.js/1.4.6/angular.min.js"></script>
</head>
<body>

<div ng-app="myApp" ng-controller="myCtrl">

<p>选择的网站是:</p>

<select ng-model="selectedSite" ng-options="x for (x, y) in sites">
</select>

<h1>你选择的值是: {{selectedSite}}</h1>

</div>

<p>该实例演示了使用对象作为创建下拉列表。</p>

<script>
var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope) {
    $scope.sites = {
        site01 : "Google",
        site02 : "Runoob",
        site03 : "Taobao"
    };
});
</script>

</body>
</html>
```
####AngularJS 表格
ng-repeat 指令可以完美的显示表格。
```
<table>
  <tr ng-repeat="x in names">
    <td>{{ x.Name }}</td>
    <td>{{ x.Country }}</td>
  </tr>
</table>
```

表格显示序号可以在 <td> 中添加 $index:  
```
 <table>
  <tr ng-repeat="x in names">
    <td>{{ $index + 1 }}</td>
    <td>{{ x.Name }}</td>
    <td>{{ x.Country }}</td>
  </tr>
</table> 
```

使用 $even 和 $odd
```
 <table>
<tr ng-repeat="x in names">
<td ng-if="$odd" style="background-color:#f1f1f1">{{ x.Name }}</td>
<td ng-if="$even">{{ x.Name }}</td>
<td ng-if="$odd" style="background-color:#f1f1f1">{{ x.Country }}</td>
<td ng-if="$even">{{ x.Country }}</td>
</tr>
</table> 
```

####ng-disabled 指令

```
 <div ng-app="" ng-init="mySwitch=true">
<p>
<button ng-disabled="mySwitch">点我!</button>
</p>
<p>
<input type="checkbox" ng-model="mySwitch">按钮
</p>
<p>
{{ mySwitch }}
</p>
</div> 
```

ng-show 指令隐藏或显示一个 HTML 元素。
ng-show 指令根据 value 的值来显示（隐藏）HTML 元素。
你可以使用表达式来计算布尔值（ true 或 false）:
```
<div ng-app="" ng-init="hour=13">
<p ng-show="hour > 12">我是可见的。</p>
</div>
```
ng-hide 指令用于隐藏或显示 HTML 元素。

###AngularJS 事件
ng-click 指令定义了 AngularJS 点击事件。 
```
 <div ng-app="" ng-controller="myCtrl">

<button ng-click="count = count + 1">点我！</button>

<p>{{ count }}</p>

</div>
```
##AngularJS 模块
模块定义了一个应用程序。
模块是应用程序中不同部分的容器。
模块是应用控制器的容器。
控制器通常属于一个模块。

你可以通过 AngularJS 的 angular.module 函数来创建模块

JavaScript 中应避免使用全局函数。因为他们很容易被其他脚本文件覆盖。
AngularJS 模块让所有函数的作用域在该模块下，避免了该问题。
##AngularJS Bootstrap
如果站点在国内，建议使用百度静态资源库的Bootstrap，代码如下：
```
<link rel="stylesheet" href="//apps.bdimg.com/libs/bootstrap/3.3.4/css/bootstrap.min.css"> 
```

###包含 AngularJS 代码
ng-include 指令除了可以包含 HTML 文件外，还可以包含 AngularJS 代码:
默认情况下， ng-include 指令不允许包含其他域名的文件。
如果你需要包含其他域名的文件，你需要设置域名访问白名单：\
```

<body ng-app="myApp">
 
<div ng-include="'http://c.runoob.com/runoobtest/angular_include.php'"></div>
 
<script>
var app = angular.module('myApp', [])
app.config(function($sceDelegateProvider) {
    $sceDelegateProvider.resourceUrlWhitelist([
        'http://c.runoob.com/runoobtest/**'
    ]);
});
</script>
 
</body>
```

####AngularJS 动画 
AngularJS 提供了动画效果，可以配合 CSS 使用。
AngularJS 使用动画需要引入 angular-animate.min.js 库。


####AngularJS 依赖注入
AngularJS 提供很好的依赖注入机制。以下5个核心组件用来作为依赖注入：

    value
    factory
    service
    provider
    constant

Value 是一个简单的 javascript 对象，用于向控制器传递值（配置阶段）： 
```
// 定义一个模块
var mainApp = angular.module("mainApp", []);

// 创建 value 对象 "defaultInput" 并传递数据
mainApp.value("defaultInput", 5);
...

// 将 "defaultInput" 注入到控制器
mainApp.controller('CalcController', function($scope, CalcService, defaultInput) {
   $scope.number = defaultInput;
   $scope.result = CalcService.square($scope.number);
   
   $scope.square = function() {
      $scope.result = CalcService.square($scope.number);
   }
});
```

factory 是一个函数用于返回值。在 service 和 controller 需要时创建。
通常我们使用 factory 函数来计算或返回值。
```
// 定义一个模块
var mainApp = angular.module("mainApp", []);

// 创建 factory "MathService" 用于两数的乘积 provides a method multiply to return multiplication of two numbers
mainApp.factory('MathService', function() {
   var factory = {};
   
   factory.multiply = function(a, b) {
      return a * b
   }
   return factory;
}); 

// 在 service 中注入 factory "MathService"
mainApp.service('CalcService', function(MathService){
   this.square = function(a) {
      return MathService.multiply(a,a);
   }
});
```

AngularJS 中通过 provider 创建一个 service、factory等(配置阶段)。
Provider 中提供了一个 factory 方法 get()，它用于返回 value/service/factory。

```
// 定义一个模块
var mainApp = angular.module("mainApp", []);
...

// 使用 provider 创建 service 定义一个方法用于计算两数乘积
mainApp.config(function($provide) {
   $provide.provider('MathService', function() {
      this.$get = function() {
         var factory = {};  
         
         factory.multiply = function(a, b) {
            return a * b; 
         }
         return factory;
      };
   });
});
```

constant(常量)用来在配置阶段传递数值，注意这个常量在配置阶段是不可用的。
```
mainApp.constant("configParam", "constant value");
```

###AngularJS 路由
AngularJS 路由允许我们通过不同的 URL 访问不同的内容。
通过 AngularJS 可以实现多视图的单页Web应用（single page web application，SPA）。
通常我们的URL形式为 http://runoob.com/first/page，但在单页Web应用中 AngularJS 通过 # + 标记 实现，例如：
```
http://runoob.com/#/first
http://runoob.com/#/second
http://runoob.com/#/third
```

![Alt text](http://www.runoob.com/wp-content/uploads/2016/04/angular-routing11.png)

```
<html>
    <head>
        <meta charset="utf-8">
        <title>AngularJS 路由实例 - 菜鸟教程</title>
    </head>
    <body ng-app='routingDemoApp'>
     
        <h2>AngularJS 路由应用</h2>
        <ul>
            <li><a href="#/">首页</a></li>
            <li><a href="#/computers">电脑</a></li>
            <li><a href="#/printers">打印机</a></li>
            <li><a href="#/blabla">其他</a></li>
        </ul>
         
        <div ng-view></div>
        <script src="http://cdn.static.runoob.com/libs/angular.js/1.4.6/angular.min.js"></script>
        <script src="https://apps.bdimg.com/libs/angular-route/1.3.13/angular-route.js"></script>
        <script>
            angular.module('routingDemoApp',['ngRoute'])
            .config(['$routeProvider', function($routeProvider){
                $routeProvider
                .when('/',{template:'这是首页页面'})
                .when('/computers',{template:'这是电脑分类页面'})
                .when('/printers',{template:'这是打印机页面'})
                .otherwise({redirectTo:'/'});
            }]);
        </script>
     
     
    </body>
</html>
```

AngularJS 路由也可以通过不同的模板来实现。
$routeProvider.when 函数的第一个参数是 URL 或者 URL 正则规则，第二个参数为路由配置对象。
路由配置对象语法规则如下：
```
$routeProvider.when(url, {
    template: string,
    templateUrl: string,
    controller: string, function 或 array,
    controllerAs: string,
    redirectTo: string, function,
    resolve: object<key, function>
});
```
