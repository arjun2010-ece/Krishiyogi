# Critical TechWorks — Senior Frontend Developer Technical Interview Preparation

## Interview Details

- **Role:** Trailblazing Frontend Developer
- **Company:** Critical TechWorks
- **Technical Interviewers:** André Sousa and Rui Oliveira
- **Duration:** 1h–1h30
- **Format:** Technical discussion + possible practical exercises
- **Domain:** BMW Group / Automotive Software
- **Likely Stack:** JavaScript, TypeScript, Angular, React, RxJS, HTML, CSS

---

# 1. Expected Interview Structure

A likely structure for the 90-minute interview:

| Approx. Time | Likely Topic |
|---|---|
| 5–10 min | Introductions + experience |
| 15–25 min | JavaScript / TypeScript / Browser fundamentals |
| 15–20 min | React + possibly Angular |
| 10–15 min | CSS / HTML / HTTP |
| 20–30 min | Practical/live coding |
| 5–10 min | Architecture, testing, Git, CI/CD + my questions |

### Important

During coding exercises:

1. Clarify requirements.
2. Explain the approach before coding.
3. Write the simplest correct solution.
4. Explain time/space complexity.
5. Mention edge cases.
6. Improve the solution if necessary.

---

# 2. Tell Me About Yourself

> I'm a Senior Frontend Engineer with around nine years of software development experience, primarily focused on JavaScript, TypeScript, React and modern frontend architecture.
>
> In my recent roles I've worked on fairly complex applications involving React, TypeScript, REST APIs, authentication, state management and reusable component architectures. I've also worked across the development lifecycle — clarifying requirements, designing frontend solutions, integrating backend APIs, testing, deployment and production troubleshooting.
>
> More recently I've been working on applications in the blockchain and financial technology space, where reliability and handling asynchronous client-server interactions correctly were particularly important.
>
> At this stage I'm looking for a role where I can contribute not only by implementing features, but also through architecture decisions, code quality, mentoring and improving engineering practices. That's one of the things that attracted me to Critical TechWorks.

Keep this around **60–90 seconds**.

---

# 3. What Do You Know About Critical TechWorks?

> Critical TechWorks was created in 2018 as a joint venture between BMW Group and Critical Software, and it focuses on developing software for BMW Group.
>
> What particularly interested me is that frontend isn't just traditional website development here. The teams work on digital experiences across areas such as vehicle connectivity, electrification and automotive systems.
>
> I also noticed that although Angular seems to be widely used, the company values engineers coming from React and other frontend ecosystems, which I like because strong frontend engineering principles transfer across frameworks.

---

# 4. Why Critical TechWorks?

> There are three things that interest me.
>
> First is the engineering domain. Automotive software introduces interesting constraints around reliability, performance and long-lived products that are different from building another standard CRUD application.
>
> Second, I'm interested in working on products with real-world scale and impact through the BMW ecosystem.
>
> Third, I like the engineering culture Critical TechWorks describes around autonomous, cross-functional teams and developer ownership. At senior level I'm looking for an environment where I'm expected to contribute to technical decisions rather than simply receive tickets and implement them.

---

# 5. Explain the JavaScript Event Loop

JavaScript executes synchronous code on a **single call stack**.

Asynchronous operations such as timers and network requests are handled by the browser/runtime.

When asynchronous operations complete, callbacks are queued.

Important queues:

- **Microtask queue:** Promise callbacks, `queueMicrotask`
- **Macrotask/task queue:** `setTimeout`, events, etc.

After synchronous code finishes:

```text
Call Stack empty
       ↓
Run microtasks
       ↓
Run next macrotask
       ↓
Run microtasks again
       ↓
Continue...
```

Example:

```javascript
console.log("A");

setTimeout(() => console.log("B"), 0);

Promise.resolve().then(() => console.log("C"));

console.log("D");
```

Output:

```text
A
D
C
B
```

Why?

1. `A` executes synchronously.
2. `setTimeout` schedules a macrotask.
3. Promise `.then()` schedules a microtask.
4. `D` executes synchronously.
5. Call stack becomes empty.
6. Microtasks execute → `C`.
7. Macrotask executes → `B`.

---

# 6. What Is a Closure?

A closure happens when a function retains access to variables from the lexical scope where it was created, even after the outer function finishes executing.

```javascript
function createCounter() {
  let count = 0;

  return function () {
    count++;
    return count;
  };
}

const counter = createCounter();

counter(); // 1
counter(); // 2
```

The inner function still has access to `count`.

### Common Uses

- debounce
- throttle
- event handlers
- encapsulation
- callbacks
- React hooks

---

# 7. var vs let vs const

### `var`

- Function scoped
- Hoisted
- Initialized with `undefined`
- Can be redeclared
- Can be reassigned

### `let`

- Block scoped
- Hoisted but in Temporal Dead Zone
- Cannot be redeclared in same scope
- Can be reassigned

### `const`

- Block scoped
- Hoisted but in Temporal Dead Zone
- Cannot be redeclared
- Cannot be reassigned

Important:

```javascript
const user = {
  name: "Arjun"
};

user.name = "John"; // Valid
```

But:

```javascript
user = {}; // Error
```

`const` protects the **binding**, not the object's contents.

---

# 8. == vs ===

`==` performs type coercion.

`===` performs strict comparison.

```javascript
0 == false;
// true

0 === false;
// false
```

Prefer:

```javascript
===
```

because it makes behavior more predictable.

---

# 9. map vs filter vs reduce vs forEach

### map

Transforms elements and returns a new array.

```javascript
const doubled = numbers.map(n => n * 2);
```

### filter

Returns elements matching a condition.

```javascript
const adults = users.filter(user => user.age >= 18);
```

### reduce

Combines an array into another value.

```javascript
const total = numbers.reduce(
  (sum, number) => sum + number,
  0
);
```

### forEach

Runs side effects and doesn't return a transformed array.

```javascript
users.forEach(user => {
  console.log(user.name);
});
```

---

# 10. Shallow Copy vs Deep Copy

```javascript
const copy = {
  ...original
};
```

This creates a **shallow copy**.

Nested objects still share references.

```javascript
const original = {
  user: {
    name: "Arjun"
  }
};

const copy = {
  ...original
};

copy.user.name = "John";

console.log(original.user.name);
// John
```

For suitable structured data:

```javascript
const copy = structuredClone(original);
```

creates a deep clone.

---

# 11. Explain async/await

`async/await` is syntax built on top of Promises.

```javascript
async function getUser() {
  const response = await fetch("/api/user");

  return response.json();
}
```

An `async` function always returns a Promise.

```javascript
async function test() {
  return 10;
}
```

Equivalent conceptually to:

```javascript
function test() {
  return Promise.resolve(10);
}
```

`await` pauses the execution of that **async function**, not the entire JavaScript thread.

---

# 12. Promise.all vs Promise.allSettled

## Promise.all

```javascript
const results = await Promise.all([
  fetchUsers(),
  fetchProducts(),
  fetchOrders()
]);
```

Fails when one Promise rejects.

Use when **all operations must succeed**.

## Promise.allSettled

```javascript
const results = await Promise.allSettled([
  fetchUsers(),
  fetchProducts(),
  fetchOrders()
]);
```

Waits for everything.

Returns:

```javascript
[
  {
    status: "fulfilled",
    value: ...
  },
  {
    status: "rejected",
    reason: ...
  }
]
```

Useful when partial failures are acceptable.

Also know:

```text
Promise.race()
Promise.any()
```

---

# 13. Debounce vs Throttle

## Debounce

Wait until events stop occurring.

Example:

```text
User typing search
```

```text
a
ar
arj
arju
arjun
     ↓
wait 500ms
     ↓
API request
```

## Throttle

Allow execution at most once during an interval.

Example:

```text
scroll events
resize events
mouse movement
```

---

# 14. Implement Debounce

```javascript
function debounce(fn, delay) {
  let timeoutId;

  return function (...args) {
    clearTimeout(timeoutId);

    timeoutId = setTimeout(() => {
      fn.apply(this, args);
    }, delay);
  };
}
```

### Why closure?

The returned function retains access to:

```javascript
timeoutId
```

### Why `...args`?

Preserves the arguments passed to the function.

### Why `this`?

Preserves the original calling context.

---

# 15. What Causes React to Re-render?

Common causes:

- State changes
- Parent component renders
- Context value changes
- External subscribed state changes

Important:

```text
React render
     ≠
DOM update
```

React first renders the component and calculates the desired UI.

Reconciliation then determines which DOM changes are actually required.

---

# 16. How Do You Reduce Unnecessary React Renders?

First:

> Measure before optimizing.

Possible techniques:

- Move state closer to where it is used
- Split large components
- `React.memo`
- `useMemo`
- `useCallback`
- Avoid unnecessary Context updates
- Virtualize large lists
- Avoid unnecessary derived state

---

# 17. useMemo vs useCallback vs React.memo

## useMemo

Memoizes a **value**.

```javascript
const sortedUsers = useMemo(() => {
  return sortUsers(users);
}, [users]);
```

## useCallback

Memoizes a **function reference**.

```javascript
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);
```

## React.memo

Memoizes a **component based on props**.

```javascript
const User = React.memo(function User({ name }) {
  return <div>{name}</div>;
});
```

Important senior-level point:

> I wouldn't use memoization everywhere because memoization itself has complexity and cost. I use it when referential stability or expensive calculations actually matter.

---

# 18. useEffect vs useLayoutEffect

## useEffect

Runs after the browser paints.

Useful for:

- API requests
- subscriptions
- analytics
- external synchronization

## useLayoutEffect

Runs after DOM mutation but **before paint**.

Useful for:

- DOM measurements
- synchronous layout corrections
- preventing visual flickering

Important:

> `useLayoutEffect` can block painting, so I use it sparingly.

---

# 19. Why Shouldn't React State Be Mutated?

Bad:

```javascript
user.name = "John";

setUser(user);
```

The reference remains unchanged.

Better:

```javascript
setUser({
  ...user,
  name: "John"
});
```

React relies heavily on referential equality.

Immutable updates:

- Create predictable state transitions
- Produce new references
- Work better with memoization
- Simplify debugging

---

# 20. useState vs useReducer

Use `useState` for simple state.

```javascript
const [name, setName] = useState("");
```

Use `useReducer` when several related transitions exist.

Example:

```text
ADD_ITEM
REMOVE_ITEM
UPDATE_QUANTITY
CLEAR_CART
```

```javascript
const [state, dispatch] = useReducer(
  reducer,
  initialState
);
```

---

# 21. Controlled vs Uncontrolled Components

## Controlled

React controls the value.

```jsx
<input
  value={name}
  onChange={e => setName(e.target.value)}
/>
```

Useful for:

- validation
- conditional UI
- synchronization
- dynamic forms

## Uncontrolled

DOM controls the value.

```jsx
const inputRef = useRef();

<input ref={inputRef} />
```

Access using:

```javascript
inputRef.current.value
```

---

# 22. Why Are React Keys Important?

Keys represent component identity.

Bad:

```jsx
items.map((item, index) => (
  <Item key={index} />
))
```

Better:

```jsx
items.map(item => (
  <Item key={item.id} />
))
```

Using indexes can cause problems when items are:

- reordered
- inserted
- deleted

because React may associate component state with the wrong item.

---

# 23. Angular Preparation

Critical TechWorks appears to use Angular extensively.

My strongest experience is React, so don't pretend to be an Angular expert.

A good answer:

> My strongest production experience is React rather than Angular, so I wouldn't present myself as an Angular specialist.
>
> However, the underlying frontend concepts transfer very well — component architecture, state, routing, reactive programming, testing and performance.
>
> I've also reviewed Angular concepts such as components, services, dependency injection, lifecycle hooks, RxJS and change detection, so I'm comfortable ramping up on it.

---

# 24. Angular Lifecycle Hooks

Important hooks:

```text
ngOnChanges
      ↓
ngOnInit
      ↓
ngDoCheck
      ↓
ngAfterContentInit
      ↓
ngAfterContentChecked
      ↓
ngAfterViewInit
      ↓
ngAfterViewChecked
      ↓
ngOnDestroy
```

Most important:

### ngOnInit

Initialization after Angular initializes inputs.

### ngOnChanges

Runs when input properties change.

### ngAfterViewInit

Runs after the component's view initializes.

### ngOnDestroy

Cleanup before component destruction.

Approximate React mental mapping:

| Angular | React Concept |
|---|---|
| `ngOnInit` | `useEffect(..., [])` |
| `ngOnChanges` | `useEffect(..., [dependency])` |
| `ngOnDestroy` | `useEffect` cleanup |

Not exact equivalents, but useful conceptually.

---

# 25. Angular Change Detection

Angular change detection determines whether component data has changed and updates the DOM accordingly.

Angular supports strategies including:

```text
Default
OnPush
```

`OnPush` can reduce unnecessary checks.

Conceptually:

```text
React
Component renders
      ↓
Reconciliation
      ↓
DOM updates
```

versus:

```text
Angular
Change detection
      ↓
Template bindings checked
      ↓
DOM updates
```

---

# 26. What Is RxJS?

RxJS is a reactive programming library based around **Observables**.

An Observable represents values arriving over time.

Example:

```text
User typing
     ↓
Observable
     ↓
debounceTime()
     ↓
distinctUntilChanged()
     ↓
switchMap()
     ↓
API
     ↓
Results
```

Important operators:

```text
map
filter
debounceTime
distinctUntilChanged
switchMap
mergeMap
catchError
```

---

# 27. Why Is switchMap Useful for Search?

Imagine:

```text
"a" request
       ↓

"ar" request
       ↓

"arj" request
```

With `switchMap`, when a new value arrives, RxJS switches to the new inner Observable and unsubscribes from the previous one.

Therefore it works well for:

```text
latest request wins
```

behavior.

---

# 28. CSS: Put Two Elements Side by Side

Using Flexbox:

```css
.container {
  display: flex;
}
```

Using Grid:

```css
.container {
  display: grid;
  grid-template-columns: 1fr 1fr;
}
```

---

# 29. Flexbox vs Grid

## Flexbox

Primarily one-dimensional.

```text
Row OR Column
```

Good for:

- navigation
- buttons
- alignment
- simple layouts

## Grid

Two-dimensional.

```text
Rows AND Columns
```

Good for:

- page layouts
- dashboards
- complex grids

---

# 30. CSS Specificity

Approximate priority:

```text
!important
      ↓
inline styles
      ↓
IDs
      ↓
classes / attributes / pseudo-classes
      ↓
elements / pseudo-elements
```

But the complete cascade also considers:

- origin
- importance
- cascade layers
- specificity
- source order

---

# 31. CSS Positioning

## relative

Remains in normal document flow.

Often establishes a containing block for positioned descendants.

## absolute

Removed from normal flow.

Usually positioned relative to the nearest positioned ancestor.

## fixed

Usually positioned relative to the viewport.

## sticky

Behaves normally until a scrolling threshold is reached, then sticks within its scroll context.

---

# 32. HTTP Status Codes

| Code | Meaning |
|---|---|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 301 | Permanent Redirect |
| 302 | Temporary Redirect |
| 304 | Not Modified |
| 400 | Bad Request |
| 401 | Unauthenticated |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Unprocessable Content |
| 429 | Too Many Requests |
| 500 | Internal Server Error |
| 502 | Bad Gateway |
| 503 | Service Unavailable |
| 504 | Gateway Timeout |

---

# 33. 401 vs 403

## 401

Authentication is missing or invalid.

```text
Who are you?
```

## 403

Identity may be known, but the user doesn't have permission.

```text
You're not allowed to do this.
```

---

# 34. PUT vs PATCH

## PUT

Conventionally represents replacing a resource representation.

Usually idempotent.

```http
PUT /users/123
```

## PATCH

Partially updates a resource.

```http
PATCH /users/123
```

Example:

```json
{
  "name": "John"
}
```

---

# 35. What Is CORS?

CORS stands for:

```text
Cross-Origin Resource Sharing
```

It controls whether JavaScript running on one origin can access resources from another origin.

Example:

```text
Frontend:
https://app.example.com

Backend:
https://api.example.com
```

The backend sends headers defining which origins, methods and headers are allowed.

Certain requests trigger:

```http
OPTIONS
```

preflight requests.

### Does Postman normally get CORS errors?

No.

CORS is primarily a **browser-enforced security mechanism**.

---

# 36. Authentication vs Authorization

## Authentication

```text
Who are you?
```

Example:

```text
Login
Password
OAuth
JWT
Session
```

## Authorization

```text
What are you allowed to do?
```

Example:

```text
Admin can delete user
Normal user cannot
```

---

# 37. JWT

JWT structure:

```text
HEADER.PAYLOAD.SIGNATURE
```

Important:

> JWT payloads are encoded, not encrypted by default.

Therefore sensitive information should not simply be stored inside JWT payloads.

---

# 38. Practical Exercise: Remove Duplicates

Input:

```javascript
const users = [
  { id: 1, name: "A" },
  { id: 2, name: "B" },
  { id: 1, name: "A" }
];
```

Solution:

```javascript
const uniqueUsers = [
  ...new Map(
    users.map(user => [user.id, user])
  ).values()
];
```

### Complexity

```text
Time: O(n)
Space: O(n)
```

---

# 39. Practical Exercise: Group Objects

Input:

```javascript
const users = [
  { name: "A", team: "frontend" },
  { name: "B", team: "backend" },
  { name: "C", team: "frontend" }
];
```

Expected:

```javascript
{
  frontend: [
    { name: "A", team: "frontend" },
    { name: "C", team: "frontend" }
  ],
  backend: [
    { name: "B", team: "backend" }
  ]
}
```

Solution:

```javascript
function groupByTeam(users) {
  return users.reduce((groups, user) => {
    if (!groups[user.team]) {
      groups[user.team] = [];
    }

    groups[user.team].push(user);

    return groups;
  }, {});
}
```

Complexity:

```text
Time: O(n)
Space: O(n)
```

---

# 40. Practical Exercise: Flatten an Array

Input:

```javascript
[1, [2, [3, 4]], 5]
```

Simple solution:

```javascript
array.flat(Infinity);
```

Without `.flat()`:

```javascript
function flatten(array) {
  return array.reduce((result, item) => {
    if (Array.isArray(item)) {
      return result.concat(flatten(item));
    }

    result.push(item);

    return result;
  }, []);
}
```

---

# 41. Fetch Data Safely

```javascript
async function fetchUsers(signal) {
  const response = await fetch(
    "/api/users",
    { signal }
  );

  if (!response.ok) {
    throw new Error(
      `Request failed: ${response.status}`
    );
  }

  return response.json();
}
```

Potential follow-ups:

```text
loading
error
cancellation
retry
race conditions
caching
request deduplication
```

---

# 42. Latest Search Request Wins

Problem:

```text
"a"   → slow request

"ar"  → request

"arj" → fast request
```

If `"a"` finishes after `"arj"`, it shouldn't overwrite the newest result.

One solution is `AbortController`.

```javascript
let controller;

async function search(query) {
  controller?.abort();

  controller = new AbortController();

  const response = await fetch(
    `/api/search?q=${encodeURIComponent(query)}`,
    {
      signal: controller.signal
    }
  );

  return response.json();
}
```

Another solution:

```text
Request ID
```

Important distinction:

> Cancellation can prevent unnecessary work, while request IDs can prevent stale state updates even where cancellation isn't available.

---

# 43. Testing React Components

Focus on **user-visible behavior**, not implementation details.

For a search component test:

```text
User enters query
       ↓
Loading indicator appears
       ↓
API response arrives
       ↓
Results appear
```

Also test:

- Error states
- Empty states
- User interactions
- Loading state
- Async behavior

---

# 44. Unit vs Integration vs E2E

## Unit

Tests small isolated logic.

```text
function
hook
utility
```

## Integration

Tests several parts working together.

Example:

```text
React component
+
API mock
+
state
```

## E2E

Tests complete user flows.

Example:

```text
Login
  ↓
Dashboard
  ↓
Create order
  ↓
Order appears
```

Tools:

```text
Jest
React Testing Library
Playwright
Cypress
```

---

# 45. How Would You Structure a Large Frontend?

Example:

```text
src/
 ├── app/
 ├── features/
 │    ├── authentication/
 │    ├── portfolio/
 │    └── payments/
 ├── components/
 ├── services/
 ├── hooks/
 ├── utils/
 └── types/
```

Senior-level explanation:

> I generally prefer organizing substantial applications around business capabilities rather than having giant global folders containing hundreds of unrelated components and hooks.
>
> I keep server state separate from client UI state, keep components focused, establish clear API boundaries and only promote something to shared infrastructure once it genuinely has multiple consumers.

---

# 46. Client State vs Server State

## Client State

Owned by the frontend.

Examples:

```text
selected tab
modal visibility
form values
theme
sidebar state
```

## Server State

Owned by a remote system.

Examples:

```text
users
products
transactions
orders
```

Server state introduces additional concerns:

```text
fetching
caching
staleness
retry
deduplication
synchronization
background refresh
```

Therefore tools such as:

```text
TanStack Query
```

can be useful rather than putting every API response into generic global state.

---

# 47. How Do You Improve Frontend Performance?

First:

> Measure before optimizing.

Tools:

```text
Chrome DevTools
Performance profiler
React Profiler
Lighthouse
Network panel
```

Potential improvements:

- Code splitting
- Lazy loading
- Image optimization
- HTTP caching
- Reduce request waterfalls
- Virtualize large lists
- Reduce unnecessary renders
- Memoize expensive calculations
- Reduce bundle size
- Web Workers for CPU-heavy operations

Also know Core Web Vitals:

```text
LCP
INP
CLS
```

---

# 48. Web Workers

JavaScript application code generally runs on the main browser thread.

CPU-intensive work can block:

```text
rendering
clicks
scrolling
animations
```

Web Workers allow computation on worker threads.

Useful for:

```text
large dataset processing
image processing
heavy calculations
large parsing operations
```

Communication occurs using messages.

---

# 49. localStorage vs sessionStorage vs Cookies

| Storage | Lifetime | Automatically Sent to Server |
|---|---|---|
| localStorage | Persistent | No |
| sessionStorage | Tab/session | No |
| Cookie | Configurable | Yes, depending on scope |

For authentication:

> HttpOnly cookies can protect tokens from direct JavaScript access, reducing token theft through XSS.

But cookie-based authentication requires consideration of:

```text
CSRF
SameSite
Secure
HttpOnly
```

---

# 50. XSS vs CSRF

## XSS

Cross-Site Scripting.

Attacker injects malicious JavaScript.

Mitigation:

```text
output escaping
sanitization
Content Security Policy
avoid unsafe HTML
HttpOnly cookies
```

## CSRF

Cross-Site Request Forgery.

Attacker tricks an authenticated browser into making an unwanted request.

Mitigation:

```text
SameSite cookies
CSRF tokens
Origin validation
```

---

# 51. Git Merge vs Rebase

## Merge

Combines histories.

Can create:

```text
merge commit
```

## Rebase

Moves/replays commits onto another base.

Creates a more linear history.

Important:

> Avoid rebasing shared commits other developers already depend on because rebase rewrites commit history.

---

# 52. git reset vs git revert

## reset

Moves the branch reference.

Can rewrite history.

Useful mainly for local changes.

## revert

Creates a new commit reversing another commit.

Safer for shared branches.

---

# 53. Explain Your CI/CD Process

Example answer:

> After opening a pull request, I'd normally expect automated linting, type checking, unit/integration tests and a production build.
>
> Depending on the project, we may also run security checks and E2E tests.
>
> After review and merge, the pipeline creates a versioned artifact and deploys it through the appropriate environments.
>
> After deployment, we monitor logs, metrics and frontend error reporting to ensure the release is healthy.

Pipeline:

```text
Developer
    ↓
Pull Request
    ↓
Lint
    ↓
Type Check
    ↓
Unit Tests
    ↓
Integration Tests
    ↓
Build
    ↓
E2E Tests
    ↓
Merge
    ↓
Deploy
    ↓
Monitor
```

---

# 54. Accessibility

Prefer:

```html
<button>
  Submit
</button>
```

instead of:

```html
<div onclick="...">
  Submit
</div>
```

A native button provides:

```text
keyboard interaction
focus behavior
semantic meaning
accessibility support
```

Senior principle:

> Prefer semantic HTML first and use ARIA to supplement semantics where necessary rather than unnecessarily rebuilding native browser behavior.

---

# 55. Difficult Technical Decision

Possible authentication story.

### Situation

The application had a complex authentication/wallet flow with multiple authentication mechanisms and redirect states.

### Task

Simplify authentication while preventing redirect loops and inconsistent authenticated states.

### Action

```text
Mapped authentication states
        ↓
Centralized authentication guards
        ↓
Removed redundant flows
        ↓
Handled explicit logout
        ↓
Separated authentication from wallet state
        ↓
Tested redirect/error scenarios
        ↓
Aligned frontend/backend API contracts
```

### Result

> The architecture became easier to reason about, authentication behavior became more deterministic and future changes became easier to implement.

---

# 56. Production Issue Story

Example:

```text
Authentication request returning 401
              ↓
Inspect Network tab
              ↓
Compare request with API contract
              ↓
Find missing/invalid auth header
              ↓
Investigate token lifecycle
              ↓
Correct authentication flow
              ↓
Add protection/tests
```

Important:

Focus on the **debugging process**, not just the final fix.

---

# 57. How Do You Debug a Slow Page?

Do NOT immediately say:

```text
useMemo
```

Start by identifying the bottleneck.

```text
Slow page
   ↓
Measure
   ↓
 ┌───────────────┐
 │               │
Network       Frontend
 │               │
 ↓               ↓
API latency    Rendering
payload        JavaScript
waterfalls     long tasks
caching        re-renders
```

Answer:

> First I'd establish whether the bottleneck is network, JavaScript execution, rendering or backend latency.
>
> I'd use the Network panel, Performance profiler and React Profiler to gather evidence.
>
> If network is the problem, I'd investigate payload size, request waterfalls and caching.
>
> If rendering is the issue, I'd inspect render frequency and expensive calculations.
>
> If JavaScript is blocking the main thread, I'd investigate long tasks and potentially move CPU-heavy work to a Web Worker.
>
> I'd optimize based on measurements rather than assumptions.

---

# 58. How to Behave During Live Coding

Suppose they ask:

> Remove duplicate users.

Don't immediately start typing.

Ask:

> Are duplicates determined by ID?

Then:

> If duplicate IDs exist, should the first or latest record win?

Then:

> Do we need to preserve input order?

Then explain:

> Assuming ID determines uniqueness and the latest record should win, I'd use a Map because it gives approximately O(1) lookup per item.

Then implement.

Finally:

```text
Time: O(n)
Space: O(n)
```

Then mention edge cases.

This demonstrates senior engineering thinking rather than just algorithm memorization.

---

# 59. High-Probability Rapid-Fire Questions

Prepare concise answers for these:

1. Tell me about yourself.
2. Why Critical TechWorks?
3. What do you know about Critical TechWorks/BMW?
4. Describe the most complex frontend application you've worked on.
5. Explain the JavaScript event loop.
6. Microtasks vs macrotasks?
7. Explain closures.
8. `var` vs `let` vs `const`.
9. What is hoisting?
10. Explain execution context/call stack.
11. Promise vs async/await.
12. `Promise.all` vs `Promise.allSettled`.
13. Debounce vs throttle.
14. Explain `this`.
15. Shallow vs deep copy.
16. `map` vs `filter` vs `reduce`.
17. What causes React to re-render?
18. `useEffect` vs `useLayoutEffect`.
19. `useMemo` vs `useCallback`.
20. Why shouldn't React state be mutated?
21. Context vs Redux/global state.
22. Client state vs server state.
23. How would you optimize a slow React application?
24. How would you structure a large frontend?
25. Controlled vs uncontrolled components.
26. Why are React keys important?
27. What is Angular change detection?
28. What is Angular `OnPush`?
29. What Angular lifecycle hooks do you know?
30. Observable vs Promise.
31. What is RxJS `switchMap`?
32. Flexbox vs Grid.
33. Explain CSS specificity.
34. How would you put two elements side by side?
35. Explain common HTTP status codes.
36. 401 vs 403.
37. PUT vs PATCH.
38. What is CORS?
39. Authentication vs authorization.
40. Explain JWT.
41. localStorage vs cookies.
42. XSS vs CSRF.
43. Unit vs integration vs E2E tests.
44. What should frontend tests test?
45. Git merge vs rebase.
46. Git reset vs revert.
47. Explain your CI/CD process.
48. How do you investigate a production frontend issue?
49. Tell me about a technical disagreement.
50. Tell me about a difficult architectural decision.
51. How do you review another engineer's PR?
52. How do you mentor junior developers?
53. How do you handle ambiguous requirements?
54. Implement debounce.
55. Transform/group/filter an array.
56. Remove duplicates efficiently.
57. Fetch data and handle errors.
58. Prevent stale API responses.
59. Implement search with debounce.
60. Discuss complexity and edge cases of your solution.

---

# 60. Final Preparation Priority

## Priority 1 — JavaScript / TypeScript + Coding

Spend approximately **35%** of preparation time here.

Focus on:

```text
Event loop
Closures
Promises
async/await
var/let/const
this
Array methods
Objects/Map/Set
Debounce
API calls
Race conditions
Error handling
```

---

## Priority 2 — React / Senior Frontend

Approximately **25%**.

Focus on:

```text
Rendering
Hooks
useEffect
useMemo
useCallback
React.memo
State architecture
Server state
Performance
Testing
Component design
```

---

## Priority 3 — Angular / RxJS

Approximately **15%**.

Don't try to learn Angular completely.

Focus on:

```text
Components
Lifecycle hooks
Change detection
OnPush
Services
Dependency injection
Observables
RxJS
switchMap
```

---

## Priority 4 — Browser / CSS / HTTP / Security

Approximately **10%**.

Focus on:

```text
Flexbox
Grid
Specificity
HTTP codes
CORS
Cookies
JWT
XSS
CSRF
Accessibility
```

---

## Priority 5 — My Own Experience

Approximately **10%**.

Prepare three strong stories:

### Story 1 — Architecture

```text
Problem
→ Options
→ Trade-offs
→ Decision
→ Implementation
→ Result
```

### Story 2 — Production Problem

```text
Problem
→ Investigation
→ Root cause
→ Fix
→ Prevention
```

### Story 3 — Leadership / Disagreement

```text
Different opinions
→ Understand constraints
→ Present evidence
→ Discuss trade-offs
→ Agree on solution
→ Result
```

---

## Priority 6 — Critical TechWorks

Approximately **5%**.

Know:

```text
Critical TechWorks
       ↓
BMW Group + Critical Software
       ↓
Automotive software
       ↓
Frontend / digital experiences
       ↓
Angular + modern web technologies
       ↓
Cross-functional engineering teams
```

---

# 61. Senior Interview Mindset

For technical questions, don't only give definitions.

Use:

```text
Definition
    ↓
Example
    ↓
When I would use it
    ↓
Trade-off
```

For coding questions:

```text
Clarify
   ↓
Examples
   ↓
Simple solution
   ↓
Code
   ↓
Complexity
   ↓
Edge cases
   ↓
Improve if necessary
```

For architecture questions:

```text
Requirements
     ↓
Constraints
     ↓
Possible solutions
     ↓
Trade-offs
     ↓
Decision
     ↓
Monitoring / Testing
```

---

# 62. Most Important Reminder

Don't try to demonstrate seniority by making every answer complicated.

A senior engineer should be able to say:

> The simplest solution I'd start with is X because of Y. If requirement Z appeared, I'd consider moving to A because of B.

Rather than:

> We should immediately introduce Redux, WebSockets, microfrontends, Web Workers and five abstraction layers.

The goal is to demonstrate:

```text
Strong fundamentals
        +
Clear reasoning
        +
Practical experience
        +
Trade-off awareness
        +
Communication
        =
Senior Frontend Engineer
```

---

# Last-Minute Checklist

- [ ] Event loop
- [ ] Microtasks vs macrotasks
- [ ] Closures
- [ ] `var` / `let` / `const`
- [ ] `this`
- [ ] Promises
- [ ] async/await
- [ ] Array methods
- [ ] Debounce
- [ ] React rendering
- [ ] `useEffect`
- [ ] `useMemo` / `useCallback`
- [ ] React state management
- [ ] Server vs client state
- [ ] Angular lifecycle
- [ ] Angular change detection
- [ ] RxJS Observables
- [ ] `switchMap`
- [ ] Flexbox / Grid
- [ ] CSS specificity
- [ ] HTTP status codes
- [ ] CORS
- [ ] Authentication / authorization
- [ ] JWT
- [ ] XSS / CSRF
- [ ] Testing
- [ ] Git merge / rebase
- [ ] CI/CD
- [ ] Performance debugging
- [ ] Accessibility
- [ ] 3 project stories
- [ ] 2–3 questions for interviewers
- [ ] Practice explaining code while writing it
