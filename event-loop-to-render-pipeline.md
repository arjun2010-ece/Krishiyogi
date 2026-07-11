# JavaScript Event Loop — A Staff Engineer's Mental Model (v1)

The event loop is **not** where your JavaScript code executes.

JavaScript executes on the **call stack**.

The event loop is the **scheduler** that decides **when the next piece of work may enter the call stack**.

That distinction alone separates junior explanations from senior ones.

---

# 1. Preceding Concept — What Comes Before the Event Loop?

Before understanding the event loop, you need to understand the execution model that creates the need for it.

The chain is:

```
JavaScript Engine
        ↓
Execution Contexts
        ↓
Call Stack
        ↓
Event Loop
        ↓
Rendering
```

Let's briefly cover each.

---

## JavaScript Engine

Examples:

* V8 (Chrome, Edge, Node.js)
* SpiderMonkey (Firefox)
* JavaScriptCore (Safari)

The engine's job is to

* parse JavaScript
* compile it
* execute it

The engine itself **does not know how to fetch a URL, wait 5 seconds, or listen for mouse clicks.**

Those capabilities come from the browser.

---

## Execution Context

Whenever a function starts running, JavaScript creates an execution context.

It contains

* local variables
* parameters
* lexical environment
* `this`
* scope chain

Example

```js
function greet(name) {
    const msg = "Hello";
    console.log(msg, name);
}

greet("John");
```

Running `greet()` creates a new execution context.

---

## Call Stack

Execution contexts are pushed onto the call stack.

```
Call Stack

-----------
greet()
-----------
Global()
-----------
```

When `greet()` finishes

```
-----------
Global()
-----------
```

When Global finishes

```
(empty)
```

Only **one frame executes at a time.**

This is why JavaScript is called **single-threaded**.

---

# Why This Creates a Problem

Imagine this:

```js
fetch("/users");
```

The network might take

* 50 ms
* 500 ms
* 5 seconds

Should JavaScript freeze for 5 seconds?

Obviously not.

If it did,

* scrolling freezes
* typing freezes
* animations freeze
* clicks stop working

Everything becomes unusable.

This is exactly the problem the event loop solves.

---

# 2. Definition — What Is the Event Loop?

A precise definition:

> The event loop is the runtime scheduling mechanism that repeatedly checks whether the JavaScript call stack is empty, moves eligible tasks into the stack, runs all pending microtasks, and gives the browser opportunities to render between iterations.

Notice what it **doesn't** do:

* It does not execute JavaScript itself.
* It does not make asynchronous operations happen.
* It does not run on the call stack.

Instead, it **coordinates** different parts of the runtime.

Think of it as an operating system scheduler—but only for JavaScript work.

---

# 3. Why the Event Loop Exists

JavaScript has

* one call stack
* one thread of execution

Meanwhile the browser has many things happening simultaneously:

* mouse events
* keyboard events
* timers
* network requests
* rendering
* image decoding
* disk access

These happen outside JavaScript.

When they finish, they need a safe moment to run JavaScript callbacks.

The event loop decides that moment.

Without it:

* callbacks would interrupt running code
* two functions could modify shared state simultaneously
* JavaScript would no longer be deterministic

The event loop guarantees:

> **Only one JavaScript callback executes at a time.**

---

# 4. Core Components

Let's connect every piece.

---

## 1. Call Stack

The call stack contains the function currently executing.

Example

```js
foo();
```

```
Stack

foo()
Global()
```

Only the top frame runs.

---

## 2. Browser APIs (or Runtime APIs)

These are **not JavaScript.**

Examples

* setTimeout
* fetch
* DOM events
* IntersectionObserver
* ResizeObserver

When JavaScript calls

```js
setTimeout(...)
```

JavaScript immediately continues.

The timer runs inside browser infrastructure.

Likewise

```js
fetch(...)
```

The network request runs on browser networking threads.

The call stack is free immediately.

---

## 3. Task Queue (Macrotask Queue)

When browser work completes,

the callback goes into the task queue.

Examples

```
click
keydown
setTimeout
setInterval
MessageChannel
postMessage
```

These wait until

* stack empty
* all microtasks finished

Only then can one task begin.

---

## 4. Microtask Queue

Higher priority than the task queue.

Examples

```
Promise.then
Promise.catch
queueMicrotask
MutationObserver
```

After every task finishes,

the runtime drains **every** microtask before continuing.

Not one.

All of them.

This detail matters enormously.

---

## 5. Render Opportunity

Only after

* stack empty
* microtasks empty

can the browser decide

* style recalculation
* layout
* paint
* compositing

Rendering never interrupts JavaScript.

JavaScript always runs to completion first.

---

# Complete Picture

```
                 Browser APIs
               /      |       \
          Timer   Network   Click

               ↓ completed

          Task Queue (Macrotasks)

               ↓

      Event Loop chooses task

               ↓

            Call Stack

               ↓

      Microtask Queue

               ↓

      Render Opportunity

               ↓

      Next Event Loop Tick
```

This is the lifecycle repeated thousands of times per second.

---

# 5. Worked Example

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

---

## Step 1

Global execution starts.

```
Stack

Global
```

---

Runs

```js
console.log("A");
```

Output

```
A
```

---

## Step 2

Runs

```js
setTimeout(...)
```

Browser starts timer.

No callback yet.

Stack keeps executing.

---

## Step 3

Runs

```js
Promise.resolve().then(...)
```

Promise already resolved.

Its callback enters

```
Microtask Queue

C
```

---

## Step 4

Runs

```js
console.log("D");
```

Output

```
A
D
```

Global execution finishes.

Stack becomes empty.

---

## Step 5

Before touching timers,

the runtime drains microtasks.

```
Run C
```

Output

```
A
D
C
```

---

## Step 6

Microtasks empty.

Event loop now checks task queue.

Timer callback enters stack.

Runs

```
B
```

Final output

```
A
D
C
B
```

---

# Why Promise Runs Before setTimeout

People often say

> "Promises are faster."

Wrong.

The real reason:

Microtasks have **higher scheduling priority** than tasks.

That's it.

---

# Another Example

```js
console.log(1);

setTimeout(() => console.log(2));

Promise.resolve().then(() => {
    console.log(3);

    Promise.resolve().then(() => {
        console.log(4);
    });
});

console.log(5);
```

Execution

```
1
5
3
4
2
```

Notice:

The new microtask (`4`) is also drained before returning to the task queue.

Microtasks keep running until none remain.

---

# 6. How This Connects to Rendering

This is where browser performance interviews become interesting.

Rendering does **not** happen continuously.

Instead,

every event loop iteration looks roughly like this:

```
Run Task

↓

Run ALL Microtasks

↓

Render (if needed)

↓

Next Task
```

Suppose you do

```js
while(true){}
```

The stack never empties.

Therefore

* no render
* no click handling
* no scrolling
* no timers

The browser appears frozen.

---

Suppose you create

```js
function loop() {
    Promise.resolve().then(loop);
}

loop();
```

The call stack empties between callbacks, but the microtask queue is **never empty** because each microtask schedules another one. The event loop keeps draining microtasks and never reaches a render opportunity.

Result:

* no painting
* frozen UI
* delayed input handling

This is called **microtask starvation**.

---

# Connection to Core Web Vitals

The event loop directly affects responsiveness.

For example,

User clicks.

```
Click Event

↓

Task Queue

↓

Long JavaScript Task

↓

Click waits

↓

Eventually handled
```

If JavaScript blocks for

```
300 ms
```

the click cannot be processed.

That delay contributes to **Interaction to Next Paint (INP)** because the browser cannot start handling the interaction or reach the next paint until the main thread becomes available.

Likewise,

large synchronous work delays

* rendering
* paints
* animations

Everything shares the same main thread.

---

# 7. Following Concept — What Comes After the Event Loop?

Once you understand the event loop, the next topics naturally are:

### 1. Rendering Pipeline

```
DOM

↓

Style

↓

Layout

↓

Paint

↓

Composite
```

The event loop decides **when** rendering may happen.

The rendering pipeline decides **how** rendering happens.

---

### 2. Main Thread vs Compositor Thread

Modern browsers separate some work:

Main thread

* JavaScript
* style
* layout

Compositor thread

* combines painted layers
* smooth scrolling
* GPU animations
* transforms
* opacity

Understanding this explains why:

```css
transform
```

is usually smoother than

```css
width
```

---

### 3. Long Tasks

Any JavaScript task over approximately **50 ms** is considered a long task.

Long tasks delay

* input
* rendering
* timers
* animations

Breaking long work into smaller chunks (for example with `setTimeout`, `scheduler.postTask`, or `requestIdleCallback` where appropriate) helps keep the main thread responsive.

---

### 4. Frame Budget

On a 60 Hz display,

one frame lasts roughly

```
16.7 ms
```

JavaScript, layout, paint, and compositing all compete for that budget if you want to maintain 60 FPS.

---

# 8. Common Interview Misconceptions

### ❌ "The event loop executes JavaScript."

No.

The **call stack** executes JavaScript.

The event loop only schedules work.

---

### ❌ "setTimeout(0) runs immediately."

No.

It runs **after**:

* current stack
* all microtasks
* any earlier tasks

---

### ❌ "Promises are asynchronous."

A resolved promise schedules its continuation as a **microtask**. The asynchronous operation (like a network request) is handled elsewhere by the browser or runtime.

---

### ❌ "Microtasks run after rendering."

Usually the opposite.

Microtasks run **before** the browser gets a chance to render.

---

### ❌ "JavaScript is single-threaded, so browsers are single-threaded."

No.

JavaScript execution is single-threaded.

The browser itself uses many threads:

* networking
* image decoding
* compositor
* rasterization
* GPU
* audio
* storage

---

### ❌ "The event loop is part of JavaScript."

Not exactly.

The JavaScript language (ECMAScript) defines concepts like jobs (used for promises), but the browser event loop, rendering, timers, and Web APIs are defined by the HTML and browser runtime specifications. Node.js has its own event loop implementation with different phases.

---

# Staff-Level Summary

The mental model to carry into interviews is:

```
JavaScript Engine
        ↓
Execution Contexts
        ↓
Call Stack (runs JavaScript)
        ↓
Browser APIs perform async work
        ↓
Completed callbacks enter queues
        ↓
Event Loop schedules work
        ↓
Run one task
        ↓
Drain all microtasks
        ↓
Browser gets a render opportunity
        ↓
Next iteration
```

The key insight is that **the event loop is a scheduler for the main thread**. It guarantees that JavaScript runs one callback at a time, prioritizes microtasks over tasks, and only allows rendering between iterations. This scheduling behavior is fundamental to understanding UI responsiveness, frame drops, long tasks, and Core Web Vitals such as INP.


I agree. The previous explanation is technically correct, but it reads more like a collection of topics than a **single mental model**. At a staff level, you should be able to explain the event loop as one continuous story where every concept naturally leads to the next.

Here's the version I would use for learning and interviews.

---






# JavaScript Event Loop — One Continuous Mental Model (v2)

## Step 1: It all starts with JavaScript being single-threaded

JavaScript can execute only **one piece of code at a time** because it has only **one call stack**.

When your application starts, the browser creates the **Global Execution Context**, which is pushed onto the call stack.

```text
Call Stack

┌─────────────┐
│ Global()    │
└─────────────┘
```

As functions are called, new execution contexts are pushed onto the stack.

```js
function A() {
  B();
}

function B() {
  console.log("Hello");
}

A();
```

Execution looks like this:

```text
Global()
    ↓
A()
    ↓
B()
```

Each function finishes before the previous one continues.

This means JavaScript is **synchronous by default**.

---

## Step 2: The Problem

Imagine JavaScript encounters this:

```js
fetch("/users");
```

The network may take two seconds.

If JavaScript simply waited here, the call stack would be blocked for two seconds.

During that time:

* clicks wouldn't work
* scrolling would freeze
* animations would stop
* nothing else could execute

That would make every webpage unusable.

So JavaScript needs a way to **continue running other code while waiting for slow operations**.

This is exactly why the browser provides asynchronous APIs.

---

## Step 3: The Browser Takes Over

When JavaScript reaches an asynchronous operation like

```js
setTimeout(...)

fetch(...)

addEventListener(...)
```

it **does not perform that work itself**.

Instead, it asks the browser:

> "Please handle this for me. Let me know when it's finished."

For example,

```js
setTimeout(callback, 1000);
```

JavaScript immediately hands the timer to the browser.

The browser starts counting one second.

Meanwhile, JavaScript continues executing the next line.

The call stack never waits.

This is the key idea:

> **JavaScript delegates slow work to the browser.**

---

## Step 4: The Browser Finishes the Work

Eventually something completes.

For example:

* the timer expires
* a network request returns
* the user clicks a button

The browser now has a callback ready to execute.

Can it immediately interrupt JavaScript?

No.

JavaScript is never interrupted while executing.

Instead, the callback is placed into a queue.

For most browser events, timers, and input events, this is the **Task Queue (Macrotask Queue)**.

```text
Task Queue

click callback
timer callback
```

The callback simply waits there.

---

## Step 5: Enter the Event Loop

Now we finally reach the Event Loop.

The Event Loop is **not where JavaScript runs**.

Instead, it continuously watches one thing:

> **Is the Call Stack empty?**

If the answer is **No**, it waits.

If the answer is **Yes**, it starts scheduling the next work.

So the Event Loop acts like a dispatcher.

```text
while (true) {

    Is Call Stack empty?

          ↓

        Yes?

          ↓

    Move next task
    onto the stack
}
```

Its job is simply deciding **when** another callback is allowed to execute.

---

## Step 6: But There Are Two Queues

Not every callback has the same priority.

JavaScript actually has two important queues.

### Task Queue (Macrotasks)

Contains things like

* setTimeout
* setInterval
* click events
* keyboard events

---

### Microtask Queue

Contains

* Promise.then()
* Promise.catch()
* queueMicrotask()

Microtasks always have higher priority.

---

## Step 7: What Happens After a Task Finishes?

Suppose a timer callback has just completed.

Before the Event Loop picks another task, it always checks:

> "Are there any microtasks waiting?"

If yes,

it executes **every single microtask**.

Only after the Microtask Queue becomes completely empty does it continue to the next task.

So every Event Loop iteration follows this sequence:

```text
Run one Task

↓

Run ALL Microtasks

↓

Browser may Render

↓

Run next Task
```

That sequence repeats forever while the page is open.

---

## Step 8: Example

```js
console.log("A");

setTimeout(() => console.log("B"), 0);

Promise.resolve().then(() => console.log("C"));

console.log("D");
```

Let's follow it exactly.

### First

Global code starts executing.

```
console.log("A");
```

Output

```
A
```

---

### Next

```js
setTimeout(...)
```

The browser starts the timer.

Nothing is printed.

---

### Next

```js
Promise.resolve().then(...)
```

The Promise is already resolved.

Its callback enters the **Microtask Queue**.

---

### Next

```js
console.log("D");
```

Output becomes

```
A
D
```

Global execution finishes.

The Call Stack is now empty.

---

The Event Loop now starts working.

It first checks the **Microtask Queue**.

There is one callback.

So it runs it.

```
C
```

Output becomes

```
A
D
C
```

Now the Microtask Queue is empty.

The Event Loop checks the Task Queue.

The timer callback is waiting.

It finally executes.

```
B
```

Final output

```
A
D
C
B
```

---

# Step 9: Where Does Rendering Fit?

One of the biggest interview mistakes is thinking rendering happens continuously.

It doesn't.

The browser gets an opportunity to render **only after JavaScript finishes executing**.

A simplified Event Loop cycle looks like this:

```text
Run one Task
        ↓
Run every Microtask
        ↓
Style Calculation
        ↓
Layout
        ↓
Paint
        ↓
Composite
        ↓
Next Task
```

If JavaScript keeps the Call Stack busy for a long time, rendering cannot begin.

That's why long JavaScript tasks make pages feel slow.

---

# Step 10: Why This Matters for Performance

Imagine the user clicks a button.

The browser receives the click immediately.

But if JavaScript is still executing another task, the click callback must wait in the Task Queue.

Nothing can interrupt the running JavaScript.

So the sequence becomes:

```text
User Clicks

↓

Click enters Task Queue

↓

Current JavaScript still running...

↓

Call Stack finally becomes empty

↓

Event Loop schedules click callback

↓

JavaScript handles click

↓

Browser renders updated UI
```

That waiting time is one of the reasons a page feels unresponsive and directly contributes to **Interaction to Next Paint (INP)**.

---

# The Entire Story in One Diagram

```text
User opens webpage
        │
        ▼
JavaScript starts executing on the Call Stack
        │
        ▼
Synchronous code runs normally
        │
        ▼
Async operation encountered?
        │
   ┌────┴────┐
   │         │
  No        Yes
   │         │
   ▼         ▼
Continue   Browser takes over
running       │
              ▼
      Browser performs work
              │
              ▼
      Work completes later
              │
              ▼
Callback enters a Queue
(Task Queue or Microtask Queue)
              │
              ▼
Event Loop waits until Call Stack is empty
              │
              ▼
Run one Task
              │
              ▼
Run ALL Microtasks
              │
              ▼
Browser gets a chance to Render
              │
              ▼
Repeat forever
```

## The one sentence that ties everything together

> **JavaScript executes code on a single call stack. Whenever it encounters slow work, it delegates that work to the browser. When the browser finishes, it places the callback into a queue. The Event Loop waits for the call stack to become empty, runs one task, drains all microtasks, gives the browser a chance to render, and then repeats this cycle for as long as the page is alive.**


I'm glad that version clicked. Now let's refine it into the mental model that senior and staff engineers actually carry around.

The biggest confusion comes from seeing terms like **Web APIs**, **Task Queue**, **Macrotask Queue**, **Callback Queue**, and **Microtask Queue** thrown around as separate concepts. They are actually just different parts of the same journey.

---

# The Complete Story (with all the terminology connected)

## Step 1: JavaScript starts executing

When a webpage loads, the browser starts the JavaScript engine.

The engine creates the **Global Execution Context** and pushes it onto the **Call Stack**.

```text
Browser
    │
    ▼
JavaScript Engine
    │
    ▼
Call Stack
    │
    ▼
Global Execution Context
```

The **Call Stack** is the only place where JavaScript code executes.

Only one function can execute at a time.

---

## Step 2: JavaScript encounters an asynchronous operation

Suppose JavaScript reaches:

```js
setTimeout(() => console.log("Hello"), 1000);
```

The Call Stack cannot wait for one second.

Instead, JavaScript asks the browser:

> "Please handle this timer for me."

Where does it send it?

It sends it to the browser's **Web APIs**.

---

## What are Web APIs?

**Web APIs are browser-provided features that run outside the JavaScript engine.**

Examples include:

* Timers (`setTimeout`, `setInterval`)
* Network requests (`fetch`, `XMLHttpRequest`)
* DOM events (`click`, `keydown`)
* Geolocation
* WebSocket
* IndexedDB

Notice something important:

These are **not part of JavaScript**.

They are part of the **browser runtime**.

So the flow becomes:

```text
Call Stack
      │
      ▼
setTimeout()
      │
      ▼
Browser Web APIs
(start timer)
```

Meanwhile, JavaScript immediately continues executing the next line.

---

# Step 3: The Web API finishes its work

One second later,

the timer inside the Web APIs expires.

The browser now has a callback ready.

```js
() => console.log("Hello")
```

Can it immediately execute it?

No.

JavaScript might still be running something else.

Instead, the browser places the callback into a queue.

---

# Step 4: Which queue?

This depends on the type of callback.

There are **two important queues**.

## 1. Task Queue

Also called:

* **Macrotask Queue**
* **Callback Queue** (older tutorials often use this name)

These names generally refer to the same queue in browser discussions.

It contains callbacks from things like:

```text
setTimeout

setInterval

click events

keyboard events

postMessage

MessageChannel
```

So after the timer finishes:

```text
Web APIs
      │
      ▼
Task Queue
(timer callback waiting)
```

The callback is **waiting**, not executing.

---

## 2. Microtask Queue

Some callbacks don't go to the Task Queue.

Instead they go into the **Microtask Queue**.

Examples:

```text
Promise.then()

Promise.catch()

Promise.finally()

queueMicrotask()

MutationObserver
```

Example:

```js
Promise.resolve().then(() => {
    console.log("Done");
});
```

The Promise callback skips the Task Queue completely.

It goes directly into the **Microtask Queue**.

---

# Step 5: Now the Event Loop enters the story

The Event Loop continuously watches the Call Stack.

Its question is very simple:

> "Is the Call Stack empty?"

If not,

it waits.

If yes,

it starts moving callbacks from the queues into the Call Stack.

Notice something important.

The Event Loop never executes code itself.

It only moves callbacks onto the Call Stack.

```text
Task Queue
      │
      ▼
Event Loop
      │
      ▼
Call Stack
```

or

```text
Microtask Queue
      │
      ▼
Event Loop
      │
      ▼
Call Stack
```

---

# Step 6: Which queue gets priority?

Suppose both queues have callbacks.

```text
Task Queue

Timer Callback



Microtask Queue

Promise Callback
```

Which one runs first?

Always the **Microtask Queue**.

The Event Loop follows this rule:

```text
1. Wait until Call Stack is empty.

2. Execute ONE Task.

3. Execute ALL Microtasks.

4. Give the browser a chance to Render.

5. Repeat.
```

This rule never changes.

---

# Let's see the entire journey

Consider:

```js
console.log("Start");

setTimeout(() => console.log("Timer"), 0);

Promise.resolve().then(() => {
    console.log("Promise");
});

console.log("End");
```

---

## Phase 1 — Synchronous execution

Call Stack executes

```text
console.log("Start")
```

Output

```text
Start
```

---

JavaScript reaches

```js
setTimeout(...)
```

It sends the timer to

```text
Web APIs
```

The timer starts.

Execution continues immediately.

---

JavaScript reaches

```js
Promise.resolve().then(...)
```

The Promise callback goes into

```text
Microtask Queue
```

---

JavaScript executes

```text
console.log("End")
```

Output

```text
Start
End
```

The Call Stack becomes empty.

---

## Phase 2 — Event Loop starts scheduling

The Event Loop first looks for microtasks.

There is one.

```text
Microtask Queue

Promise callback
```

It moves it to the Call Stack.

Output

```text
Promise
```

Now the Microtask Queue is empty.

---

The Event Loop now checks the Task Queue.

The timer callback is waiting there.

It moves it onto the Call Stack.

Output

```text
Timer
```

Final output

```text
Start
End
Promise
Timer
```

---

# Where Rendering Fits

After the Event Loop has:

* executed one Task
* drained the entire Microtask Queue

the browser finally gets an opportunity to render.

```text
Task
   │
   ▼
All Microtasks
   │
   ▼
Style
   │
   ▼
Layout
   │
   ▼
Paint
   │
   ▼
Composite
   │
   ▼
Next Event Loop iteration
```

If JavaScript keeps the Call Stack busy, or keeps adding more microtasks, the browser cannot reach this rendering step. That's why excessive synchronous work or endless microtasks can hurt responsiveness and metrics like **INP**.

---

# The Complete Mental Model

```text
                JavaScript starts
                       │
                       ▼
                 Call Stack executes
                       │
      ┌────────────────┴────────────────┐
      │                                 │
Synchronous code                  Async operation?
      │                                 │
      │                                 ▼
      │                         Browser Web APIs
      │                                 │
      │                         (Timer, Fetch,
      │                         Click, etc.)
      │                                 │
      │                        Work completes
      │                                 │
      │               ┌─────────────────┴─────────────────┐
      │               │                                   │
      │        Promise callback                  Timer / Click / Fetch callback
      │               │                                   │
      │               ▼                                   ▼
      │       Microtask Queue                     Task Queue (Macrotask/Callback Queue)
      │               └──────────────┬────────────────────┘
      │                              ▼
      │                        Event Loop
      │                              │
      ▼                              ▼
               Move callback to Call Stack
                              │
                              ▼
                     JavaScript executes it
                              │
                              ▼
                  Drain all Microtasks
                              │
                              ▼
                Browser gets a Render opportunity
                              │
                              ▼
                         Repeat forever
```

## One small terminology note for interviews

You will hear these terms used:

* **Task Queue** ✅ (modern HTML specification term)
* **Macrotask Queue** ✅ (very common in interviews and articles)
* **Callback Queue** ✅ (older educational term)

In browser interviews, they almost always refer to the **same queue**. The preferred modern terminology is **Task Queue**, while **Microtask Queue** is a separate, higher-priority queue.

This connected story is the mental model you'll use not only for the event loop, but also when you later study `requestAnimationFrame`, rendering, long tasks, layout thrashing, and Core Web Vitals such as INP.


This is the mental model that connects every concept—call stack, Web APIs, task queue, microtasks, event loop, and rendering—into one continuous flow rather than treating them as isolated topics.

