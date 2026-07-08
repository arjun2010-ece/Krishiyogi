# Browser Rendering and Performance Deep Dive

**Role:** Senior Frontend Engineer and Web Performance Expert  
**Objective:** Build an in-depth mental model of how a browser renders a page and handles interactivity, moving sequentially beyond the basic Critical Rendering Path (CRP) and initial metrics like FCP/LCP.

> **Current Knowledge Baseline:** I already understand how the DOM/CSSOM form the Render Tree, leading to Layout, Paint, and FCP/LCP. Help me connect the next set of dots from a frontend developer's perspective.


I think you're asking exactly the right question.

Most resources stop at:

> **HTML → DOM → CSSOM → Render Tree → Layout → Paint → FCP/LCP**

But that's only about **getting pixels on the screen**. As a senior frontend engineer, you need to understand what happens **after the page becomes visible**—because that's where performance, React, and user experience intersect.

I would teach it as one continuous story instead of isolated topics.

---

# The Complete Browser Rendering & Interaction Journey

Think of the browser as having **three phases**:

```
PHASE 1
Loading the page
(Initial Render)

↓

PHASE 2
Making the page interactive

↓

PHASE 3
Keeping the page fast
(User Interactions)
```

Most tutorials only teach Phase 1.

---

# Phase 1 — Initial Rendering (You already know this)

```
Request HTML

↓

Parse HTML

↓

DOM

↓

Download CSS

↓

CSSOM

↓

Style Calculation

↓

Render Tree

↓

Layout

↓

Paint

↓

Composite

↓

FCP

↓

LCP
```

At this point,

the user can **see** something.

But...

Can they actually use it?

Not necessarily.

---

# Phase 2 — Making the page interactive

Imagine your React app.

Initially:

```
<button>
    Buy Now
</button>
```

The button is visible.

You click it.

Nothing happens.

Why?

Because JavaScript hasn't finished.

This introduces the next important metric.

---

# Time to Interactive (TTI)

The page may already be painted.

But JavaScript is still:

* downloading
* parsing
* compiling
* executing

Example

```
Visible page

↓

JavaScript still executing

↓

User clicks

↓

Nothing happens

↓

Eventually JS finishes

↓

Now button works
```

That's why visibility ≠ interactivity.

---

# Why JavaScript delays interactivity

After downloading,

the browser must

```
Download JS

↓

Parse JS

↓

Compile JS

↓

Execute JS

↓

Attach event listeners

↓

Interactive
```

Large bundles delay all of this.

That's why

```
2MB bundle

↓

Slow TTI
```

while

```
300KB bundle

↓

Fast TTI
```

---

# The Main Thread

Now we reach one of the most important concepts.

Everything you've learned so far happens mostly on one thread:

```
Main Thread
```

Think of it as a single worker.

```
┌───────────────────────────────┐
│ Main Thread                   │
│                               │
│ HTML Parsing                  │
│ CSS Parsing                   │
│ JavaScript                    │
│ Layout                        │
│ Paint                         │
│ Event Handlers                │
└───────────────────────────────┘
```

Only one thing runs at a time.

This explains almost every frontend performance problem.

---

# Long Tasks

Imagine

```js
for (let i = 0; i < 500000000; i++) {}
```

Now

```
Main Thread

Busy

Busy

Busy

Busy

Busy
```

User clicks

Nothing happens.

Because the main thread is occupied.

---

This introduces another Core Web Vital.

---

# INP (Interaction to Next Paint)

Previously Google used FID.

Now they recommend **INP**.

INP measures

```
User clicks

↓

How long until

↓

The next visible update?
```

If JavaScript blocks the thread,

INP becomes worse.

---

# Event Loop

Now imagine

```
User clicks

↓

Browser creates click event

↓

Event enters queue

↓

Main Thread free?

↓

Yes

↓

Run handler
```

If the Main Thread is busy,

the event waits.

```
Click

↓

Queue

↓

Queue

↓

Queue

↓

Finally handled
```

That's why heavy JavaScript creates laggy UIs.

---

# Rendering Frames

Modern browsers aim for

```
60 FPS
```

Meaning

```
One frame every

16.67 ms
```

Every frame,

the browser ideally performs

```
JavaScript

↓

Style

↓

Layout

↓

Paint

↓

Composite
```

within 16.67 ms.

If it exceeds that budget,

frames are dropped.

Animations stutter.

---

# requestAnimationFrame()

Suppose you're animating something.

Bad

```js
setInterval(move, 16);
```

Good

```js
requestAnimationFrame(move);
```

Because

```
Browser

↓

Preparing next frame

↓

Runs your callback

↓

Then renders
```

Animations stay synchronized with the browser's rendering cycle.

---

# React enters the story

React does NOT paint pixels.

Instead

```
State changes

↓

React renders

↓

Virtual DOM

↓

Diff

↓

Real DOM updates

↓

Browser

↓

Style

↓

Layout

↓

Paint

↓

Composite
```

React's job ends after updating the DOM.

The browser still performs rendering.

---

# User Interaction Pipeline

Suppose

```jsx
setCount(count + 1)
```

What happens?

```
State Update

↓

React Render

↓

Virtual DOM

↓

Diff

↓

DOM Mutation

↓

Style Calculation

↓

Layout?

↓

Paint?

↓

Composite

↓

Screen Updates
```

Exactly the same browser pipeline happens again.

Only this time,

it's incremental instead of building everything from scratch.

---

# Where Reflow/Repaint fit

Whenever React updates

```
DOM

↓

Style

↓

Layout?

↓

Paint?

↓

Composite
```

If only

```
color
```

changes

```
Paint
```

If

```
width
```

changes

```
Layout

↓

Paint
```

---

# Layout Thrashing

Suppose

```
Read Layout

↓

Write Layout

↓

Read Layout

↓

Write Layout
```

The browser repeatedly recalculates layout.

Very expensive.

Senior engineers batch reads and writes.

---

# Compositor Layers

Some animations avoid Layout and Paint completely.

```
transform

↓

Composite only
```

That's why

```
transform

opacity
```

are preferred for animations.

---

# Putting Everything Together

Here is the complete picture:

```
URL
 │
 ▼
Download HTML
 │
 ▼
Parse HTML
 │
 ▼
DOM
 │
 ▼
Download CSS
 │
 ▼
CSSOM
 │
 ▼
Style Calculation
 │
 ▼
Render Tree
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
FCP
 │
 ▼
LCP
 │
 ▼
Download JavaScript
 │
 ▼
Parse JS
 │
 ▼
Compile JS
 │
 ▼
Execute JS
 │
 ▼
Attach Event Listeners
 │
 ▼
Time To Interactive
 │
 ▼
User Click
 │
 ▼
Event Loop
 │
 ▼
React State Update
 │
 ▼
Virtual DOM
 │
 ▼
Diff
 │
 ▼
DOM Mutation
 │
 ▼
Style
 │
 ▼
Layout?
 │
 ▼
Paint?
 │
 ▼
Composite
 │
 ▼
Next Frame
 │
 ▼
INP
```

---

## The roadmap I recommend

To build a **senior-level mental model**, I'd learn these topics in this order because each one naturally builds on the previous:

1. **The Browser Process Model** – browser process, renderer process, GPU process, network process, sandboxing, and how Chrome's multi-process architecture works.
2. **The Main Thread & Event Loop** – call stack, Web APIs, task queue, microtask queue, rendering opportunities, and how rendering fits between tasks.
3. **JavaScript Execution** – parsing, compilation (e.g., JIT), execution, garbage collection, and why long tasks block rendering.
4. **The Rendering Pipeline in Depth** – style invalidation, layout invalidation, paint invalidation, compositing, layer promotion, and GPU acceleration.
5. **Rendering Performance** – frame budget (16.67 ms), `requestAnimationFrame`, `requestIdleCallback`, layout thrashing, forced synchronous layout, and animation best practices.
6. **Loading Performance** – preload, prefetch, preconnect, lazy loading, code splitting, tree shaking, HTTP caching, compression, and resource priorities.
7. **Core Web Vitals** – FCP, LCP, CLS, INP, TTFB, what affects each metric, and how to improve them.
8. **React Through the Browser's Eyes** – reconciliation, commit phase, React scheduling, concurrent rendering, hydration, and how React work maps onto the browser pipeline.

This progression lets every new concept connect directly to the previous one, giving you a single, coherent mental model rather than a collection of unrelated topics.

From what we've covered so far, the next topic I'd recommend is **the browser's process architecture and the event loop**, because once you understand *where* the browser does work and *how* tasks are scheduled, concepts like long tasks, INP, React scheduling, and even concurrent rendering become much easier to reason about.
