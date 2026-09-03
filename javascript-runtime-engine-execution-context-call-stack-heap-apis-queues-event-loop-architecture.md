# 1. Js runtime vs js engine vs event loop


Think of it like this:

**JavaScript engine = executes JavaScript code**

The engine is the thing that understands and runs JS.

Examples:

| Environment   | JS engine      |
| ------------- | -------------- |
| Chrome / Edge | V8             |
| Node.js       | V8             |
| Firefox       | SpiderMonkey   |
| Safari        | JavaScriptCore |

The engine gives you core JS features:

```js
const x = 1;
function add(a, b) {
  return a + b;
}
Promise.resolve()
```

It handles parsing, execution, memory, call stack, heap, garbage collection, etc.

But the engine alone does **not** give you things like:

```js
setTimeout()
fetch()
document.querySelector()
fs.readFile()
```

Those come from the runtime.

---

**JavaScript runtime = engine + environment APIs + event loop**

A runtime is the full environment where JavaScript runs.

Browser runtime:

```text
V8 / SpiderMonkey / JavaScriptCore
+ DOM APIs
+ Web APIs
+ fetch
+ setTimeout
+ event loop
```

Node.js runtime:

```text
V8
+ Node APIs
+ fs
+ http
+ crypto
+ timers
+ libuv
+ event loop
```

So yes: **Node.js is a JavaScript runtime**, and the **browser is also a JavaScript runtime**.

They may use the same engine, like V8, but they expose different APIs.

That is why this works in the browser:

```js
document.querySelector("button")
```

But not in Node.js.

And this works in Node.js:

```js
fs.readFile("file.txt")
```

But not in the browser.

---

**Event loop = coordination system for async work**

JavaScript itself is single-threaded at the execution level: one call stack runs JS code at a time.

But async work is handled by the runtime.

Example:

```js
console.log("A");

setTimeout(() => {
  console.log("B");
}, 0);

Promise.resolve().then(() => {
  console.log("C");
});

console.log("D");
```

Flow:

```text
1. JS engine runs sync code on call stack
2. Runtime handles async APIs like setTimeout/fetch/fs
3. Finished async callbacks go into queues
4. Event loop moves queued callbacks back to the call stack
5. Engine executes them
```

Output:

```text
A
D
C
B
```

Because:

```text
Sync code first
Promise microtasks next
setTimeout macrotasks after
```

---

The connected mental model:

```text
Your JS code
   ↓
JavaScript engine executes it
   ↓
If async/browser/Node API is used, runtime handles it
   ↓
Callback/promise result waits in a queue
   ↓
Event loop schedules it back to the engine
   ↓
Engine executes the callback
```

So the clean distinction is:

| Concept            | Meaning                          |
| ------------------ | -------------------------------- |
| JavaScript engine  | Runs JavaScript code             |
| JavaScript runtime | Engine + APIs + event loop       |
| Event loop         | Decides when async callbacks run |
| Browser            | Runtime for frontend JS          |
| Node.js            | Runtime for server-side JS       |

Shortest version:

> The **engine** runs JS. The **runtime** provides the world around JS. The **event loop** connects async runtime work back into the single JS execution thread.



# 2. Where call stack sits in above grand scheme of things

Yes, you are very close. The missing dot is:

> The **call stack does not execute code by itself**.
> The **JavaScript engine executes code using the call stack**.

So the call stack is like the engine’s current “to-do stack”.

**Grand Picture**

```text
JavaScript Runtime
├── JavaScript Engine
│   ├── Call Stack
│   ├── Heap / Memory
│   └── Executes JS code
│
├── Runtime APIs
│   ├── setTimeout
│   ├── fetch
│   ├── DOM events / Node fs
│
└── Event Loop
    ├── Watches queues
    └── Sends callbacks to engine when stack is empty
```

So:

| Part         | Job                                     |
| ------------ | --------------------------------------- |
| Runtime      | Whole environment                       |
| Engine       | Actually runs JS                        |
| Call stack   | Tracks currently running function calls |
| Runtime APIs | Handle async work outside the stack     |
| Event loop   | Moves ready callbacks into execution    |
| Queue        | Waiting area for callbacks              |

---

When we say:

> “The call stack executes code”

That is a simplified phrase.

More accurate:

> The **engine executes code**, and the **call stack tracks what function is currently being executed**.

Example:

```js
function a() {
  b();
}

function b() {
  console.log("hello");
}

a();
```

Flow:

```text
push a() onto stack
push b() onto stack
push console.log() onto stack
run console.log
pop console.log
pop b
pop a
```

The stack answers:

```text
Where am I right now?
Which function called this function?
Where do I return after this finishes?
```

---

Important point:

**Async callback does not execute asynchronously.**

This sounds strange, but it is key.

```js
setTimeout(() => {
  console.log("timeout");
}, 1000);
```

The timer runs outside the call stack.

But when the callback finally runs, it runs like normal synchronous JS on the call stack.

So async means:

> The callback is scheduled asynchronously, but once it starts executing, it executes synchronously on the call stack.

---

Example:

```js
console.log("A");

setTimeout(() => {
  console.log("B");
}, 0);

console.log("C");
```

Flow:

```text
1. Engine starts global code on call stack
2. console.log("A") runs
3. setTimeout is given to runtime API
4. console.log("C") runs
5. Global code finishes, stack becomes empty
6. Event loop sees timer callback is ready
7. Event loop sends callback to call stack
8. Engine executes callback
9. console.log("B") runs
```

Output:

```text
A
C
B
```

---

So the most precise mental model is:

```text
Runtime provides the environment.
Engine executes JavaScript.
Call stack tracks active execution.
Async APIs handle work outside the engine.
Queues store completed async callbacks.
Event loop waits for the call stack to be empty, then schedules queued callbacks.
```

# 3. How Heap memory, GEC(global execution context) & FEC(function execution context) sits in grand scheme of things

Yes. Add two more pieces inside the **JavaScript engine**:

```text
JavaScript Runtime
├── JavaScript Engine
│   ├── Call Stack
│   ├── Heap Memory
│   ├── Global Execution Context
│   └── Function Execution Contexts
│
├── Runtime APIs
│   ├── setTimeout / fetch / DOM / fs
│
├── Queues
│   ├── Microtask queue
│   └── Macrotask queue
│
└── Event Loop
```

**Heap Memory**

Heap is where objects/functions/arrays are stored.

```js
const user = { name: "Arjun" };
```

Conceptually:

```text
Variable user -> reference/address
Object { name: "Arjun" } -> heap memory
```

Primitive values like numbers/booleans are usually handled directly in execution context/stack-related storage, while objects live in heap and variables hold references to them.

---

**Execution Context**

An execution context is the environment created when JS code runs.

It contains things like:

```text
variables
function declarations
scope chain
this value
references to heap objects
```

There are mainly two types:

| Type                       | Created when          |
| -------------------------- | --------------------- |
| Global Execution Context   | JS file/script starts |
| Function Execution Context | Function is called    |

---

**Call Stack + Execution Context**

The call stack stores execution contexts.

```js
const user = { name: "Arjun" };

function greet() {
  const message = "Hello";
  console.log(message, user.name);
}

greet();
```

Flow:

```text
1. Global Execution Context is created
   user -> reference to heap object
   greet -> function stored in memory

2. Global Execution Context is pushed onto call stack

3. greet() is called

4. Function Execution Context for greet is created

5. greet context is pushed onto call stack

6. greet finishes

7. greet context is popped from call stack

8. Global context remains until program/page ends
```

So:

```text
Call stack = stack of execution contexts
Execution context = variables + scope + this for currently running code
Heap = shared memory area for objects/functions
```

---

**Where Event Loop Fits**

The event loop does not directly manage heap or execution contexts.

Its job is only:

```text
Wait until call stack is empty
Take next queued callback
Ask engine to execute it
```

When a callback runs, the engine creates a new function execution context for that callback and pushes it onto the call stack.

Example:

```js
const user = { name: "Arjun" };

setTimeout(() => {
  console.log(user.name);
}, 1000);
```

Flow:

```text
1. Global context created
2. user object stored in heap
3. setTimeout callback registered with runtime
4. global sync code finishes
5. later event loop sends callback to engine
6. callback execution context is created
7. callback context is pushed onto call stack
8. callback reads user reference from outer scope
9. object is found in heap
```

---

The connected version:

```text
Runtime
  = whole environment

Engine
  = executes JS

Execution context
  = environment for currently running code

Call stack
  = stack of execution contexts

Heap
  = memory for objects/functions

Runtime APIs
  = handle async work outside stack

Queues
  = store ready callbacks

Event loop
  = moves callbacks from queues to call stack when stack is empty
```

Shortest mental model:

> The **engine** runs code by creating **execution contexts** and placing them on the **call stack**. Those contexts store variables and references. Objects live in the **heap**. Async work is handled by the **runtime**, and the **event loop** brings callbacks back so the engine can create a new execution context for them.



One-line version:

> The **engine runs code on the call stack**, the **runtime handles async work outside the stack**, and the **event loop brings finished async callbacks back onto the stack when it is empty**.
