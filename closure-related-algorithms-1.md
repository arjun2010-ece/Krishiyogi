Yes. These are classic JavaScript interview questions because they test **closures, caching, lexical scope, and async behavior**.

## 1. Implement a `once` utility

### Problem

Create a function `once(fn)` that ensures `fn` runs **only once**.

Later calls should not execute `fn` again. They should return the **same result from the first execution**.

Example:

```javascript
function add(a, b) {
  console.log("Executing...");
  return a + b;
}

const addOnce = once(add);

console.log(addOnce(2, 3));   // Executing... 5
console.log(addOnce(10, 20)); // 5
console.log(addOnce(50, 50)); // 5
```

### Implementation

```javascript
function once(fn) {
  let hasRun = false;
  let result;

  return function (...args) {
    if (!hasRun) {
      result = fn.apply(this, args);
      hasRun = true;
    }

    return result;
  };
}
```

### How it works

When we call:

```javascript
const addOnce = once(add);
```

`once()` executes and creates:

```javascript
let hasRun = false;
let result;
```

Then it returns another function.

Because of **closure**, the returned function remembers those variables:

```text
once(add)
   │
   ├── hasRun = false
   ├── result = undefined
   │
   └── returned function
          ↑
          │
       closure
```

First call:

```javascript
addOnce(2, 3);
```

Since:

```javascript
hasRun === false
```

we execute:

```javascript
result = add(2, 3);
```

Now:

```text
result = 5
hasRun = true
```

Second call:

```javascript
addOnce(10, 20);
```

Now:

```javascript
hasRun === true
```

so `add()` doesn't run.

We simply return:

```javascript
return result;
```

which is:

```text
5
```

### Why `apply(this, args)`?

We could write:

```javascript
fn(...args);
```

But:

```javascript
fn.apply(this, args);
```

also preserves the original calling context.

For example:

```javascript
const user = {
  name: "Arjun",

  greet() {
    return this.name;
  }
};

user.greet();
```

If preserving `this` matters, `apply` makes our utility safer.

### Interview answer

> `once` can be implemented using a closure. The closure stores whether the function has already executed and stores its first result. On subsequent calls, instead of calling the original function again, we simply return the cached result.

---

# 2. Write a `memoize` function

Memoization is related to `once`, but there is an important difference.

`once`:

```text
Execute function once globally
```

Memoization:

```text
Execute once per unique input
```

For example:

```javascript
function square(n) {
  console.log("Calculating...");
  return n * n;
}

const memoizedSquare = memoize(square);

memoizedSquare(5);
// Calculating...
// 25

memoizedSquare(5);
// 25

memoizedSquare(10);
// Calculating...
// 100

memoizedSquare(10);
// 100
```

The function executes once for `5` and once for `10`.

## Basic implementation with one argument

```javascript
function memoize(fn) {
  const cache = new Map();

  return function (arg) {
    if (cache.has(arg)) {
      return cache.get(arg);
    }

    const result = fn(arg);

    cache.set(arg, result);

    return result;
  };
}
```

Visualize the cache:

```text
Map

5  → 25
10 → 100
20 → 400
```

When:

```javascript
memoizedSquare(5);
```

we first ask:

```javascript
cache.has(5)
```

If false:

```javascript
const result = fn(5);

cache.set(5, result);
```

Next time:

```javascript
cache.has(5)
```

is true, so:

```javascript
return cache.get(5);
```

The original function never executes again for that argument.

---

## What about multiple arguments?

Suppose:

```javascript
function add(a, b) {
  return a + b;
}
```

We need to cache:

```text
(1, 2) → 3
(2, 3) → 5
(4, 5) → 9
```

A simple interview implementation is:

```javascript
function memoize(fn) {
  const cache = new Map();

  return function (...args) {
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      return cache.get(key);
    }

    const result = fn.apply(this, args);

    cache.set(key, result);

    return result;
  };
}
```

Usage:

```javascript
function add(a, b) {
  console.log("Calculating");
  return a + b;
}

const memoizedAdd = memoize(add);

console.log(memoizedAdd(2, 3));
// Calculating
// 5

console.log(memoizedAdd(2, 3));
// 5

console.log(memoizedAdd(5, 10));
// Calculating
// 15
```

Cache becomes roughly:

```text
"[2,3]"  → 5
"[5,10]" → 15
```

### Important senior-level caveat

`JSON.stringify(args)` is fine for an interview demonstration but is **not a universally safe production cache key**.

It can have issues with complex objects, cyclic references, unsupported values, and differences in object structure.

So say:

> For primitive arguments, a Map is straightforward. For multiple or complex object arguments, I'd choose the cache-key strategy based on the application's requirements rather than blindly using JSON.stringify.

That qualification makes the answer stronger.

---

## Why must the function ideally be pure?

The question specifically says:

> memoize a pure function

That's important.

A **pure function**:

1. produces the same output for the same inputs;
2. has no externally observable side effects.

Example:

```javascript
function square(n) {
  return n * n;
}
```

Always:

```text
square(5) → 25
```

Therefore caching is safe.

But this would be problematic:

```javascript
function getRandomNumber(n) {
  return n + Math.random();
}
```

Same input:

```javascript
getRandomNumber(5);
```

doesn't necessarily produce the same output.

Memoizing it changes its behavior.

### Interview answer

> Memoization stores previously calculated results, usually in a Map. When the same arguments are supplied again, we return the cached result instead of recalculating it. It's particularly appropriate for pure functions because the same inputs always produce the same outputs.

---

# 3. Why does `var` behave unexpectedly in loops with async callbacks?

This one is extremely important for JavaScript interviews.

Consider:

```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(() => {
    console.log(i);
  }, 100);
}
```

Many beginners expect:

```text
0
1
2
```

But it prints:

```text
3
3
3
```

### Why?

Because `var` is **function-scoped**, not block-scoped.

There is essentially only **one `i` variable** shared by all callbacks.

You can think of it approximately as:

```javascript
var i;

for (i = 0; i < 3; i++) {
  setTimeout(() => {
    console.log(i);
  }, 100);
}
```

During the loop:

```text
i = 0
i = 1
i = 2
```

Callbacks are scheduled, but don't run yet.

Then:

```text
i = 3
```

The loop stops.

Only afterwards do the timer callbacks execute.

Every callback looks at the **same variable**:

```text
             ┌───────────┐
callback 1 ──┤           │
callback 2 ──┤  var i    │ → 3
callback 3 ──┤           │
             └───────────┘
```

Therefore:

```text
3
3
3
```

---

# Fix 1 — use `let`

This is the modern and preferred solution:

```javascript
for (let i = 0; i < 3; i++) {
  setTimeout(() => {
    console.log(i);
  }, 100);
}
```

Output:

```text
0
1
2
```

Why?

Because `let` is block-scoped, and in a `for` loop JavaScript creates a **new binding for each iteration**.

Conceptually:

```text
Iteration 1:
i = 0
callback closes over i₁

Iteration 2:
i = 1
callback closes over i₂

Iteration 3:
i = 2
callback closes over i₃
```

So:

```text
callback 1 → i₁ → 0
callback 2 → i₂ → 1
callback 3 → i₃ → 2
```

This is a closure question as much as it is a `var` question.

---

# Fix 2 — IIFE

Before `let` was available, this was a common solution:

```javascript
for (var i = 0; i < 3; i++) {
  (function (currentI) {
    setTimeout(() => {
      console.log(currentI);
    }, 100);
  })(i);
}
```

Output:

```text
0
1
2
```

Each iteration passes the current value:

```javascript
(function (currentI) {
   ...
})(i);
```

creating a new function scope.

Conceptually:

```text
i = 0
   ↓
currentI = 0

i = 1
   ↓
currentI = 1

i = 2
   ↓
currentI = 2
```

Each callback closes over its own `currentI`.

---

# Fix 3 — pass argument to `setTimeout`

There is another neat solution:

```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(
    (value) => {
      console.log(value);
    },
    100,
    i
  );
}
```

Output:

```text
0
1
2
```

But for modern JavaScript, your answer should simply start with:

```javascript
for (let i = 0; i < 3; i++) {
```

---

# Connecting all three questions

These three questions are actually testing one common concept: **closures**.

### `once`

Closure remembers:

```text
hasRun
result
```

```javascript
function once(fn) {
  let hasRun = false;
  let result;

  return function (...args) {
    // remembers hasRun + result
  };
}
```

### `memoize`

Closure remembers:

```text
cache
```

```javascript
function memoize(fn) {
  const cache = new Map();

  return function (...args) {
    // remembers cache
  };
}
```

### `var` loop

Callback closure remembers the variable:

```javascript
setTimeout(() => {
  console.log(i);
});
```

But with `var`, every callback closes over the **same binding**.

So a very useful mental model for your interview is:

```text
                CLOSURES
                   │
        ┌──────────┼──────────┐
        ↓          ↓          ↓
      once      memoize    async loop
        │          │          │
 remembers     remembers   remembers
  result        cache      variables
```

If Critical TechWorks asks these three around the same time, they're very likely trying to verify that you understand closures practically, rather than just being able to recite:

> "A closure is a function bundled with its lexical environment."

You should be able to explain **what the closure is remembering and why that matters** in each example.
