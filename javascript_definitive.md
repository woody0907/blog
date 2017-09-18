[TOC]
### Lexical Structure

#### Optional Semicolons
javascript usually treat line breaks as semicolons only if it can't parse the code without the semicolons.

``` javascript

	var a
	a
	=
	3
	console.log(a)
	//javascript interprets this code like this:
	var a;
	a = 3; //it can continue parsing the longer statement
	console.log(a);

```
There are two exceptions to the general rule that javascript interprets line breaks as semicolon when it cannot parse the line as a continuation of the statment on the first line. The first exception involves the **reture**,**break**,**continue** statements.
The second exception involves the **++**,**--** operator.

### Types
#### Numbers
All number in javascript are represented as floating-point values. Javascript represents numbers using 64-bit floating format.
##### Integer Literals
hexadecimal 0x 0X
octal 0
##### Floating-Point Literals
[digits].[digits][E|e][(+|-)]digits]

	Infinity // A read/write variable initialized to Infinity.
	Number.POSITIVE_INFINITY // Same value, read-only.
	1/0 // This is also the same value.
	Number.MAX_VALUE + 1 // This also evaluates to Infinity.
	Number.NEGATIVE_INFINITY // These expressions are negative infinity.
	-Infinity
	-1/0
	-Number.MAX_VALUE - 1
	NaN // A read/write variable initialized to NaN.
	Number.NaN // A read-only property holding the same value.
	0/0 // Evaluates to NaN.
	Number.MIN_VALUE/2 // Underflow: evaluates to 0
	-Number.MIN_VALUE/2 // Negative zero
	-1/Infinity // Also negative 0
	-0
JavaScript numbers have plenty of precision and can be approximations 0.1 very close. But the fact that this number cannot be represented exactly can lead to problems. Consider this code:
	
	var x = .3 - .2;
	var y = .2 - .1;
	x==y; //false
	x==.1;//false
	y==.1;//true

#### Dates and Times

	var then = new Date(2010, 0, 1); // The 1st day of the 1st month of 2010
	var later = new Date(2010, 0, 1, // Same day, at 5:10:30pm, local time
	 17, 10, 30);
	var now = new Date(); // The current date and time
	var elapsed = now - then; // Date subtraction: interval in milliseconds
	later.getFullYear() // => 2010
	later.getMonth() // => 0: zero-based months
	later.getDate() // => 1: one-based days
	later.getDay() // => 5: day of week. 0 is Sunday 5 is Friday.
	later.getHours() // => 17: 5pm, local time
	later.getUTCHours() // hours in UTC time; depends on timezone
	later.toString() // => "Fri Jan 01 2010 17:10:30 GMT-0800 (PST)"
	later.toUTCString() // => "Sat, 02 Jan 2010 01:10:30 GMT"
	later.toLocaleDateString() // => "01/01/2010"
	later.toLocaleTimeString() // => "05:10:30 PM"
	later.toISOString() // => "2010-01-02T01:10:30.000Z"; ES5 only

#### Text

A String is an immutable ordered sequence of 16-bit values, each of which typically represents a unicode character. 

#### Escape Sequences in String Literals

	Sequence Character represented
	\0 The NUL character (\u0000)
	\b Backspace (\u0008)
	\t Horizontal tab (\u0009)
	\n Newline (\u000A)
	\v Vertical tab (\u000B)
	\f Form feed (\u000C)
	\r Carriage return (\u000D)
	\" Double quote (\u0022)
	\' Apostrophe or single quote (\u0027)
	\\ Backslash (\u005C)
	\x XX The Latin-1 character specified by the two hexadecimal digits XX
	\u XXXX The Unicode character specified by the four hexadecimal digits XXXX


#### Pattern Matching

	/^HTML/ // Match the letters H T M L at the start of a string
	/[1-9][0-9]*/ // Match a non-zero digit, followed by any # of digits
	/\bjavascript\b/i // Match "javascript" as a word, case-insensitive

	var text = "testing: 1, 2, 3"; // Sample text
	var pattern = /\d+/g // Matches all instances of one or more digits
	pattern.test(text) // => true: a match exists
	text.search(pattern) // => 9: position of first match
	text.match(pattern) // => ["1", "2", "3"]: array of all matches
	text.replace(pattern, "#"); // => "testing: #, #, #"
	text.split(/\D+/); // => ["","1","2","3"]: split on non-digits

#### Null and undefined

Using the typeof operator on null returns the string 'object', indicates that null can be thought of a special value that indicates 'no object'.

The undefined value represents a deeper kind of absence. It is the value of variables that have not been initialized and the value you get when you query the value of an object property or array element that does not exist.

#### The Global Object

The properties of this object are the globally defined symbols that are available to a javascript program.

	global properties like undefined, Infinity, and NaN
	global functions like isNaN(), parseInt(), and eval() 
	constructor functions like Date(), RegExp(), String(), Object(), and Array()
	global objects like Math and JSON

#### Wrapper Objects

String Number Boolean

Consider the following code:

	var s = "test";
	var s.len = 4;
	var t = s.len;//undefined

When you run this code, the value of t is undefined.
This code demostrate that the strings, numbers and boolean values behave like ojbects when you try to read the value of a property from them. But if you attemp to set value of a property, that attempt is silently ignored: the change is made on a temporary and does not persist.
You just need to know that string,number,boolean values differ from objects in that their properties are read-only and that you can't define new properties on them.

#### Object to primitive conversions

To convert an object to a string, Javascript take these steps:
1. If object has a toString(), then calls it;
2. If object has no toString, then looks for valueOf();
3. If object cannot obtain either toString() or valueOf() so it throws a TypeError.
To convert an object to a number, Javasript does the same thing, but it tries the valueOf() method first.

The **+** operator in javascript performs numeric addition and string concatenation. If either of its operants is an object, javascript converts the object using special object-to-primitive conversion.

	var now = new Date(); // Create a Date object
	typeof (now + 1) // => "string": + converts dates to strings
	typeof (now - 1) // => "number": - uses object-to-number conversion
	now == now.toString() // => true: implicit and explicit string conversions
	now > (now -1) // => true: > converts a Date to a number


#### Variable Scope
	
Although you can get away with not using the var statement when you write code in the globle scope, you must always use var to declare local varibles.
Function definitions can be nested. Each function has its own local scope, so it is possible to have several nested layers of local scope.	

#### Function scope and Hoisting

Javascript uses function scope: varibles are visible whin the function in which they are defined and within any function that are nested within that function:

Javascript's function scope means that all variables declared within a function are visible throughout the body of the function. Curiously, this means that variables are even visible before they are declared. This feature is informally known as hoisting. Javascript code behaves as if all variable  declarations in a function (but not any associated assignments) are hoisted to the top of the function.

	var scope = "global";
	function(f){
		console.log(scope);  
		var scope = "local";
		console.log(scope);
	}

	var scope = "globle";
	function(f){
		var scope;
		console.log(scope);
		scope = "local";
		console.log(scope);
	}

#### Variables as properties

When you declare a global variable, what you are actually doing is defining a property of the global object. If you use var to declare, the property that is created id nonconfigurable,which means that it cannot be deleted.

	var truevar = 1; // A properly declared global variable, nondeletable.
	fakevar = 2; // Creates a deletable property of the global object.
	this.fakevar2 = 3; // This does the same thing.
	delete truevar // => false: variable not deleted
	delete fakevar // => true: variable deleted
	delete this.fakevar2 // => true: variable deleted

#### The Scope Chain

In top level javascript code the scope chain consists of a single object, the global object.
In none nested function, the scope chain consists of two objects, the first is the object that define the function's parameters and local variables, and the second is the globle object.
In nested function, the scope chain has three or more object. 

It is important to understand how this chain of objects is created. When a function is created, it stores the scope chain and in effect. When the function is invoked, it creates a new object to store its local variables, and adds the new object to the stored scope chain to create a new, longer, chain that reprents the scope for that function invocation.


### Operater and Expression

#### the in operator

	var point = { x:1, y:1 }; // Define an object
	"x" in point // => true: object has property named "x"
	"z" in point // => false: object has no "z" property.
	"toString" in point // => true: object inherits toString method
	var data = [7,8,9]; // An array with elements 0, 1, and 2
	"0" in data // => true: array has an element "0"
	1 in data // => true: numbers are converted to strings
	3 in data // => false: no element 3

#### the instanceof operator

	var d = new Date(); // Create a new object with the Date() constructor
	d instanceof Date; // Evaluates to true; d was created with Date()
	d instanceof Object; // Evaluates to true; all objects are instances of Object
	d instanceof Number; // Evaluates to false; d is not a Number object
	var a = [1, 2, 3]; // Create an array with array literal syntax
	a instanceof Array; // Evaluates to true; a is an array
	a instanceof Object; // Evaluates to true; all arrays are objects
	a instanceof RegExp; // Evaluates to false; arrays are not regular expressions

#### Evaluation Expressions

Like many interpreted languages, javascript has the ability to interpret strings of javascript source code, evaluating them to produce a value. javascript does this with the global function eval()

#### The void operator

it evaluates its operand, then discard the value and return undefined.

### Statements

#### switch

When all of the branches depend on the value of the same expression, it is preffer using switch  than using if statement

#### loops

while, do/while, for, for/in

#### labled statement

identifier: statement

#### with

The with statement is used to temporarily extend the scope chain, this statement adds object to the front of the scope chain, execute statement, and then restores the scope chain to its original state.

the with statement is forbidden in the strict mode and should be considered deprecated in non-strict mode

	with(document.forms[0]) {
	// Access form elements directly here. For example:
	name.value = "";
	address.value = "";
	email.value = "";
	}

	var f = document.forms[0];
	f.name.value = "";
	f.address.value = "";
	f.email.value = "";

### Object

#### Creating Objects
- Object Literals

```
	var empty = {}; // An object with no properties
	var point = { x:0, y:0 }; // Two properties
	var point2 = { x:point.x, y:point.y+1 }; // More complex values
	var book = {
	"main title": "JavaScript", // Property names include spaces,
	'sub-title': "The Definitive Guide", // and hyphens, so use string literals
	"for": "all audiences", // for is a reserved word, so quote
	author: { // The value of this property is
	firstname: "David", // itself an object. Note that
	surname: "Flanagan" // these property names are unquoted.
	}
	};
```
- Creating Object with new 