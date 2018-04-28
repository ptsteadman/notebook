# JavaScript Notes

### Meta

TC-39: ECMA working group

Stage 0 - Strawman:
only reviewed at a TC-39

Stage 1 - Proposal:
Champion
Solves Problem
API
Concerns

Stage 2 - Draft:
Formal semantics / syntax

Stage 3 - Candidate:
spec text
two implementations

Stage 4:



### Functions

Anonymous closures `(function(){}())` require the outer parentheses because
without the parentheses it is evaluated as a FunctionDeclaration rather than a
FunctionExpression, and anonymous FunctionDeclarations are not allowed. 

### Modules

#### Non-Native Solutions

Problems solved over just loading modules into global scope: ordering of module
loading, namespace collisions, versioning, making dependcies explicit.

__What is CommonJS?__  It's a 'volunteer working group that designs and
implements JavaScript APIs for declaring modules.

"A CommonJS module is essentially a reusable piece of JavaScript which exports
specific objects, making them available for other modules to require in their
programs. If you’ve programmed in Node.js, you’ll be very familiar with this
format.

With CommonJS, each JavaScript file stores modules in its own unique module
context (just like wrapping it in a closure). In this scope, we use the
module.exports object to expose modules, and require to import them."

[source](https://medium.freecodecamp.com/javascript-modules-a-beginner-s-guide-783f7d7a5fcc#.ti2j1lji9)

__Problem with CommonJS:__ modules are loaded synchronously.  Bad for
browser/web.

__What is AMD?__ Async module loading.

Looks like: `define(['modules'], function(modules){});`

__What is UMD?__ Boilerplate that lets you mix CommonJS and AMD.

#### Native ES6 Modules

Native ES6 Modules let us avoid some of the problems of CommonJS and AMD (which
aren't 'native' to the language), and work well with React because of the the
implied Babel step necessary for JSX.

Async, and supports read-only views of modules.  (Don't really understand the
use of the latter.)

Syntax:

```
// Default exports and named exports
import theDefault, { named1, named2 } from 'src/mylib';
import theDefault from 'src/mylib';
import { named1, named2 } from 'src/mylib';

// Renaming: import named1 as myNamed1
import { named1 as myNamed1, named2 } from 'src/mylib';

// Importing the module as an object
// (with one property per named export)
import * as mylib from 'src/mylib';

// Only load the module, don’t import anything
import 'src/mylib';


export var myVar1 = ...;
export let myVar2 = ...;
export const MY_CONST = ...;

export function myFunc() {
    ...
}
export function* myGeneratorFunc() {
    ...
}
export class MyClass {
    ...
}
```

__Braces__:

Braces allow you to export multiple variables `export { foo, bar }`.
They can then be imported using `import { foo, bar } from './foobar'`.

`export default` lets you import like `import React from 'react'`.

### This Keyword

- Implicit Binding
- Explicit Binding
- new Binding
- window Binding

Where is the function invoked?

#### Implicit Binding

Left of the dot at call time.

```
var sayNameMixin = function(obj){
  obj.sayName = function(){
    console.log(this.name);
  }
}

var me = {
  name: "Patrick",
}

var you = {
  name: "Bob",
}

sayNameMixin(me);
sayNameMixin(you);

me.sayName(); // Patrick
you.sayname(); // Bob

```

#### Explicit Binding

Using call, apply, bind.

Call: pass context, and then arguments individuallly
Apply: pass context, in arguments as an array
Bind: returns a new function that we can call later

```
var sayName = function(lang1, lang2){
  console.log('My name is ' + this.name);
}

var me = {
  name: "Patrick",
}

sayName.call(me); // My name is Patrick
```

#### new Binding

var Animal = function(color, name, type){
  // this = {}
  this.color = color;
  this.name = name;
  this.type = type;
}

#### window Binding

By default, this will default to the `window` object.
```
var sayAge = function(){
  console.log(this.age);
}

window.age = 24;
sayAge(); // 24

If `use strict` is used, it will just be undefined.
```

### Feathers

`config/default.json`

### String Encoding

charCodeAt() gets numeric unicode code point of any character up to 0xFFFF

Single character escape sequences: like `\n`, `\t`, etc
Escape character makes special characters literal

"Any character with a character code lower than 256 (i.e. any character in the extended ASCII range) can be escaped using its hex-encoded character code, prefixed with \x."

Under the hood, JS uses UCS-2, so 'astral plane' characters use two 'characters'

(Same characters as octal encoded characters.)

Unicode whatacters are prefixed with `\u`.


### var vs let

var: 
- is function scoped
- referencing before instantiation gives undefined

let
- is block scoped (ex: for loop)
- referencing before instantiation gives reference error

### generators

state machine
generator can only yield internally
'calling' a generator does not execute its code

```
function* gen() {
  console.log('hello')
  yield 1;
  console.log('world')
}

const it = gen();
it.next(); // { value: 1, done: false }
it.next();
```

for ... of is a way to iterate thru an iterator
