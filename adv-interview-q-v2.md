# Pixelmatters Full Stack Engineer --- Technical Interview Master Guide

> **Purpose:** Fast interview preparation for a senior Full Stack
> Engineer role with a backend emphasis.
>
> **How to use this guide:** Read the **TL;DR** first. If you can
> explain it naturally, move on. Read the detailed answer only when the
> concept is unclear or you expect follow-up questions.
>
> **Priority:** ★★★ = must know, ★★ = likely/useful, ★ = secondary.
>
> The answers are intentionally interview-oriented rather than textbook
> definitions: **what it is → why it matters → when to use it →
> trade-offs.**

------------------------------------------------------------------------

# INDEX

## JavaScript

1.  ★★★ What is the JavaScript event loop?
2.  ★★★ What is the difference between the call stack, microtask queue,
    and task/macrotask queue?
3.  ★★★ What is a closure?
4.  ★★★ What is lexical scope?
5.  ★★★ What is hoisting?
6.  ★★★ `var` vs `let` vs `const`?
7.  ★★★ `==` vs `===`?
8.  ★★★ Primitive values vs reference values?
9.  ★★★ What is a shallow copy vs a deep copy?
10. ★★★ How does `this` work in JavaScript?
11. ★★ Arrow functions vs regular functions?
12. ★★ What are prototypes and prototypal inheritance?
13. ★★★ `map`, `filter`, `reduce`, `find`, and `some/every`?
14. ★★ `null` vs `undefined`?
15. ★★★ What does `async/await` actually do?
16. ★★★ How does `Promise.all()` work and when can it be dangerous?
17. ★★ `Promise.allSettled`, `race`, and `any`?
18. ★★★ How should errors be handled with async JavaScript?
19. ★★ What are optional chaining and nullish coalescing?
20. ★★ What are destructuring and spread/rest syntax?
21. ★★ What are `Object.keys`, `Object.values`, and `Object.entries`?
22. ★★★ What output does a Promise/setTimeout example produce?
23. ★★ What is debouncing vs throttling?
24. ★★ What is immutability and why does it matter?
25. ★★ What is event delegation?

## TypeScript

26. ★★★ Why use TypeScript?
27. ★★★ `interface` vs `type`?
28. ★★★ `any` vs `unknown`?
29. ★★★ What is `never`?
30. ★★★ What are union and intersection types?
31. ★★★ What is type narrowing?
32. ★★★ What are type guards?
33. ★★★ What are generics?
34. ★★★ What is `keyof`?
35. ★★ What is `typeof` in a type context?
36. ★★ What are indexed access types?
37. ★★★ `Partial`, `Required`, `Pick`, `Omit`, `Record`, and `Readonly`?
38. ★★ What are mapped types?
39. ★★ What are conditional types?
40. ★★ What are discriminated unions?
41. ★★★ Optional property vs `null`?
42. ★★★ Does TypeScript validation exist at runtime?
43. ★★ Enum vs string union?
44. ★★ What is structural typing?
45. ★★ What is type inference?
46. ★★ What are function overloads?
47. ★★ What does `as const` do?
48. ★★ What does `satisfies` do?
49. ★★ What are decorators?
50. ★★★ How would you type dynamic object access safely?

## Node.js

51. ★★★ How can Node.js handle thousands of concurrent requests if
    JavaScript is single-threaded?
52. ★★★ Is Node.js actually single-threaded?
53. ★★★ What is libuv?
54. ★★★ What blocks the Node.js event loop?
55. ★★★ CPU-bound vs I/O-bound work?
56. ★★ What are worker threads?
57. ★★ `process.nextTick()` vs Promise microtasks vs `setImmediate()`?
58. ★★★ What are streams and why use them?
59. ★★ What are Buffers?
60. ★★★ How would you scale a Node.js application?
61. ★★★ How should configuration/secrets be handled?
62. ★★★ How do you handle uncaught errors in a Node service?
63. ★★ CommonJS vs ES modules?
64. ★★★ How would you diagnose a slow Node.js API?
65. ★★ What causes memory leaks in Node?
66. ★★ What is backpressure?
67. ★★ How do you gracefully shut down a Node service?
68. ★★ What is connection pooling?

## NestJS

69. ★★★ Explain the basic NestJS architecture.
70. ★★★ What is dependency injection?
71. ★★★ What is a Module?
72. ★★★ Controller vs Provider/Service?
73. ★★★ Explain the NestJS request lifecycle.
74. ★★★ Middleware vs Guard vs Pipe vs Interceptor vs Exception Filter?
75. ★★★ What is a Guard?
76. ★★★ What is a Pipe?
77. ★★★ What is an Interceptor?
78. ★★★ What is Middleware?
79. ★★★ What is an Exception Filter?
80. ★★★ What are DTOs and why use them?
81. ★★★ How do validation pipes work?
82. ★★★ How would you implement authentication in NestJS?
83. ★★★ Authentication vs authorization?
84. ★★★ How would you implement role/permission-based authorization?
85. ★★★ How should a large NestJS application be modularized?
86. ★★★ How would you avoid circular dependencies?
87. ★★ Provider scopes: singleton/request/transient?
88. ★★★ How do you test NestJS services/controllers?
89. ★★ How do you mock dependencies in NestJS tests?
90. ★★★ How should database transactions be handled?
91. ★★ How would you implement logging/correlation IDs?
92. ★★★ How would you implement centralized error handling?
93. ★★★ How would you protect an API from abuse?
94. ★★★ How would you improve a slow NestJS endpoint?
95. ★★ What are custom decorators useful for?
96. ★★ Dynamic modules?
97. ★★★ How do you structure configuration?
98. ★★★ How would you design an idempotent endpoint?
99. ★★★ When would you NOT use microservices?
100. ★★★ How would you refactor a large NestJS service?

## REST / Backend Architecture

101. ★★★ What makes an API RESTful?
102. ★★★ PUT vs PATCH?
103. ★★★ Important HTTP status codes?
104. ★★★ How do you design pagination?
105. ★★★ Offset vs cursor pagination?
106. ★★★ How do filtering and sorting belong in an API?
107. ★★★ What is idempotency?
108. ★★★ How do you version an API?
109. ★★★ How should API errors be designed?
110. ★★★ How do you validate input?
111. ★★★ How do you secure a REST API?
112. ★★★ JWT vs session authentication?
113. ★★ Access tokens vs refresh tokens?
114. ★★★ What is rate limiting?
115. ★★★ What is caching and where can it happen?
116. ★★★ How do you avoid race conditions?
117. ★★★ Optimistic vs pessimistic locking?
118. ★★★ How would you handle a long-running operation without blocking
     an HTTP request?
119. ★★★ How do you design file uploads?
120. ★★★ How do you make an endpoint observable?

## Databases

121. ★★★ SQL vs NoSQL?
122. ★★★ What is a database index?
123. ★★★ What are the trade-offs of indexes?
124. ★★★ What is a composite index and why does column order matter?
125. ★★★ What is a query execution plan?
126. ★★★ What is the N+1 query problem?
127. ★★★ What is a transaction?
128. ★★★ Explain ACID.
129. ★★★ What are transaction isolation levels?
130. ★★★ What is a race condition in a database?
131. ★★★ Primary key vs unique constraint vs foreign key?
132. ★★★ Normalization vs denormalization?
133. ★★ What is connection pooling?
134. ★★★ When would you use Redis?
135. ★★★ What is cache invalidation?
136. ★★ Cache-aside pattern?
137. ★★ What is a TTL?
138. ★★★ How would you investigate a slow SQL query?
139. ★★★ Why avoid `SELECT *`?
140. ★★★ How do database migrations work safely in production?

## React

141. ★★★ What causes a React component to render?
142. ★★★ What is reconciliation?
143. ★★★ What is the Virtual DOM?
144. ★★★ What does `useEffect` do?
145. ★★★ Common `useEffect` mistakes?
146. ★★★ `useMemo` vs `useCallback`?
147. ★★★ What does `useRef` do?
148. ★★★ Controlled vs uncontrolled components?
149. ★★★ Local state vs global state?
150. ★★★ Context vs Redux/Zustand?
151. ★★★ Server state vs client/application state?
152. ★★★ What does React Query/TanStack Query solve?
153. ★★★ How do you prevent unnecessary renders?
154. ★★ Why are `key` props important?
155. ★★★ What are Error Boundaries?
156. ★★★ Code splitting and lazy loading?
157. ★★ What is component composition?
158. ★★★ How would you structure a large React application?
159. ★★★ How do you test React components?
160. ★★ What is accessibility in React?

## Testing / Quality

161. ★★★ Unit vs integration vs E2E tests?
162. ★★★ What should you mock?
163. ★★★ What makes a good unit test?
164. ★★★ What is the testing pyramid?
165. ★★★ How would you test a REST endpoint?
166. ★★★ How would you test database code?
167. ★★ What are flaky tests and how do you fix them?
168. ★★★ What should run in CI?
169. ★★★ Code coverage: useful or misleading?
170. ★★★ How do you test failure paths?

## Docker / CI/CD / AWS

171. ★★★ What is Docker?
172. ★★★ Image vs container?
173. ★★★ What is a Dockerfile?
174. ★★★ What are Docker layers and why do they matter?
175. ★★★ What is a multi-stage build?
176. ★★★ Docker volume vs bind mount?
177. ★★★ Container vs VM?
178. ★★★ What should NOT be stored in a Docker image?
179. ★★★ Describe a good CI/CD pipeline.
180. ★★★ CI vs CD?
181. ★★★ What happens after `git push` in a production pipeline?
182. ★★★ How do you roll back a bad deployment?
183. ★★ Blue/green vs rolling deployment?
184. ★★★ What is a health check?
185. ★★★ Core AWS services a full-stack engineer should understand?
186. ★★★ EC2 vs ECS/Fargate vs Lambda?
187. ★★★ S3?
188. ★★★ RDS?
189. ★★★ CloudFront?
190. ★★★ IAM and least privilege?
191. ★★★ How should secrets be stored in AWS?
192. ★★★ How would you deploy a NestJS API on AWS?
193. ★★★ How would you make that deployment highly available?
194. ★★ What is autoscaling?
195. ★★★ What should you monitor in production?

## OOP / Design / Architecture

196. ★★★ What are the SOLID principles?
197. ★★★ Composition vs inheritance?
198. ★★★ What is dependency inversion?
199. ★★ Repository pattern?
200. ★★ Strategy pattern?
201. ★★ Factory pattern?
202. ★★ Observer pattern?
203. ★★★ What is separation of concerns?
204. ★★★ Monolith vs microservices?
205. ★★★ What is technical debt?
206. ★★★ How do you balance quality with delivery speed?
207. ★★★ How do you approach refactoring a legacy system?

## AI-Native / Claude / Agentic Engineering

208. ★★★ How do you use AI in your engineering workflow?
209. ★★★ What is an AI agent?
210. ★★★ Agent vs deterministic workflow?
211. ★★★ What is an agentic loop?
212. ★★★ What is context engineering?
213. ★★★ What is MCP?
214. ★★★ What is CLAUDE.md?
215. ★★ What are Skills?
216. ★★ What are subagents?
217. ★★ What are hooks?
218. ★★★ What is human-in-the-loop?
219. ★★★ How do you safely review AI-generated code?
220. ★★★ Where should AI NOT be trusted blindly?
221. ★★★ How do you make a repository AI-friendly?
222. ★★ What are guardrails?
223. ★★★ How do you evaluate an AI-assisted workflow?
224. ★★★ What happens when today's AI model/tool becomes obsolete?

## Senior / Product Engineering

225. ★★★ How do you approach an unfamiliar problem?
226. ★★★ How do you make a technical decision?
227. ★★★ How do you disagree with another engineer?
228. ★★★ What does ownership mean to you?
229. ★★★ How do you handle a production incident?
230. ★★★ How do you improve something without being asked?
231. ★★★ How do you review a pull request?
232. ★★★ What makes code maintainable?
233. ★★★ How do you decide whether to refactor or ship?
234. ★★★ How do you communicate technical trade-offs to non-engineers?
235. ★★★ How do you onboard into an unfamiliar codebase?
236. ★★★ What does "high quality" mean in software engineering?

------------------------------------------------------------------------

# ANSWERS

## JavaScript

### 1 - What is the JavaScript event loop? ★★★

**TL;DR:** The event loop lets JavaScript execute asynchronous work
without blocking the main execution thread. Synchronous code runs on the
call stack; completed async callbacks are queued and executed when the
stack is free, with microtasks such as Promise callbacks processed
before the next task/macrotask.

**Detailed:** JavaScript executes one piece of JS code at a time on the
call stack. Operations such as timers, network I/O, and file I/O can be
handled by the browser or Node runtime outside that stack. When those
operations complete, their callbacks become eligible to run. The event
loop repeatedly checks whether the call stack is empty and schedules
queued work. Promise reactions and `queueMicrotask` use the microtask
queue, which is drained before the runtime moves to the next task such
as a timer. This architecture is why JavaScript can support high I/O
concurrency despite single-threaded execution of ordinary JS.

**Small code example / visual:**

``` js
console.log("A");
setTimeout(() => console.log("timer"), 0);
Promise.resolve().then(() => console.log("promise"));
console.log("B");
// A, B, promise, timer
```

### 2 - Call stack vs microtask queue vs task/macrotask queue? ★★★

**TL;DR:** The call stack executes synchronous JS. Microtasks
(`Promise.then`, `queueMicrotask`) run after the current stack empties
and before the next task. Tasks/macrotasks include timers and many I/O
callbacks.

**Detailed:** A synchronous function call is pushed onto the stack and
removed when it returns. After the current synchronous job finishes, the
runtime drains eligible microtasks. It then advances to another
event-loop phase/task. This explains why a resolved Promise normally
runs before `setTimeout(..., 0)`. Exact Node event-loop phases are more
nuanced, but this mental model is correct for most interview questions.

**Small code example / visual:**
```js
console.log("sync");
Promise.resolve().then(() => console.log("microtask"));
setTimeout(() => console.log("task"), 0);
// sync -> microtask -> task
```

### 3 - What is a closure? ★★★

**TL;DR:** A closure is a function that retains access to variables from
its lexical scope even after the outer function has finished.

**Detailed:** Functions remember the environment in which they were
created. For example, a function returned from `createCounter()` can
continue accessing a private `count` variable. Closures are useful for
encapsulation, factories, callbacks, memoization, and maintaining state.
A common pitfall is unintentionally retaining large objects and
preventing garbage collection.

**Small code example / visual:**

``` js
function counter() {
  let n = 0;
  return () => ++n;
}
const next = counter();
console.log(next(), next()); // 1 2
```

### 4 - What is lexical scope? ★★★

**TL;DR:** Variable accessibility is determined by where code is
written, not where a function is called.

**Detailed:** An inner function can access variables defined in its
surrounding scopes. The scope chain is determined at function creation.
Lexical scoping is the foundation of closures and explains why moving a
function's definition can change what variables it can access.

**Small code example / visual:**
```js
const name = "global";
function outer() {
  const name = "outer";
  return function inner() { console.log(name); };
}
outer()(); // outer
```

### 5 - What is hoisting? ★★★

**TL;DR:** JavaScript processes declarations before execution, but
different declarations behave differently. Function declarations are
callable before their source line; `var` is initialized to `undefined`;
`let`/`const` exist in a temporal dead zone until initialized.

**Detailed:** "Hoisting" is a useful mental model rather than code
literally moving. `var x` is declared and initialized to `undefined`
during environment creation. `let` and `const` are declared but
accessing them before initialization throws a `ReferenceError`. Function
declarations have their function value available earlier. Prefer clear
declaration-before-use code rather than relying on hoisting.

**Small code example / visual:**

``` js
console.log(a); // undefined
var a = 1;
// console.log(b); // ReferenceError: TDZ
let b = 2;
```

### 6 - `var` vs `let` vs `const`? ★★★

**TL;DR:** `var` is function-scoped and can be redeclared; `let` and
`const` are block-scoped. `const` prevents reassignment of the binding,
not mutation of an object. Default to `const`, use `let` when
reassignment is required.

**Detailed:** `var` also has hoisting behavior that historically caused
bugs. `let`/`const` have a temporal dead zone. `const user = {}` means
`user = otherUser` is forbidden, but `user.name = "A"` is allowed.
Modern JS generally avoids `var`.

**Small code example / visual:**
```js
var a = 1;   // function-scoped
let b = 2;   // block-scoped
const c = { n: 1 };
c.n = 2;     // allowed: object mutated
// c = {};   // not allowed: binding reassignment
```

### 7 - `==` vs `===`? ★★★

**TL;DR:** `==` performs coercion; `===` compares without coercing
types. Prefer `===`.

**Detailed:** `0 == false` is true because abstract equality performs
conversions; `0 === false` is false. Loose equality has a few
intentional uses (`value == null` matches both null and undefined), but
explicit strict comparisons are clearer in most application code.

**Small code example / visual:**
```js
console.log(0 == false);   // true: coercion
console.log(0 === false);  // false: different types
console.log("5" == 5);     // true
console.log("5" === 5);    // false
```

### 8 - Primitive vs reference values? ★★★

**TL;DR:** Primitives behave as independent values;
objects/arrays/functions are reference-like values, so multiple
variables can point to the same object.

**Detailed:** Assigning a number/string copies the value. Assigning an
object copies the reference to that object, so mutating through one
variable is visible through the other. JavaScript technically passes
everything by value---the value passed for an object is a reference
value.

**Small code example / visual:**
```js
let a = 1;
let b = a;
b = 2;
console.log(a); // 1

const x = { n: 1 };
const y = x;
y.n = 2;
console.log(x.n); // 2
```

### 9 - Shallow vs deep copy? ★★★

**TL;DR:** A shallow copy creates a new top-level object but nested
objects remain shared. A deep copy recursively duplicates nested data.

**Detailed:** `{...user}` and `[...items]` are shallow. If
`user.address` is an object, both copies still point to the same
address. `structuredClone()` can deep-clone many built-in data types.
JSON serialization is a limited workaround and loses unsupported
types/values.

**Small code example / visual:**

``` js
const a = { nested: { n: 1 } };
const b = { ...a };
b.nested.n = 2;
console.log(a.nested.n); // 2
```

### 10 - How does `this` work? ★★★

**TL;DR:** For regular functions, `this` is generally determined by how
the function is called. Arrow functions do not create their own `this`;
they capture it lexically.

**Detailed:** `obj.method()` normally binds `this` to `obj`. Calling a
detached function may lose that receiver. `call`, `apply`, and `bind`
explicitly control it. Arrow functions are useful in callbacks where
lexical `this` is desired, but are not a drop-in replacement for every
method.

**Small code example / visual:**

``` js
const user = {
  name: "Ana",
  say() { console.log(this.name); }
};
user.say(); // Ana
```

### 11 - Arrow vs regular functions? ★★

**TL;DR:** Arrow functions have lexical `this`, no own `arguments`, and
cannot be constructors. Regular functions have call-dependent `this` and
can be constructors.

**Detailed:** Choose based on semantics, not merely shorter syntax.
Arrow callbacks often avoid accidental `this` rebinding. Prototype
methods are normally regular methods/functions.

**Small code example / visual:**
```js
const obj = {
  value: 42,
  regular() { return this.value; },
  arrow: () => this?.value
};
console.log(obj.regular()); // 42
// arrow does not get obj as its own `this`
```

### 12 - Prototypes? ★★

**TL;DR:** JavaScript objects can delegate property lookup to another
object through the prototype chain. `class` syntax is largely a
friendlier abstraction over prototypal inheritance.

**Detailed:** If a property isn't found directly on an object,
JavaScript checks its prototype and continues up the chain. Shared
methods on a prototype avoid creating a separate function for every
instance.

**Small code example / visual:**
```js
function User(name) { this.name = name; }
User.prototype.sayHi = function () {
  return `Hi ${this.name}`;
};
const u = new User("Ana");
console.log(u.sayHi());
```

### 13 - `map`, `filter`, `reduce`, `find`, `some`, `every`? ★★★

**TL;DR:** `map` transforms every item; `filter` selects items; `reduce`
accumulates; `find` returns the first match; `some` checks if any match;
`every` checks if all match.

**Detailed:** Prefer the operation that communicates intent. Don't force
everything into `reduce`; readable loops are perfectly acceptable. These
methods return new arrays/values rather than mutating the original
array, although callback code can still mutate referenced objects.

**Small code example / visual:**
```js
const nums = [1, 2, 3, 4];
nums.map(n => n * 2);         // [2,4,6,8]
nums.filter(n => n > 2);      // [3,4]
nums.find(n => n === 3);      // 3
nums.some(n => n > 3);        // true
nums.every(n => n > 0);       // true
nums.reduce((sum,n)=>sum+n,0);// 10
```

### 14 - `null` vs `undefined`? ★★

**TL;DR:** `undefined` usually means missing/not provided/not
initialized; `null` is commonly an explicit "no value".

**Detailed:** In an optional filter, `undefined` can mean "don't filter
by this field" while `null` can intentionally mean "find records whose
field is null." This distinction is particularly useful in APIs and
TypeScript.

**Small code example / visual:**
```js
let a;
const b = null;
console.log(a); // undefined = not assigned
console.log(b); // null = explicit empty value
```

### 15 - What does `async/await` do? ★★★

**TL;DR:** `async/await` is syntax built on Promises. An `async`
function always returns a Promise; `await` pauses that function's
continuation without blocking the JS thread.

**Detailed:** When awaiting a Promise, control returns to the runtime.
Once it settles, continuation is scheduled as a microtask. Independent
operations should often be started concurrently and awaited together
rather than sequentially.

**Small code example / visual:**

``` js
async function load() {
  const user = await getUser();
  return user.name;
}
// load() always returns a Promise
```

### 16 - `Promise.all()`? ★★★

**TL;DR:** Runs/awaits multiple Promise-producing operations
concurrently and resolves when all succeed; rejects as soon as one
rejects.

**Detailed:** It preserves result ordering corresponding to input
ordering. It's excellent for independent I/O. Avoid launching an
unbounded number of operations against a database/API; concurrency may
need limiting. It doesn't magically cancel remaining operations when one
fails.

**Small code example / visual:**

``` js
const [user, orders] = await Promise.all([
  getUser(id),
  getOrders(id)
]); // independent I/O concurrently
```

### 17 - `allSettled`, `race`, `any`? ★★

**TL;DR:** `allSettled` waits for every outcome; `race` settles with the
first settled Promise; `any` fulfills with the first successful Promise
and fails only if all fail.

**Detailed:** Use `allSettled` when partial failure is acceptable,
`race` for timeout/racing behavior (with proper cancellation where
possible), and `any` for redundant providers where one successful result
is enough.

**Small code example / visual:**

``` ts
function parse(value: unknown) {
  if (typeof value === "string") return value.toUpperCase();
  // unknown forces a safety check first
}
```

### 18 - Async error handling? ★★★

**TL;DR:** Use `try/catch` around awaited operations where you can
meaningfully handle or translate the error; otherwise propagate it to a
centralized boundary.

**Detailed:** Don't swallow errors. Add context, preserve useful causes,
log at appropriate boundaries, and map domain/application errors to
stable API responses. In Promise chains, return/await Promises so
rejections aren't accidentally detached.

**Small code example / visual:**
```js
async function getOrder(id) {
  try {
    return await api.get(`/orders/${id}`);
  } catch (err) {
    logger.error({ err, id });
    throw new Error("Could not load order");
  }
}
```

### 19 - Optional chaining and nullish coalescing? ★★

**TL;DR:** `a?.b` safely accesses through null/undefined;
`x ?? fallback` uses fallback only for null/undefined, unlike `||`,
which also treats `0`, `false`, and `""` as falsy.

**Detailed:** `count || 10` incorrectly changes a valid `0` to 10;
`count ?? 10` preserves 0.

**Small code example / visual:**

``` js
const city = user.address?.city ?? "Unknown";
const retries = config.retries ?? 3; // preserves valid 0
```

### 20 - Destructuring and spread/rest? ★★

**TL;DR:** Destructuring extracts values; spread expands/copies values;
rest collects remaining values. Object/array spread is shallow.

**Detailed:** `{name, ...rest} = user` extracts `name`;
`{...user, name: "New"}` creates a shallow updated object. Rest
parameters `(...args)` collect arguments.

**Small code example / visual:**

``` js
const { id, ...rest } = user;
const updated = { ...user, name: "New" };
const copy = [...items];
```

### 21 - `Object.keys/values/entries`? ★★

**TL;DR:** They return an object's own enumerable string keys, values,
or `[key,value]` pairs.

**Detailed:** `entries()` is particularly useful for iterating or
transforming dictionaries/records. Remember TypeScript may need help
preserving precise key types when using these generic JS APIs.

**Small code example / visual:**

``` js
Object.keys(user);
Object.values(user);
Object.entries(user).forEach(([key, value]) => console.log(key, value));
```

### 22 - Promise/setTimeout output? ★★★

``` js
console.log("A");
setTimeout(() => console.log("B"), 0);
Promise.resolve().then(() => console.log("C"));
console.log("D");
```

**TL;DR:** `A`, `D`, `C`, `B`.

**Detailed:** `A` and `D` execute synchronously. The Promise callback is
a microtask. The timer callback is a later task. Microtasks run after
the current synchronous stack and before the timer task.

**Small code example / visual:**
```js
console.log("A");
setTimeout(() => console.log("B"), 0);
Promise.resolve().then(() => console.log("C"));
console.log("D");
// A, D, C, B
```

### 23 - Debounce vs throttle? ★★

**TL;DR:** Debounce waits until calls stop for a period; throttle limits
execution to at most once per interval.

**Detailed:** Debounce search input to avoid requests per keystroke.
Throttle scroll/resize handlers when periodic updates are enough.

**Small code example / visual:**

``` js
const search = debounce(q => api.search(q), 300);
const scroll = throttle(() => updatePosition(), 100);
```

### 24 - Immutability? ★★

**TL;DR:** Treat existing data as unchanged and create new values for
updates. It reduces hidden side effects and makes state changes easier
to reason about.

**Detailed:** Particularly important in React because referential
changes help React/state libraries identify updates. Don't blindly
deep-copy everything; use targeted immutable updates.

**Small code example / visual:**

``` js
const updated = {
  ...user,
  preferences: { ...user.preferences, theme: "dark" }
};
```

### 25 - Event delegation? ★★

**TL;DR:** Attach one event listener to a common ancestor and use event
bubbling to handle events from many descendants.

**Detailed:** Useful for large/dynamic lists and reduces listener count.
Inspect `event.target`/`closest()` while accounting for nested elements.

------------------------------------------------------------------------

**Small code example / visual:**
```js
document.querySelector("#list").addEventListener("click", e => {
  const button = e.target.closest("button[data-id]");
  if (!button) return;
  removeItem(button.dataset.id);
});
```

## TypeScript

### 26 - Why TypeScript? ★★★

**TL;DR:** TypeScript adds static type checking and developer tooling to
JavaScript, catching many errors before runtime and making large
codebases safer to refactor.

**Detailed:** It improves contracts, autocomplete, navigation,
documentation, and refactoring. It does not replace runtime validation
because types disappear when compiled.

**Small code example / visual:**
```ts
function total(price: number, qty: number): number {
  return price * qty;
}
// total("10", 2); // compile-time error
```

### 27 - `interface` vs `type`? ★★★

**TL;DR:** Both describe object shapes. Interfaces support declaration
merging and are natural for extendable object contracts; type aliases
are more flexible for unions, intersections, tuples, primitives, and
mapped/conditional types.

**Detailed:** Either is fine for many object models. Avoid dogmatic
rules. Interfaces can `extends`; types can compose with intersections.
TypeScript's structural typing means implementation compatibility
depends mostly on shape.

**Small code example / visual:**

``` ts
interface User { id: number; name: string }
type Status = "active" | "disabled";
type Admin = User & { permissions: string[] };
```

### 28 - `any` vs `unknown`? ★★★

**TL;DR:** `any` disables type safety. `unknown` accepts any value but
forces you to narrow/check it before using it. Prefer `unknown` at
untrusted boundaries.

**Detailed:** An API/parser catch value may be unknown. You can use
`typeof`, `instanceof`, schema validation, or custom guards before
accessing properties.

**Small code example / visual:**

``` ts
function parse(value: unknown) {
  if (typeof value === "string") return value.toUpperCase();
  // unknown forces a safety check first
}
```

### 29 - `never`? ★★★

**TL;DR:** `never` represents a value that cannot occur, useful for
functions that never return and exhaustive checks.

**Detailed:** In a discriminated-union switch, assigning the default
case to `never` lets the compiler flag newly added variants that weren't
handled.

**Small code example / visual:**

``` ts
function assertNever(x: never): never {
  throw new Error(`Unexpected value: ${x}`);
}
```

### 30 - Union vs intersection? ★★★

**TL;DR:** `A | B` means a value may be A or B; `A & B` means it must
satisfy both A and B.

**Detailed:** Unions often require narrowing. Intersections combine
compatible shapes but can become impossible if properties conflict.

**Small code example / visual:**
```ts
type Id = string | number; // union: either one

type Named = { name: string };
type Timestamped = { createdAt: Date };
type Entity = Named & Timestamped; // intersection: both
```

### 31 - Type narrowing? ★★★

**TL;DR:** TypeScript uses runtime checks/control flow to reduce a broad
type to a more specific one.

**Detailed:** `typeof value === "string"`, `"id" in value`,
`instanceof Error`, equality checks, discriminant fields, and custom
guards can narrow types.

**Small code example / visual:**

``` ts
function format(v: string | number) {
  return typeof v === "string" ? v.toUpperCase() : v.toFixed(2);
}
```

### 32 - Type guards? ★★★

**TL;DR:** Checks that let TypeScript infer a more specific type. Custom
guards can return a predicate such as `value is User`.

**Detailed:** A custom guard should actually verify the claimed shape;
otherwise you create false compiler confidence.

**Small code example / visual:**

``` ts
function isUser(v: unknown): v is User {
  return typeof v === "object" && v !== null && "id" in v;
}
```

### 33 - Generics? ★★★

**TL;DR:** Generics let code operate on types supplied by callers while
preserving type information, instead of falling back to `any`.

**Detailed:** `function first<T>(items: T[]): T | undefined` works for
any item type and returns the corresponding type. Constraints such as
`<T extends { id: number }>` require capabilities while retaining
generic information.

**Small code example / visual:**

``` ts
function first<T>(items: T[]): T | undefined {
  return items[0];
}
const n = first([1, 2, 3]);
```

### 34 - `keyof`? ★★★

**TL;DR:** `keyof T` creates a union of the known property keys of `T`.

**Detailed:** `function get<T, K extends keyof T>(obj:T,key:K):T[K]`
provides safe dynamic property access and preserves the property's
return type.

**Small code example / visual:**

``` ts
function get<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

### 35 - `typeof` in type context? ★★

**TL;DR:** TypeScript's `typeof value` can derive a type from an
existing value; runtime JS `typeof value` returns a type string.

**Detailed:** Useful when configuration/data is defined as a value and
you want the type to follow it.

**Small code example / visual:**

``` tsx
<ThemeContext.Provider value={theme}>
  <App />
</ThemeContext.Provider>
```

### 36 - Indexed access types? ★★

**TL;DR:** `T[K]` obtains the type of property/properties K from T.

**Detailed:** `User["email"]` yields the email property's type. Combined
with generics and `keyof`, it enables precise helper functions.

**Small code example / visual:**
```ts
interface User { id: number; email: string }
type Email = User["email"]; // string
type IdOrEmail = User["id" | "email"]; // number | string
```

### 37 - Utility types? ★★★

**TL;DR:** `Partial<T>` makes fields optional; `Required<T>` required;
`Pick<T,K>` selects; `Omit<T,K>` excludes; `Record<K,V>` maps keys to
values; `Readonly<T>` prevents assignment at compile time.

**Detailed:** They derive types from canonical models and reduce
duplication. Don't overuse `Partial` when your domain really has a
distinct input model.

**Small code example / visual:**

``` ts
type Update = Partial<User>;
type PublicUser = Pick<User, "id" | "name">;
type SafeUser = Omit<User, "password">;
```

### 38 - Mapped types? ★★

**TL;DR:** Mapped types generate a new type by iterating over keys of
another type.

**Detailed:** `type Optional<T> = { [K in keyof T]?: T[K] }` is the
basic idea behind utilities like `Partial`.

**Small code example / visual:**
```ts
type ReadonlyCopy<T> = {
  readonly [K in keyof T]: T[K];
};
type ReadonlyUser = ReadonlyCopy<User>;
```

### 39 - Conditional types? ★★

**TL;DR:** Types can choose one type or another based on assignability:
`T extends U ? X : Y`.

**Detailed:** Powerful in reusable libraries but can harm readability if
over-engineered. `infer` can extract component types.

**Small code example / visual:**
```ts
type ApiResult<T> = T extends Error
  ? { ok: false; error: T }
  : { ok: true; data: T };
type R = ApiResult<User>;
```

### 40 - Discriminated unions? ★★

**TL;DR:** Union members share a literal discriminant field, enabling
safe narrowing and exhaustive handling.

**Detailed:** `{type:"success",data:...} | {type:"error",error:...}` is
safer than many optional fields.

**Small code example / visual:**

``` ts
type Result =
  | { type: "ok"; data: string }
  | { type: "error"; error: Error };
if (result.type === "ok") console.log(result.data);
```

### 41 - Optional vs nullable? ★★★

**TL;DR:** `x?: T` means the property may be absent/undefined;
`x: T | null` means the property exists but can explicitly contain no
value.

**Detailed:** Choose based on domain semantics and API contracts.
Sometimes both are valid but should be intentional.

**Small code example / visual:**
```ts
type Filters = {
  status?: string;          // may be absent / undefined
  assigneeId: number|null; // property exists; null means no assignee
};
```

### 42 - Runtime validation? ★★★

**TL;DR:** TypeScript types are erased at runtime. External input still
requires runtime validation.

**Detailed:** HTTP bodies, environment variables, DB/raw JSON, and
third-party responses are untrusted runtime data. Use validation
libraries/framework validation and transform them into trusted
domain/application types.

**Small code example / visual:**

``` ts
const body: unknown = req.body;
const dto = CreateUserSchema.parse(body);
// TS types alone cannot validate HTTP input.
```

### 43 - Enum vs string union? ★★

**TL;DR:** String unions are lightweight and integrate naturally with
JS; enums create a runtime construct. Prefer unions for many
application-level finite strings unless enum behavior is specifically
useful.

**Small code example / visual:**
```ts
type Status = "todo" | "done";
const s: Status = "todo";

// Enum creates a runtime object:
enum StatusEnum {
  Todo = "todo",
  Done = "done"
}
console.log(StatusEnum.Todo);
```

### 44 - Structural typing? ★★

**TL;DR:** Type compatibility is primarily based on shape rather than
explicit inheritance/name.

**Detailed:** An object with all required `User` fields can be
assignable to `User` even if it never explicitly declared that it
implements User.

**Small code example / visual:**
```ts
interface Named { name: string }

const user = { name: "Ana", age: 30 };
const named: Named = user; // OK: shape has required `name`

// No `implements Named` declaration was required.
```

### 45 - Type inference? ★★

**TL;DR:** TypeScript can infer types from values, returns, control
flow, and generic usage, so explicit annotations aren't needed
everywhere.

**Detailed:** Annotate public boundaries where clarity/contracts help;
don't add redundant annotations that make code noisy.

**Small code example / visual:**
```ts
const count = 3;            // inferred as number
const names = ["Ana", "Bob"]; // inferred as string[]

function double(n: number) {
  return n * 2;              // return inferred as number
}
```

### 46 - Function overloads? ★★

**TL;DR:** Multiple call signatures can describe different valid
argument/result combinations while sharing one implementation.

**Detailed:** Useful when return type meaningfully depends on input
shape; unions/generics are often simpler.

**Small code example / visual:**
```ts
function format(value: string): string;
function format(value: number): string;
function format(value: string | number): string {
  return typeof value === "number" ? value.toFixed(2) : value.trim();
}
```

### 47 - `as const`? ★★

**TL;DR:** Narrows literal values and makes object/array properties
readonly in the inferred type.

**Detailed:** `["admin","user"] as const` yields a readonly tuple of
literal strings rather than `string[]`, useful for deriving unions.

**Small code example / visual:**

``` ts
const roles = ["admin", "user"] as const;
type Role = typeof roles[number]; // "admin" | "user"
```

### 48 - `satisfies`? ★★

**TL;DR:** Checks that a value satisfies a type while preserving the
value's more specific inferred type.

**Detailed:** Useful for configuration objects where you want validation
against a contract without widening away useful literal information.

**Small code example / visual:**

``` ts
const config = {
  mode: "prod", retries: 3
} satisfies AppConfig;
```

### 49 - Decorators? ★★

**TL;DR:** Decorators attach metadata/behavior to classes or members;
NestJS uses them extensively to declare controllers, routes, providers,
validation metadata, etc.

**Detailed:** In NestJS, decorators are declarative metadata consumed by
the framework. Avoid thinking that `@Get()` itself contains the endpoint
business logic.

**Small code example / visual:**

``` ts
@Controller("users")
class UsersController {
  @Get(":id") find(@Param("id") id: string) {}
}
```

### 50 - Safe dynamic object access? ★★★

**TL;DR:** Constrain the key with `keyof`:
`get<T,K extends keyof T>(obj:T,key:K):T[K]`.

**Detailed:** This prevents arbitrary strings from indexing objects and
preserves the exact property type, unlike returning `any`.

------------------------------------------------------------------------

**Small code example / visual:**
```ts
function getProp<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
const email = getProp(user, "email"); // typed from User["email"]
```

## Node.js

### 51 - How can Node handle thousands of concurrent requests? ★★★

**TL;DR:** JavaScript runs on an event loop, while asynchronous I/O is
delegated to the OS/libuv. Node doesn't need one JS thread per
connection, so it can efficiently manage many I/O-bound requests.

**Detailed:** The JS thread initiates I/O and continues other work.
Completion events later schedule callbacks. Some operations use libuv's
worker pool. This works extremely well for I/O-heavy services but
CPU-heavy JS blocks progress for all requests on that event loop.

**Small code example / visual:**

``` js
app.get("/users/:id", async (req, res) => {
  const user = await db.find(req.params.id); // async I/O
  res.json(user);
});
```

### 52 - Is Node actually single-threaded? ★★★

**TL;DR:** JavaScript execution in a normal Node process primarily runs
on one event-loop thread, but Node itself uses OS facilities and
additional threads; worker threads can also execute JS in parallel.

**Detailed:** Saying simply "Node is single-threaded" is incomplete.
libuv has a worker pool for certain operations such as
filesystem/crypto/DNS work, and the runtime has internal threads.

**Small code example / visual:**

``` text
JS callbacks -> event-loop thread
I/O -> OS/libuv
Some operations -> libuv worker pool
CPU-heavy JS -> Worker Threads / separate process
```

### 53 - libuv? ★★★

**TL;DR:** libuv is the cross-platform library underpinning Node's event
loop and asynchronous I/O abstractions, including a worker thread pool
for operations that can't use native async OS facilities directly.

**Small code example / visual:**

``` js
fs.readFile("data.txt", (err, data) => {
  // callback runs later when async work completes
  console.log(data.length);
});
```

### 54 - What blocks the event loop? ★★★

**TL;DR:** Long synchronous CPU work, synchronous I/O, huge JSON
processing, pathological regexes, or any JS callback that runs too long.

**Detailed:** Blocking increases latency for unrelated requests. Measure
event-loop delay and CPU; optimize, chunk work, move CPU-heavy work to
workers/separate services, or redesign the operation.

**Small code example / visual:**

``` js
console.log("A");
setTimeout(() => console.log("timer"), 0);
Promise.resolve().then(() => console.log("promise"));
console.log("B");
// A, B, promise, timer
```

### 55 - CPU-bound vs I/O-bound? ★★★

**TL;DR:** I/O-bound work mostly waits for external resources and suits
Node's async model; CPU-bound work spends significant CPU time and can
block the event loop.

**Small code example / visual:**

``` js
await db.query("SELECT ..."); // I/O-bound
calculateHugePrime();         // CPU-bound; can block
```

### 56 - Worker threads? ★★

**TL;DR:** Worker threads execute JavaScript in separate threads and are
useful for CPU-intensive work, not ordinary asynchronous I/O.

**Detailed:** They have communication/coordination overhead. For large
workloads, separate processes/services may offer stronger isolation and
scaling.

**Small code example / visual:**

``` js
const worker = new Worker("./cpu-task.js", {
  workerData: input
});
```

### 57 - `nextTick` vs Promise vs `setImmediate`? ★★

**TL;DR:** Node's `process.nextTick` queue is processed with very high
priority after the current operation; Promise callbacks are microtasks;
`setImmediate` runs in the event loop's check phase. Avoid recursive
`nextTick` starvation.

**Small code example / visual:**
```js
console.log("A");
process.nextTick(() => console.log("nextTick"));
Promise.resolve().then(() => console.log("promise"));
setImmediate(() => console.log("immediate"));
console.log("B");
// In Node: A, B, nextTick, promise, then immediate
```

### 58 - Streams? ★★★

**TL;DR:** Streams process data incrementally instead of loading the
entire payload into memory.

**Detailed:** Readable, Writable, Duplex, Transform. Great for files,
uploads/downloads, compression, and large datasets. They support
backpressure so producers don't overwhelm consumers.

**Small code example / visual:**

``` js
createReadStream("huge.csv")
  .pipe(transform)
  .pipe(createWriteStream("out.csv"));
```

### 59 - Buffers? ★★

**TL;DR:** Buffers represent raw binary data in Node, useful for files,
network protocols, images, cryptography, etc.

**Small code example / visual:**

``` js
const buf = Buffer.from("hello");
console.log(buf.toString()); // hello
```

### 60 - Scale Node? ★★★

**TL;DR:** Keep application instances stateless, run multiple
instances/containers behind a load balancer, externalize shared state,
scale horizontally, and ensure DB/cache dependencies can handle the
load.

**Detailed:** Profile before scaling. Use autoscaling based on useful
metrics. Avoid relying on process memory for sessions/shared state if
requests can land on different instances.

**Small code example / visual:**
```text
Client -> Load Balancer -> Node instance A
                       -> Node instance B
                       -> Node instance C

Instances stay stateless; shared state lives in DB/Redis.
```

### 61 - Configuration/secrets? ★★★

**TL;DR:** Separate configuration from code; validate environment/config
at startup; store secrets in a secret manager, never source control or
Docker images.

**Small code example / visual:**

``` text
ECS task IAM role -> Secrets Manager -> DB_PASSWORD
Never Git -> Docker image -> production secret.
```

### 62 - Uncaught errors? ★★★

**TL;DR:** Handle expected errors at application boundaries. For truly
uncaught exceptions/unhandled fatal states, log context and terminate
gracefully so the process manager can restart a clean process.

**Detailed:** Continuing after unknown corrupted state can be riskier
than restarting. Graceful shutdown should stop accepting traffic and
finish/timeout in-flight work.

**Small code example / visual:**
```js
process.on("uncaughtException", err => {
  logger.fatal({ err }, "Uncaught exception");
  server.close(() => process.exit(1));
});
// Log + graceful termination instead of blindly continuing.
```

### 63 - CommonJS vs ESM? ★★

**TL;DR:** CommonJS uses `require/module.exports`; ES modules use
`import/export` and are the JavaScript standard module system.

**Small code example / visual:**
```js
// CommonJS
const fs = require("node:fs");
module.exports = { read };

// ES modules
import fs from "node:fs";
export { read };
```

### 64 - Diagnose slow API? ★★★

**TL;DR:** Measure first: request tracing/timing → application
CPU/event-loop → DB queries → external services → serialization/network
→ fix bottleneck → measure again.

**Detailed:** Inspect percentiles, traces, slow queries/query plans,
N+1, indexes, connection pools, external call latency, sequential I/O,
payload sizes, CPU profiles, caching opportunities.

**Small code example / visual:**
```text
GET /orders took 820ms
  controller logic: 8ms
  DB query:       730ms  <-- investigate EXPLAIN/index
  external API:    40ms
  serialization:   10ms

Measure first; optimize the actual bottleneck.
```

### 65 - Memory leaks? ★★

**TL;DR:** Common causes include unbounded caches/collections, retained
closures, event listeners never removed, timers, global references, and
leaked request objects.

**Detailed:** Observe heap growth and use heap snapshots/profilers to
compare retained objects.

**Small code example / visual:**
```js
const cache = new Map();

app.get("/user/:id", async (req, res) => {
  const user = await loadUser(req.params.id);
  cache.set(req.params.id, user); // dangerous if cache grows forever
  res.json(user);
});
```

### 66 - Backpressure? ★★

**TL;DR:** Backpressure prevents a fast producer from overwhelming a
slower consumer by controlling how quickly data is produced/written.

**Small code example / visual:**
```js
for await (const chunk of readable) {
  if (!writable.write(chunk)) {
    await once(writable, "drain"); // wait for slower consumer
  }
}
```

### 67 - Graceful shutdown? ★★

**TL;DR:** On SIGTERM/SIGINT, stop accepting new requests, mark
unhealthy, finish or timeout in-flight requests, close DB/resources,
then exit.

**Small code example / visual:**

``` js
process.on("SIGTERM", () => {
  server.close(async () => {
    await db.close();
    process.exit(0);
  });
});
```

### 68 - Connection pooling? ★★

**TL;DR:** Reuse a bounded pool of expensive DB/network connections
rather than opening one per request.

**Detailed:** Too small causes waiting; too large can overwhelm the
database. Pool sizing must consider the number of application instances.

------------------------------------------------------------------------

**Small code example / visual:**
```ts
const pool = new Pool({ max: 20 });

const result = await pool.query(
  "SELECT id,name FROM users WHERE id=$1",
  [id]
);
// connections are reused instead of created per request
```

## NestJS

### 69 - Basic NestJS architecture? ★★★

**TL;DR:** Modules organize features; Controllers handle transport/HTTP;
Providers/Services contain application/domain logic; dependency
injection connects them.

**Detailed:** Keep controllers thin. Group related functionality by
domain/feature rather than giant technical folders. Infrastructure such
as repositories/clients should be injected behind clear boundaries where
useful.

**Small code example / visual:**
```ts
@Module({
  imports: [DatabaseModule],
  controllers: [UsersController],
  providers: [UsersService, UsersRepository]
})
export class UsersModule {}
```

### 70 - Dependency injection? ★★★

**TL;DR:** A class receives its dependencies from Nest's IoC container
instead of constructing them itself, reducing coupling and making
testing/replacement easier.

**Detailed:** Providers are registered in modules and resolved through
constructor injection. DI enables a service to depend on an
abstraction/provider token rather than hardcoding concrete creation.

**Small code example / visual:**

``` ts
@Injectable()
class OrdersService {
  constructor(private readonly repo: OrdersRepository) {}
}
```

### 71 - Module? ★★★

**TL;DR:** A Nest module defines a cohesive application boundary and
declares/imports/exports controllers and providers.

**Detailed:** `imports` consumes other modules; `providers` registers
dependencies; `controllers` exposes controllers; `exports` makes
selected providers available to importing modules.

**Small code example / visual:**

``` ts
@Module({
  controllers: [OrdersController],
  providers: [OrdersService],
  exports: [OrdersService]
})
export class OrdersModule {}
```

### 72 - Controller vs Service? ★★★

**TL;DR:** Controller translates HTTP/transport requests into
application calls; service contains reusable business/application logic.

**Detailed:** Controllers should deal with route params, DTOs,
status/response concerns---not database-heavy business logic.

**Small code example / visual:**

``` ts
@Get(":id")
find(@Param("id") id: string) {
  return this.service.findById(id); // thin controller
}
```

### 73 - Request lifecycle? ★★★

**TL;DR:** Rough mental model: Middleware → Guards → Interceptors
(before) → Pipes → Controller/Service → Interceptors (after) → Exception
Filters on errors.

**Detailed:** Exact ordering can vary by global/controller/route scope.
The important interview point is responsibility: preprocessing,
authorization, transformation/validation, execution wrapping, and error
mapping.

**Small code example / visual:**

``` text
Request -> Middleware -> Guard -> Interceptor(before)
        -> Pipe -> Controller -> Service
        -> Interceptor(after) -> Response
Error -> Exception Filter
```

### 74 - Middleware vs Guard vs Pipe vs Interceptor vs Filter? ★★★

**TL;DR:** Middleware = generic request preprocessing; Guard = may
request access route?; Pipe = validate/transform input; Interceptor =
wrap execution/response; Filter = translate uncaught exceptions.

**Detailed:** Choosing the correct lifecycle mechanism keeps concerns
explicit. Don't put authorization in a validation pipe or DTO validation
in a guard.

**Small code example / visual:**

``` ts
@UseGuards(AuthGuard, PermissionsGuard)
@Permissions("orders:write")
@Post()
create() {}
```

### 75 - Guard? ★★★

**TL;DR:** Determines whether a request is allowed to continue,
typically authentication/authorization.

**Detailed:** Implements `CanActivate` and gets `ExecutionContext`,
allowing access to handler/controller metadata and request. Good for JWT
auth, roles, permissions.

**Small code example / visual:**

``` ts
@UseGuards(AuthGuard, PermissionsGuard)
@Permissions("orders:write")
@Post()
create() {}
```

### 76 - Pipe? ★★★

**TL;DR:** Validates or transforms incoming handler arguments before the
controller receives them.

**Detailed:** Built-ins include parsing primitives. `ValidationPipe` can
validate DTOs and optionally transform payloads. Invalid input should
fail before business logic.

**Small code example / visual:**

``` ts
@Get(":id")
find(@Param("id", ParseIntPipe) id: number) {
  return this.service.find(id);
}
```

### 77 - Interceptor? ★★★

**TL;DR:** Wraps handler execution and can run logic before/after
it---useful for timing, logging, response transformation, caching, and
cross-cutting behavior.

**Detailed:** Nest interceptors use RxJS around `next.handle()`. They
are conceptually similar to AOP around advice.

**Small code example / visual:**

``` ts
intercept(ctx, next) {
  const start = Date.now();
  return next.handle().pipe(finalize(() => log(Date.now() - start)));
}
```

### 78 - Middleware? ★★★

**TL;DR:** Runs early in request processing and is useful for generic
HTTP concerns such as request IDs, basic logging, or integrating
Express/Fastify middleware.

**Detailed:** It generally lacks the route-handler metadata awareness
that guards/interceptors have.

**Small code example / visual:**

``` ts
function requestId(req, res, next) {
  req.requestId = crypto.randomUUID();
  next();
}
```

### 79 - Exception Filter? ★★★

**TL;DR:** Catches exceptions that escape request processing and maps
them to controlled responses/logging.

**Detailed:** Useful for consistent API error shape or translating
domain/infrastructure exceptions. Avoid leaking stack traces/internal
details to clients.

**Small code example / visual:**

``` ts
@Catch(DomainError)
class DomainFilter {
  catch(err, host) {
    host.switchToHttp().getResponse().status(422).json({ code: err.code });
  }
}
```

### 80 - DTO? ★★★

**TL;DR:** A DTO defines the data contract crossing a boundary, such as
an incoming create-user request. In Nest it can also carry runtime
validation metadata.

**Detailed:** DTOs separate API input/output contracts from
persistence/domain models and prevent accidental mass assignment of
arbitrary fields.

**Small code example / visual:**

``` ts
class CreateUserDto {
  @IsEmail() email: string;
  @MinLength(8) password: string;
}
```

### 81 - ValidationPipe? ★★★

**TL;DR:** Validates incoming DTO instances using configured validators
and can transform payloads into expected types.

**Detailed:** Common options include `whitelist` to remove unknown
fields and `forbidNonWhitelisted` to reject them. Validation is runtime
protection; TypeScript alone is not enough.

**Small code example / visual:**

``` ts
@Get(":id")
find(@Param("id", ParseIntPipe) id: number) {
  return this.service.find(id);
}
```

### 82 - Authentication in NestJS? ★★★

**TL;DR:** Verify credentials at login, issue/manage session or tokens,
then use a Guard to authenticate protected requests and attach trusted
identity to the request/context.

**Detailed:** Passwords must be securely hashed. Validate token
signature/expiry/issuer/audience as applicable. Refresh/token
rotation/revocation strategy depends on risk model.

**Small code example / visual:**

``` ts
@UseGuards(JwtAuthGuard)
@Get("me")
me(@CurrentUser() user: AuthUser) {
  return user;
}
```

### 83 - Authentication vs authorization? ★★★

**TL;DR:** Authentication answers "who are you?"; authorization answers
"are you allowed to do this?"

**Small code example / visual:**

``` ts
@UseGuards(JwtAuthGuard)
@Get("me")
me(@CurrentUser() user: AuthUser) {
  return user;
}
```

### 84 - Roles/permissions? ★★★

**TL;DR:** Put required permission metadata on handlers and enforce it
in a Guard using the authenticated user plus `Reflector`.

**Detailed:** Prefer capability/permission checks for complex systems
rather than scattering role-name comparisons throughout business code.

**Small code example / visual:**
```ts
@Permissions("orders:write")
@UseGuards(JwtAuthGuard, PermissionsGuard)
@Post("orders")
createOrder(@Body() dto: CreateOrderDto) {
  return this.orders.create(dto);
}
```

### 85 - Modularize large Nest app? ★★★

**TL;DR:** Organize around business domains/features with explicit
public boundaries; keep controllers thin and avoid giant shared
modules/services.

**Detailed:** For example `UsersModule`, `OrdersModule`,
`BillingModule`. Each owns application logic and persistence access.
Shared technical utilities should be truly cross-cutting.

**Small code example / visual:**
```text
AppModule
├─ UsersModule
│  ├─ UsersController
│  └─ UsersService
├─ OrdersModule
└─ BillingModule

Prefer business/domain boundaries over one giant SharedModule.
```

### 86 - Circular dependencies? ★★★

**TL;DR:** Usually a design smell indicating boundaries are coupled.
Extract shared responsibility, introduce events/abstractions, or
reorganize ownership before reaching for `forwardRef`.

**Small code example / visual:**

``` text
Bad: OrdersService <-> PaymentsService
Better: Orders -> CheckoutUseCase <- Payments
Extract the shared/orchestration responsibility.
```

### 87 - Provider scopes? ★★

**TL;DR:** Default singleton scope reuses a provider; request scope
creates one per request; transient creates one per injection. Prefer
singleton unless lifecycle-specific state requires otherwise.

**Detailed:** Request scope adds overhead and can propagate scope
through dependency graphs.

**Small code example / visual:**
```ts
@Injectable() // singleton by default
class CatalogService {}

@Injectable({ scope: Scope.REQUEST })
class RequestContext {}

@Injectable({ scope: Scope.TRANSIENT })
class TemporaryFormatter {}
```

### 88 - Testing Nest? ★★★

**TL;DR:** Unit-test services with mocked dependencies, integration-test
modules/infrastructure, and E2E-test important HTTP flows using a real
Nest application.

**Small code example / visual:**
```ts
const module = await Test.createTestingModule({
  providers: [
    UsersService,
    { provide: UsersRepository, useValue: repoMock }
  ]
}).compile();

const service = module.get(UsersService);
```

### 89 - Mock dependencies? ★★

**TL;DR:** Build a `TestingModule` and replace provider tokens with
controlled mocks/fakes so the unit under test is isolated.

**Small code example / visual:**

``` ts
const gateway = {
  charge: jest.fn().mockResolvedValue({ id: "pay_1" })
};
```

### 90 - Transactions? ★★★

**TL;DR:** Put operations that must succeed/fail atomically inside a
database transaction and keep the transaction boundary in the
application/service layer that owns the use case.

**Detailed:** Keep transactions short; avoid unnecessary external
network calls inside them. Handle retries/deadlocks where relevant.

**Small code example / visual:**

``` sql
BEGIN;
UPDATE accounts SET balance=balance-100 WHERE id=1;
UPDATE accounts SET balance=balance+100 WHERE id=2;
COMMIT;
```

### 91 - Correlation IDs? ★★

**TL;DR:** Assign/propagate a request ID and include it in structured
logs/traces so events across layers/services can be connected.

**Small code example / visual:**

``` ts
logger.info({
  requestId: req.requestId,
  userId: req.user?.id,
  path: req.url
}, "request");
```

### 92 - Centralized errors? ★★★

**TL;DR:** Throw meaningful domain/application exceptions, translate
them consistently at a boundary (often filters), log internal context,
and expose safe stable error responses.

**Small code example / visual:**
```ts
throw new OrderNotFoundError(id);

// Global ExceptionFilter translates it to:
// HTTP 404
// { code: "ORDER_NOT_FOUND", requestId: "req_123" }
```

### 93 - Protect API from abuse? ★★★

**TL;DR:** Authentication/authorization, validation, rate limiting,
payload limits, secure headers/CORS as appropriate, least privilege,
audit/logging, and dependency/security hygiene.

**Small code example / visual:**
```ts
@UseGuards(JwtAuthGuard, PermissionsGuard, RateLimitGuard)
@Post("orders")
create(@Body() dto: CreateOrderDto) {
  // DTO validation + auth + authorization + rate limit before business logic
  return this.service.create(dto);
}
```

### 94 - Slow Nest endpoint? ★★★

**TL;DR:** Measure → trace → DB/external calls/application CPU →
optimize → measure again.

**Detailed:** Nest itself is rarely the first assumption. Check N+1
queries, indexes, sequential awaits, excessive serialization, huge DTOs,
blocking work, pool saturation, external dependencies, and caching.

**Small code example / visual:**
```ts
// Sequential when unnecessary:
const user = await users.find(id);
const orders = await ordersRepo.findByUser(id);

// If independent, run concurrently:
const [user2, orders2] = await Promise.all([
  users.find(id),
  ordersRepo.findByUser(id)
]);
```

### 95 - Custom decorators? ★★

**TL;DR:** Encapsulate reusable metadata or parameter extraction,
e.g. `@CurrentUser()` or `@Permissions(...)`, keeping controllers
declarative.

**Small code example / visual:**

``` ts
@Controller("users")
class UsersController {
  @Get(":id") find(@Param("id") id: string) {}
}
```

### 96 - Dynamic modules? ★★

**TL;DR:** Modules configurable at import time, often via
`forRoot/forRootAsync`, useful for reusable infrastructure libraries
needing configuration/providers.

**Small code example / visual:**

``` ts
@Module({
  controllers: [OrdersController],
  providers: [OrdersService],
  exports: [OrdersService]
})
export class OrdersModule {}
```

### 97 - Configuration? ★★★

**TL;DR:** Centralize typed configuration, validate required environment
values at startup, separate environments, and inject config rather than
reading arbitrary `process.env` everywhere.

**Small code example / visual:**
```ts
ConfigModule.forRoot({
  isGlobal: true,
  validate: env => EnvSchema.parse(env)
});

@Injectable()
class ApiClient {
  constructor(private config: ConfigService) {}
}
```

### 98 - Idempotent endpoint? ★★★

**TL;DR:** Repeating the same logical request must not duplicate its
effect. Accept an idempotency key, persist its result/operation identity
atomically, and return the existing result on retries.

**Detailed:** Especially important for payments/create operations where
clients retry after timeouts. DB unique constraints are useful final
protection against races.

**Small code example / visual:**

``` http
POST /payments
Idempotency-Key: checkout-abc-123

# Retry with same key -> same logical effect/result
```

### 99 - When NOT microservices? ★★★

**TL;DR:** Don't introduce them merely for "scalability." A modular
monolith is simpler when the team/domain/scale doesn't justify network
boundaries and operational complexity.

**Detailed:** Microservices add deployment, observability, consistency,
latency, versioning, and debugging complexity. Split when there are real
independent scaling, ownership, reliability, or domain-boundary
benefits.

**Small code example / visual:**

``` text
One team + one domain + same scaling needs -> modular monolith
Independent ownership/scaling boundary emerges -> consider extraction
```

### 100 - Refactor a giant Nest service? ★★★

**TL;DR:** Don't freeze everything and rewrite blindly. Characterize
behavior with tests/observability, identify responsibilities, extract
incrementally behind stable interfaces, deploy safely, and measure.

**Detailed:** Use the strangler approach where appropriate. Separate
domain/application responsibilities first; "smaller services" does not
automatically mean network microservices. Preserve business behavior and
migrate incrementally to reduce rewrite risk.

------------------------------------------------------------------------

**Small code example / visual:**
```text
Before:
OrdersService (1,500 lines)

After incremental extraction:
OrdersController -> CheckoutUseCase
                 -> OrderPricingService
                 -> OrderValidator
                 -> OrderRepository
```

## REST / Backend

### 101 - RESTful API? ★★★

**TL;DR:** Model resources with predictable URIs and HTTP semantics,
keep requests stateless, use appropriate methods/status codes, and
expose consistent representations.

**Small code example / visual:**
```http
GET    /orders/42
POST   /orders
PATCH  /orders/42
DELETE /orders/42

# Resources + HTTP semantics, rather than RPC-style /createOrder
```

### 102 - PUT vs PATCH? ★★★

**TL;DR:** PUT conventionally replaces the resource representation and
is idempotent; PATCH applies a partial modification.

**Small code example / visual:**

``` http
PUT /users/42   # replace representation
PATCH /users/42 # partial modification
```

### 103 - Status codes? ★★★

**TL;DR:** 200 OK; 201 Created; 204 No Content; 400 invalid request; 401
unauthenticated; 403 authenticated but forbidden; 404 missing; 409
conflict; 422 semantically invalid (depending API convention); 429 rate
limited; 500 unexpected server error.

**Small code example / visual:**

``` http
POST /orders -> 201 Created
GET /orders/999 -> 404 Not Found
Invalid body -> 400
No permission -> 403
```

### 104 - Pagination? ★★★

**TL;DR:** Bound collection responses and return stable pagination
metadata/cursors. Ensure deterministic ordering.

**Small code example / visual:**

``` http
GET /orders?limit=20&cursor=abc123
{
  "items": [...],
  "nextCursor": "def456"
}
```

### 105 - Offset vs cursor? ★★★

**TL;DR:** Offset is simple and supports page numbers but becomes
inefficient/inconsistent at large changing datasets; cursor pagination
is more stable/scalable for sequential navigation.

**Small code example / visual:**
```http
# Offset pagination
GET /orders?limit=20&offset=100

# Cursor pagination
GET /orders?limit=20&after=order_100
```

### 106 - Filtering/sorting? ★★★

**TL;DR:** Use explicit query parameters, validate allowed
fields/operators, apply deterministic sorting, and ensure common query
patterns are indexed.

**Small code example / visual:**

``` http
GET /orders?status=paid&minTotal=50&sort=-createdAt
```

### 107 - Idempotency? ★★★

**TL;DR:** Multiple identical requests have the same intended effect as
one. GET/PUT/DELETE are conceptually idempotent; POST operations can add
explicit idempotency keys.

**Small code example / visual:**
```http
POST /payments
Idempotency-Key: checkout-abc-123

# First request creates payment.
# Retry with same key returns same logical result, not a second charge.
```

### 108 - API versioning? ★★★

**TL;DR:** Prefer backward-compatible evolution. For breaking changes
use an explicit strategy such as URL/header versioning, deprecate old
versions, communicate and observe usage.

**Small code example / visual:**

``` http
GET /v1/orders/42
GET /v2/orders/42
# Prefer backward compatibility before introducing a new version.
```

### 109 - API errors? ★★★

**TL;DR:** Stable machine-readable code + safe human message + relevant
field/details + correlation/request ID. Never leak internal stack
traces/secrets.

**Small code example / visual:**

``` json
{
  "code": "ORDER_NOT_FOUND",
  "message": "Order was not found",
  "requestId": "req_123"
}
```

### 110 - Input validation? ★★★

**TL;DR:** Validate type, shape, ranges, format, business constraints,
and authorization at the boundary; reject unknown/unexpected data where
appropriate.

**Small code example / visual:**
```ts
class CreateOrderDto {
  @IsInt()
  @Min(1)
  quantity: number;

  @IsUUID()
  productId: string;
}
```

### 111 - Secure REST API? ★★★

**TL;DR:** TLS, authn/authz, validation, least privilege, secure
secrets, rate limits, safe error handling, dependency hygiene,
auditability, and protection against relevant OWASP risks.

**Small code example / visual:**
```text
Internet
  -> TLS
  -> Authentication
  -> Authorization
  -> Validation + payload limits
  -> Rate limiting
  -> Business logic
  -> DB with least-privilege credentials
```

### 112 - JWT vs sessions? ★★★

**TL;DR:** Sessions keep server-side auth state and use an opaque
cookie/id; JWTs carry signed claims and can enable stateless
verification but complicate revocation. Choose based on
architecture/security needs.

**Small code example / visual:**
```text
Session model:
Browser cookie(session_id) -> API -> server-side session store

JWT model:
Authorization: Bearer <signed claims> -> API verifies signature/expiry
```

### 113 - Access vs refresh token? ★★

**TL;DR:** Access tokens are short-lived credentials for APIs; refresh
tokens are longer-lived credentials used to obtain new access tokens and
need stronger storage/rotation/revocation protection.

**Small code example / visual:**
```text
Access token: short-lived, used on normal API requests
Refresh token: longer-lived, used only to obtain a new access token

Refresh token compromise is more serious, so protect/rotate/revoke it carefully.
```

### 114 - Rate limiting? ★★★

**TL;DR:** Limit requests per identity/IP/API key/window to protect
capacity and abuse-sensitive operations; return 429 when exceeded.

**Small code example / visual:**

``` http
HTTP/1.1 429 Too Many Requests
Retry-After: 30
```

### 115 - Caching? ★★★

**TL;DR:** Store expensive-to-compute/fetch data closer to consumers.
Possible layers: browser/CDN, application memory, Redis, DB caches.
Every cache needs an invalidation/freshness strategy.

**Small code example / visual:**
```text
Browser/CDN cache
       ↓
Application / Redis cache
       ↓
Database

Cache hit -> avoid expensive work
Cache miss -> fetch -> cache -> return
```

### 116 - Avoid race conditions? ★★★

**TL;DR:** Put correctness in atomic database
operations/transactions/constraints rather than relying on "check then
write" in application memory.

**Small code example / visual:**

``` sql
UPDATE inventory
SET stock = stock - 1
WHERE id = 42 AND stock > 0;
-- atomic conditional update
```

### 117 - Optimistic vs pessimistic locking? ★★★

**TL;DR:** Optimistic locking detects concurrent changes (version field)
and retries/rejects; pessimistic locking acquires DB locks before
modification. Optimistic suits low contention; pessimistic stronger
contention-sensitive operations.

**Small code example / visual:**

``` sql
SELECT * FROM orders WHERE id=$1 FOR UPDATE;
-- pessimistic lock inside a transaction
```

### 118 - Long-running operation? ★★★

**TL;DR:** Return quickly with an operation/job ID (often 202 Accepted),
execute asynchronously outside the request lifecycle, persist status,
and let clients poll or receive a supported notification mechanism.

**Small code example / visual:**

``` http
POST /reports -> 202 Accepted
{ "operationId": "op_123" }
GET /operations/op_123 -> { "status": "done" }
```

### 119 - File uploads? ★★★

**TL;DR:** Validate metadata/size/type, stream rather than buffering
large files, preferably upload directly to object storage with signed
URLs, scan/process asynchronously, and store metadata in DB.

**Small code example / visual:**

``` text
Client -> API gets signed URL -> Object Storage
                              -> processing/validation
DB stores metadata/key, not giant file bytes.
```

### 120 - Observable endpoint? ★★★

**TL;DR:** Structured logs + request/correlation IDs +
latency/error/request metrics + distributed traces where useful +
dashboards/alerts.

------------------------------------------------------------------------

**Small code example / visual:**

``` text
request_id=req_123 status=200 latency_ms=42
Metrics: rate / p95 latency / errors
Trace: API -> DB -> external dependency
```

## Databases

### 121 - SQL vs NoSQL? ★★★

**TL;DR:** Choose from data model/access patterns/consistency needs. SQL
excels at relational integrity, joins and transactions; document/NoSQL
databases can suit flexible aggregate-shaped data and particular
scaling/access patterns.

**Small code example / visual:**

``` text
Relational + transactions + joins -> PostgreSQL likely fits
Document-shaped flexible aggregate -> MongoDB may fit
Choose from access/consistency requirements.
```

### 122 - Index? ★★★

**TL;DR:** A data structure that lets the DB find rows without scanning
the entire table, trading extra storage/write cost for faster reads.

**Small code example / visual:**
```sql
CREATE INDEX idx_orders_user_id
ON orders(user_id);

SELECT id,total
FROM orders
WHERE user_id = 42;
```

### 123 - Index trade-offs? ★★★

**TL;DR:** Faster relevant reads, but additional disk/memory and slower
inserts/updates/deletes because indexes must also be maintained.

**Small code example / visual:**
```sql
CREATE INDEX idx_orders_status ON orders(status);

-- Benefit: faster relevant reads.
-- Cost: INSERT/UPDATE/DELETE must maintain the index too.
```

### 124 - Composite index ordering? ★★★

**TL;DR:** An index on `(a,b)` is ordered first by `a`, then `b`; column
order should reflect real filtering/sorting patterns and
selectivity/query behavior.

**Detailed:** The leftmost-prefix concept means `(user_id, created_at)`
naturally supports queries starting with `user_id`; it isn't equivalent
to `(created_at, user_id)`. Verify with execution plans rather than
guessing.

**Small code example / visual:**

``` sql
CREATE INDEX idx_orders_user_created
ON orders(user_id, created_at DESC);
```

### 125 - Query plan? ★★★

**TL;DR:** The DB optimizer's chosen strategy for executing a query:
scans, indexes, joins, estimated/actual rows and costs. Use
`EXPLAIN`/`EXPLAIN ANALYZE` to understand slow queries.

**Small code example / visual:**
```sql
EXPLAIN ANALYZE
SELECT id,total
FROM orders
WHERE user_id = 42
ORDER BY created_at DESC;
```

### 126 - N+1? ★★★

**TL;DR:** Fetch one list, then issue one extra query per item. It
creates many round trips. Fix with joins, batching, eager/preloading
where appropriate.

**Small code example / visual:**

``` sql
SELECT o.*, u.name
FROM orders o
JOIN users u ON u.id = o.user_id;
-- instead of one user query per order
```

### 127 - Transaction? ★★★

**TL;DR:** Groups operations into one atomic unit so either all commit
or all roll back.

**Small code example / visual:**

``` sql
BEGIN;
UPDATE accounts SET balance=balance-100 WHERE id=1;
UPDATE accounts SET balance=balance+100 WHERE id=2;
COMMIT;
```

### 128 - ACID? ★★★

**TL;DR:** Atomicity = all/none; Consistency = constraints/invariants
preserved; Isolation = concurrent transactions behave according to
defined isolation guarantees; Durability = committed data survives
failures.

**Small code example / visual:**

``` text
Transfer €100:
Atomicity -> debit+credit both happen or neither
Consistency -> invariants remain valid
Isolation -> concurrent transactions controlled
Durability -> commit survives failure
```

### 129 - Isolation levels? ★★★

**TL;DR:** Higher isolation reduces concurrency anomalies but may reduce
throughput/increase locking/retries. Common levels include Read
Committed, Repeatable Read, Serializable; exact guarantees vary by DB.

**Small code example / visual:**

``` sql
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- consistency-sensitive work
COMMIT;
```

### 130 - DB race condition? ★★★

**TL;DR:** Two concurrent operations read/write shared state in an order
that violates an invariant. Use atomic statements, constraints,
transactions, locks or optimistic concurrency.

**Small code example / visual:**

``` sql
UPDATE inventory
SET stock = stock - 1
WHERE id = 42 AND stock > 0;
-- atomic conditional update
```

### 131 - PK/unique/FK? ★★★

**TL;DR:** Primary key identifies each row; unique constraint prevents
duplicate values; foreign key enforces references between related
tables.

**Small code example / visual:**
```sql
CREATE TABLE orders (
  id BIGINT PRIMARY KEY,
  external_id TEXT UNIQUE,
  user_id BIGINT REFERENCES users(id)
);
```

### 132 - Normalize vs denormalize? ★★★

**TL;DR:** Normalize to reduce duplication and preserve integrity;
denormalize selectively to optimize read patterns when measured benefits
justify consistency complexity.

**Small code example / visual:**
```sql
-- Normalized:
orders(user_id) -> users(id, name, email)

-- Selective denormalization example:
order_summary(order_id, customer_name_snapshot, total)
```

### 133 - Connection pooling? ★★

**TL;DR:** Reuses a bounded set of DB connections. Size it across all
service instances so the application doesn't exhaust DB connection
limits.

**Small code example / visual:**
```text
10 API instances × pool max 20 = up to 200 DB connections

A pool is configured per process/instance, so size it against the database limit across the whole deployment.
```

### 134 - Redis? ★★★

**TL;DR:** Fast in-memory store commonly used for caching, rate
limiting, ephemeral state, distributed coordination primitives, and
other low-latency access patterns.

**Small code example / visual:**

``` ts
const cached = await redis.get(`product:${id}`);
if (cached) return JSON.parse(cached);
const p = await db.product.find(id);
await redis.set(`product:${id}`, JSON.stringify(p), { EX: 60 });
```

### 135 - Cache invalidation? ★★★

**TL;DR:** Decide when cached data becomes stale and how it is
refreshed/removed. TTL, explicit invalidation, versioned keys, or
event-driven invalidation are common approaches.

**Small code example / visual:**

``` ts
await db.product.update(id, input);
await redis.del(`product:${id}`);
```

### 136 - Cache-aside? ★★

**TL;DR:** Application checks cache → on miss reads DB → stores result
in cache → returns. Writes usually update DB then invalidate/update
cache.

**Small code example / visual:**

``` text
GET -> cache hit -> return
    -> miss -> DB -> cache SET with TTL -> return
WRITE -> DB -> invalidate/update cache
```

### 137 - TTL? ★★

**TL;DR:** Time To Live automatically expires cached/ephemeral data
after a duration, limiting staleness and storage growth.

**Small code example / visual:**

``` text
SET product:42 "{...}" EX 60
# entry expires automatically after 60 seconds
```

### 138 - Slow SQL query? ★★★

**TL;DR:** Reproduce/measure → execution plan → scans/indexes →
rows/selectivity → joins/N+1 → data volume → query rewrite/index →
measure again.

**Small code example / visual:**

``` sql
EXPLAIN ANALYZE
SELECT id, created_at
FROM orders
WHERE user_id=42
ORDER BY created_at DESC
LIMIT 20;
```

### 139 - Why avoid `SELECT *`? ★★★

**TL;DR:** Fetch only required columns to reduce
I/O/network/serialization and avoid coupling consumers to irrelevant
schema fields.

**Small code example / visual:**

``` sql
SELECT id, name, email
FROM users
WHERE id=$1; -- fetch only required columns
```

### 140 - Safe migrations? ★★★

**TL;DR:** Prefer backward-compatible expand/migrate/contract changes:
add new schema first, deploy compatible code, backfill safely, switch
reads/writes, remove old schema later.

**Detailed:** Avoid locking huge tables unexpectedly; test migration
duration, have backups/rollback strategy, and don't couple destructive
migration with code that assumes it instantly completed everywhere.

------------------------------------------------------------------------

**Small code example / visual:**

``` sql
ALTER TABLE users ADD COLUMN display_name TEXT;
-- deploy compatible code + backfill first
-- remove old schema only in a later safe deploy
```

## React

### 141 - What causes render? ★★★

**TL;DR:** Initial mount, state updates, parent renders, or consumed
context changes can cause a component function to run again. Memoization
may skip some renders when inputs are unchanged.

**Small code example / visual:**
```tsx
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
// setCount schedules a re-render of Counter
```

### 142 - Reconciliation? ★★★

**TL;DR:** React compares the new element tree with the previous one and
determines the minimal host DOM updates required.

**Small code example / visual:**

``` tsx
// Same type + stable key helps React preserve identity:
<UserRow key={user.id} user={user} />
```

### 143 - Virtual DOM? ★★★

**TL;DR:** An in-memory representation of desired UI. React reconciles
representations and applies required changes to the real DOM.

**Small code example / visual:**

``` tsx
const element = <h1>Hello {name}</h1>;
// React compares desired element tree with previous tree,
// then updates necessary DOM nodes.
```

### 144 - `useEffect`? ★★★

**TL;DR:** Synchronizes a component with an external system after
rendering---network subscriptions, DOM APIs, timers, third-party
systems. It is not the default place for derived state.

**Small code example / visual:**

``` tsx
useEffect(() => {
  const sub = chat.subscribe(roomId);
  return () => sub.unsubscribe();
}, [roomId]);
```

### 145 - `useEffect` mistakes? ★★★

**TL;DR:** Missing/wrong dependencies, infinite update loops, stale
closures, failing cleanup, unnecessary effects, and request race
conditions.

**Small code example / visual:**

``` tsx
useEffect(() => {
  const sub = chat.subscribe(roomId);
  return () => sub.unsubscribe();
}, [roomId]);
```

### 146 - `useMemo` vs `useCallback`? ★★★

**TL;DR:** `useMemo` memoizes a computed value; `useCallback` memoizes a
function reference. Use them when they solve measured/relevant
referential or computational problems---not automatically.

**Small code example / visual:**

``` tsx
const filtered = useMemo(() => filter(items, query), [items, query]);
const onSave = useCallback(() => save(id), [id]);
```

### 147 - `useRef`? ★★★

**TL;DR:** Holds a mutable value across renders without triggering a
render when it changes; also references DOM nodes.

**Small code example / visual:**

``` tsx
const inputRef = useRef<HTMLInputElement>(null);
<input ref={inputRef} />
<button onClick={() => inputRef.current?.focus()}>Focus</button>
```

### 148 - Controlled vs uncontrolled? ★★★

**TL;DR:** Controlled inputs derive their value from React state;
uncontrolled inputs keep state in the DOM and are read via refs/form
APIs.

**Small code example / visual:**

``` tsx
<input value={name} onChange={e => setName(e.target.value)} />
// uncontrolled: <input ref={nameRef} defaultValue="Ana" />
```

### 149 - Local vs global state? ★★★

**TL;DR:** Keep state as close as possible to where it's consumed;
lift/share it only when coordination requirements justify broader
ownership.

**Small code example / visual:**
```tsx
function ProductModal() {
  const [open, setOpen] = useState(false); // local: only this feature needs it
  return <Modal open={open} />;
}

// Move state higher/global only when distant consumers need coordination.
```

### 150 - Context vs Redux/Zustand? ★★★

**TL;DR:** Context is built-in dependency/state propagation and suits
relatively stable shared values; dedicated stores offer stronger
patterns/selectors/tooling for complex frequently-changing application
state.

**Small code example / visual:**

``` tsx
<ThemeContext.Provider value={theme}>
  <App />
</ThemeContext.Provider>
```

### 151 - Server vs client state? ★★★

**TL;DR:** Server state is remote, asynchronous, cached and potentially
stale; client state belongs to the UI/application. Treating server data
like ordinary global state recreates caching/refetch complexity.

**Small code example / visual:**
```tsx
// Server state: remote, cacheable, can become stale
const { data: user } = useQuery({
  queryKey: ["user", id],
  queryFn: () => api.getUser(id)
});

// Client/UI state:
const [modalOpen, setModalOpen] = useState(false);
```

### 152 - TanStack Query? ★★★

**TL;DR:** Manages server-state fetching, caching, deduplication,
freshness, retries, invalidation, mutations and loading/error states.

**Small code example / visual:**
```tsx
const { data, isLoading, error } = useQuery({
  queryKey: ["orders", userId],
  queryFn: () => getOrders(userId),
  staleTime: 30_000
});
```

### 153 - Prevent unnecessary renders? ★★★

**TL;DR:** First measure. Keep state local, avoid unnecessary parent
updates/context breadth, use stable keys, split components, and apply
memo/useMemo/useCallback selectively.

**Small code example / visual:**

``` tsx
const Row = memo(function Row({ item }: Props) {
  return <div>{item.name}</div>;
});
// Only when memoization solves a real cost.
```

### 154 - Keys? ★★

**TL;DR:** Stable keys identify list items across renders so React
preserves the correct component identity/state. Avoid array index when
order can change.

**Small code example / visual:**
```tsx
{users.map(user => (
  <UserRow key={user.id} user={user} />
))}
// Stable key = React can preserve the correct item identity across reorders.
```

### 155 - Error Boundaries? ★★★

**TL;DR:** Catch rendering/lifecycle errors in descendant React trees
and render fallback UI. They don't catch every async/event-handler
error.

**Small code example / visual:**

``` tsx
<ErrorBoundary fallback={<ErrorPage />}>
  <Checkout />
</ErrorBoundary>
```

### 156 - Code splitting? ★★★

**TL;DR:** Load code only when needed using dynamic imports/lazy
loading, reducing initial bundle cost.

**Small code example / visual:**

``` tsx
const AdminPage = lazy(() => import("./AdminPage"));
<Suspense fallback={<Spinner />}><AdminPage /></Suspense>
```

### 157 - Composition? ★★

**TL;DR:** Build complex UI by combining smaller components/children
instead of deep inheritance; React strongly favors composition.

**Small code example / visual:**

``` tsx
function Card({ children }) {
  return <section>{children}</section>;
}
<Card><UserProfile /></Card>
```

### 158 - Structure large React app? ★★★

**TL;DR:** Feature/domain-oriented modules, clear UI/data boundaries,
reusable primitives, server-state layer, local state by default,
consistent routing/error/loading patterns.

**Small code example / visual:**
```text
src/
├─ features/
│  ├─ orders/
│  │  ├─ api.ts
│  │  ├─ components/
│  │  └─ hooks.ts
│  └─ users/
├─ components/ui/
└─ routes/

Keep feature behavior close together.
```

### 159 - Test React? ★★★

**TL;DR:** Test user-visible behavior rather than implementation
details. Component/integration tests simulate interactions and assert
what users see; E2E covers critical journeys.

**Small code example / visual:**
```tsx
render(<Login />);
await user.type(screen.getByLabelText("Email"), "a@x.com");
await user.click(screen.getByRole("button", { name: "Sign in" }));
expect(await screen.findByText("Welcome")).toBeVisible();
```

### 160 - Accessibility? ★★

**TL;DR:** Semantic HTML first, keyboard access, labels, focus
management, appropriate ARIA only when necessary, contrast, and
screen-reader-friendly states.

------------------------------------------------------------------------

**Small code example / visual:**

``` html
<label for="email">Email</label>
<input id="email" type="email" />
<button type="submit">Sign in</button>
```

## Testing

### 161 - Unit/integration/E2E? ★★★

**TL;DR:** Unit isolates small logic; integration verifies
components/infrastructure working together; E2E validates complete
user/system flows.

**Small code example / visual:**
```text
Unit:
calculateTotal(order) -> pure function

Integration:
OrdersRepository -> real PostgreSQL test DB

E2E:
POST /orders -> Nest HTTP -> service -> DB -> response
```

### 162 - What mock? ★★★

**TL;DR:** Mock unstable/slow/external boundaries when isolation is the
goal, not every internal class. Over-mocking tests implementation rather
than behavior.

**Small code example / visual:**

``` ts
const gateway = {
  charge: jest.fn().mockResolvedValue({ id: "pay_1" })
};
```

### 163 - Good unit test? ★★★

**TL;DR:** Fast, deterministic, isolated, readable, focused on behavior,
and includes meaningful edge/failure cases.

**Small code example / visual:**

``` ts
it("rejects negative quantity", () => {
  expect(() => createOrder({ quantity: -1 })).toThrow();
});
```

### 164 - Testing pyramid? ★★★

**TL;DR:** Many fast unit tests, fewer integration tests, and a smaller
number of expensive E2E tests---adapt based on product risk.

**Small code example / visual:**

``` text
        E2E        few
     Integration    some
   Unit tests       many/fast
```

### 165 - Test REST endpoint? ★★★

**TL;DR:** Verify success plus validation, auth/authz, missing
resources, conflicts/failures, status/body contract, and relevant side
effects.

**Small code example / visual:**

``` ts
await request(app.getHttpServer())
  .post("/orders")
  .send({ quantity: 0 })
  .expect(400);
```

### 166 - Test DB code? ★★★

**TL;DR:** Important query/repository behavior benefits from integration
tests against a real compatible database because mocks don't reproduce
SQL constraints/transactions/query behavior.

**Small code example / visual:**
```ts
beforeEach(async () => resetDatabase());

await repo.create({ email: "a@x.com" });
await expect(repo.create({ email: "a@x.com" }))
  .rejects.toThrow(); // verifies real UNIQUE constraint behavior
```

### 167 - Flaky tests? ★★

**TL;DR:** Tests that nondeterministically pass/fail due to timing,
shared state, randomness, environment, external dependencies. Remove
root cause; don't normalize endless retries.

**Small code example / visual:**

``` ts
// Fragile: await sleep(1000)
// Better: await the actual observable event/condition.
```

### 168 - CI checks? ★★★

**TL;DR:** Install reproducibly → lint/static checks → typecheck →
unit/integration tests → build → security/dependency checks as
appropriate → artifact/image creation → deploy gates.

**Small code example / visual:**
```yaml
steps:
  - run: npm ci
  - run: npm run lint
  - run: npm run typecheck
  - run: npm test
  - run: npm run build
```

### 169 - Coverage? ★★★

**TL;DR:** Useful signal for untested code, terrible proxy for quality
by itself. 100% coverage can still have useless assertions.

**Small code example / visual:**

``` ts
// Coverage is a signal, not the goal:
expect(calculateTotal(order)).toBe(42); // meaningful behavior assertion
```

### 170 - Failure paths? ★★★

**TL;DR:** Explicitly test invalid input, dependency failures,
permissions, timeouts, conflicts/races where reproducible, and
rollback/no-partial-side-effect behavior.

------------------------------------------------------------------------

**Small code example / visual:**

``` ts
gateway.charge.mockRejectedValue(new Error("down"));
await expect(service.checkout(input)).rejects.toThrow();
expect(repo.save).not.toHaveBeenCalled();
```

## Docker / CI/CD / AWS

### 171 - Docker? ★★★

**TL;DR:** Packages an application and its runtime dependencies into an
image that runs as an isolated, reproducible container.

**Small code example / visual:**

``` dockerfile
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY dist ./dist
CMD ["node", "dist/main.js"]
```

### 172 - Image vs container? ★★★

**TL;DR:** Image = immutable template/artifact; container = running
instance of an image with a writable runtime layer.

**Small code example / visual:**

``` bash
docker build -t api:1.0 . # image
docker run api:1.0          # running container
```

### 173 - Dockerfile? ★★★

**TL;DR:** Declarative recipe for building an image: base image,
dependencies, files, build steps, user, command, etc.

**Small code example / visual:**

``` dockerfile
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY dist ./dist
CMD ["node", "dist/main.js"]
```

### 174 - Layers? ★★★

**TL;DR:** Dockerfile steps create cacheable filesystem layers. Order
stable dependency installation before frequently-changing source files
to improve build caching.

**Small code example / visual:**

``` dockerfile
COPY package*.json ./
RUN npm ci       # cacheable dependency layer
COPY . .         # source changes more often
```

### 175 - Multi-stage build? ★★★

**TL;DR:** Build in one stage with compilers/dev dependencies, copy only
production artifacts into a smaller runtime stage.

**Small code example / visual:**

``` dockerfile
FROM node:22 AS build
COPY . /app
RUN cd /app && npm ci && npm run build

FROM node:22-alpine
COPY --from=build /app/dist ./dist
```

### 176 - Volume vs bind mount? ★★★

**TL;DR:** Docker-managed volume persists data independently of a
container; bind mount maps a specific host path into the container.

**Small code example / visual:**

``` bash
docker run -v postgres_data:/var/lib/postgresql/data postgres
# named volume persists DB data
```

### 177 - Container vs VM? ★★★

**TL;DR:** Containers share the host kernel and isolate processes; VMs
virtualize hardware and run separate guest OS kernels. Containers are
typically lighter/faster.

**Small code example / visual:**

``` text
VM: Hardware -> Hypervisor -> Guest OS -> App
Container: Host kernel -> Container runtime -> App process
```

### 178 - Don't store in image? ★★★

**TL;DR:** Secrets, credentials, environment-specific sensitive config,
or mutable application data.

**Small code example / visual:**
```dockerfile
# BAD: secret becomes part of image metadata/layers
ENV DB_PASSWORD=super-secret

# GOOD: inject at runtime from Secrets Manager / platform secret store
CMD ["node", "dist/main.js"]
```

### 179 - Good CI/CD pipeline? ★★★

**TL;DR:** Reproducible build → lint/typecheck/tests/security checks →
immutable artifact/image → registry → staged deployment → health
verification → observability → safe promotion/rollback.

**Small code example / visual:**

``` ts
@Get(":id")
find(@Param("id", ParseIntPipe) id: number) {
  return this.service.find(id);
}
```

### 180 - CI vs CD? ★★★

**TL;DR:** CI continuously integrates and validates changes; continuous
delivery keeps software deployable, while continuous deployment
automatically releases passing changes.

**Small code example / visual:**

``` text
CI = integrate + validate every change
CD = keep releasable / deploy validated artifact
```

### 181 - After `git push`? ★★★

**TL;DR:** CI triggers → checkout/install → lint/typecheck/tests → build
image/artifact → scan → push registry → deploy environment → migration
strategy → health/smoke checks → traffic/promotion → monitor.

**Small code example / visual:**

``` yaml
steps:
  - run: npm ci
  - run: npm run lint && npm test
  - run: docker build -t api:${GITHUB_SHA} .
  - run: ./deploy.sh
```

### 182 - Rollback? ★★★

**TL;DR:** Deploy immutable versioned artifacts so the platform can
quickly route/redeploy the previous known-good version; database changes
must remain rollback-compatible.

**Small code example / visual:**
```text
Deploy immutable versions:
api:sha-111 (known good)
api:sha-222 (new release)

If sha-222 fails health/metrics -> redeploy or route traffic back to sha-111.
DB migrations must remain rollback-compatible.
```

### 183 - Blue/green vs rolling? ★★

**TL;DR:** Blue/green runs old/new environments and switches traffic;
rolling gradually replaces instances. Blue/green enables fast switchback
but costs more capacity.

**Small code example / visual:**

``` text
Blue v1 <- traffic
Green v2 <- deploy + verify
Switch traffic -> Green
Problem? switch back -> Blue
```

### 184 - Health check? ★★★

**TL;DR:** Liveness asks whether process should be restarted; readiness
asks whether it can safely receive traffic. Don't mark ready before
critical initialization completes.

**Small code example / visual:**

``` http
GET /health/live  -> 200
GET /health/ready -> 200
```

### 185 - Core AWS? ★★★

**TL;DR:** IAM (permissions), VPC/networking, compute (EC2/ECS/Lambda),
S3, RDS, load balancers, CloudFront, CloudWatch, Route 53, Secrets
Manager/Parameter Store.

**Small code example / visual:**

``` text
Route53 -> CloudFront/ALB -> ECS/Fargate -> RDS
                         |              |
                         S3          CloudWatch
IAM + VPC + Secrets Manager
```

### 186 - EC2 vs ECS/Fargate vs Lambda? ★★★

**TL;DR:** EC2 = manage VMs; ECS/Fargate = run containers with less
server management; Lambda = event-driven functions with managed scaling
and execution constraints.

**Small code example / visual:**

``` text
EC2 = VMs / more control+ops
ECS/Fargate = managed container compute
Lambda = managed event/function execution
```

### 187 - S3? ★★★

**TL;DR:** Durable object storage for files/assets/backups/data---not a
mounted relational filesystem/database.

**Small code example / visual:**

``` bash
aws s3 cp avatar.jpg s3://app-uploads/users/42/avatar.jpg
```

### 188 - RDS? ★★★

**TL;DR:** Managed relational databases such as PostgreSQL/MySQL with
backups, maintenance options, monitoring and HA features.

**Small code example / visual:**

``` text
NestJS tasks -> RDS PostgreSQL
              -> backups / monitoring / Multi-AZ as required
```

### 189 - CloudFront? ★★★

**TL;DR:** AWS CDN that caches/distributes content at edge locations,
often in front of S3 or HTTP origins.

**Small code example / visual:**

``` text
User -> CloudFront edge -> origin (S3/API)
        cache hit: edge response
        miss: fetch origin
```

### 190 - IAM? ★★★

**TL;DR:** AWS identity/authorization. Apply least privilege: each
user/service gets only permissions needed, preferably via roles and
temporary credentials.

**Small code example / visual:**

``` json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject"],
  "Resource": "arn:aws:s3:::bucket/public/*"
}
```

### 191 - Secrets AWS? ★★★

**TL;DR:** Secrets Manager or SSM Parameter Store as appropriate;
workloads access them using IAM roles. Never bake credentials into
source/images.

**Small code example / visual:**

``` text
Route53 -> CloudFront/ALB -> ECS/Fargate -> RDS
                         |              |
                         S3          CloudWatch
IAM + VPC + Secrets Manager
```

### 192 - Deploy NestJS on AWS? ★★★

**TL;DR:** Containerize → ECR → ECS/Fargate (one sensible option) →
Application Load Balancer → RDS/Redis as needed → Secrets Manager →
CloudWatch → CI/CD.

**Detailed:** Lambda or EC2 could also be correct depending workload.
Explain why rather than claiming one universal architecture.

**Small code example / visual:**

``` text
Route53 -> CloudFront/ALB -> ECS/Fargate -> RDS
                         |              |
                         S3          CloudWatch
IAM + VPC + Secrets Manager
```

### 193 - Highly available deployment? ★★★

**TL;DR:** Multiple stateless app tasks across availability zones behind
a load balancer, managed HA database, resilient dependencies, health
checks, autoscaling, backups and observability.

**Small code example / visual:**

``` text
             Load Balancer
            /             \
       AZ-A task       AZ-B task
            \             /
             RDS Multi-AZ
```

### 194 - Autoscaling? ★★

**TL;DR:** Automatically adjust capacity based on demand signals such as
CPU, memory, request rate/latency or workload-specific metrics.

**Small code example / visual:**

``` text
Load rises -> tasks 2 -> 4 -> 8
Load falls -> scale back within min/max limits
```

### 195 - Production monitoring? ★★★

**TL;DR:** Golden signals: latency, traffic, errors, saturation---plus
CPU/memory/event-loop, DB pools/query latency, dependency latency,
business metrics, logs/traces, and actionable alerts.

------------------------------------------------------------------------

**Small code example / visual:**

``` text
Latency | Traffic | Errors | Saturation
+ CPU/memory/event-loop + DB + dependencies
+ structured logs + traces + business metrics
```

## OOP / Architecture

### 196 - SOLID? ★★★

**TL;DR:** SRP one reason to change; OCP extend without repeatedly
modifying stable code; LSP subtypes preserve expected behavior; ISP
small focused interfaces; DIP depend on abstractions rather than
concrete low-level details.

**Detailed:** Treat SOLID as design guidance, not laws. Over-abstraction
can be worse than simple code.

**Small code example / visual:**

``` ts
interface PaymentGateway { charge(amount: number): Promise<void> }
class CheckoutService {
  constructor(private gateway: PaymentGateway) {} // DIP
}
```

### 197 - Composition vs inheritance? ★★★

**TL;DR:** Prefer composition for flexible behavior reuse and lower
coupling; use inheritance when there is a genuine stable "is-a"
relationship and substitutability.

**Small code example / visual:**

``` tsx
function Card({ children }) {
  return <section>{children}</section>;
}
<Card><UserProfile /></Card>
```

### 198 - Dependency inversion? ★★★

**TL;DR:** High-level business policy should not depend directly on
low-level infrastructure details; both can depend on stable
abstractions/contracts.

**Small code example / visual:**

``` http
GET /v1/orders/42
GET /v2/orders/42
# Prefer backward compatibility before introducing a new version.
```

### 199 - Repository pattern? ★★

**TL;DR:** Encapsulates persistence/query access behind a
domain/application-facing interface. Useful when it creates a meaningful
boundary; redundant wrappers around an ORM add little value.

**Small code example / visual:**

``` ts
interface OrderRepository {
  findById(id: string): Promise<Order|null>;
  save(order: Order): Promise<void>;
}
```

### 200 - Strategy pattern? ★★

**TL;DR:** Encapsulates interchangeable algorithms/behaviors behind one
contract---e.g. multiple pricing/payment strategies.

**Small code example / visual:**

``` ts
interface DiscountStrategy {
  discount(total: number): number;
}
class Checkout { constructor(private strategy: DiscountStrategy) {} }
```

### 201 - Factory pattern? ★★

**TL;DR:** Centralizes object creation when selecting/configuring
concrete implementations is non-trivial.

**Small code example / visual:**

``` ts
function createGateway(type: "stripe"|"mock"): PaymentGateway {
  return type === "stripe" ? new StripeGateway() : new MockGateway();
}
```

### 202 - Observer pattern? ★★

**TL;DR:** Subscribers react to changes/events from a publisher without
the publisher directly knowing each consumer. JS event emitters are a
familiar example.

**Small code example / visual:**

``` js
emitter.on("order.created", order => analytics.track(order));
emitter.emit("order.created", order);
```

### 203 - Separation of concerns? ★★★

**TL;DR:** Keep responsibilities/boundaries distinct so changes in one
concern don't unnecessarily affect others.

**Small code example / visual:**

``` text
Controller -> HTTP
Service -> business/use case
Repository -> persistence
Gateway -> external provider
```

### 204 - Monolith vs microservices? ★★★

**TL;DR:** Start with the simplest architecture that satisfies
requirements. Modular monoliths reduce operational complexity;
microservices buy independent deployment/scaling/ownership at
significant distributed-system cost.

**Small code example / visual:**

``` text
One team + one domain + same scaling needs -> modular monolith
Independent ownership/scaling boundary emerges -> consider extraction
```

### 205 - Technical debt? ★★★

**TL;DR:** Future engineering cost created by current
design/implementation choices. Some debt is rational if consciously
accepted, visible, and managed.

**Small code example / visual:**

``` text
Shortcut: same validation copied into 4 places
Future cost: rule change touches 4 paths
Track debt and repay based on impact/risk.
```

### 206 - Quality vs speed? ★★★

**TL;DR:** Protect non-negotiables---correctness/security/data
integrity---then consciously trade scope or sophistication for time.
Ship the simplest maintainable solution and record intentional debt.

**Small code example / visual:**

``` text
Correctness/security/data integrity = non-negotiable
Deadline -> reduce scope/complexity, not safety
Ship -> observe -> improve
```

### 207 - Legacy refactor? ★★★

**TL;DR:** Understand/measure behavior, add characterization tests
around risky paths, identify boundaries, refactor incrementally,
preserve compatibility, deploy/observe in small steps.

------------------------------------------------------------------------

**Small code example / visual:**

``` text
Characterization tests -> extract one boundary -> deploy/observe -> repeat
Avoid a giant blind rewrite.
```

## AI-Native / Claude

### 208 - How do you use AI? ★★★

**TL;DR:** I use AI aggressively to increase throughput---understanding
unfamiliar code, planning, first implementations, tests, refactoring and
repetitive work---but I retain responsibility for architecture,
correctness and security and verify generated changes through
review/tests/tooling.

**Detailed:** Good answer emphasizes supervision rather than "vibe
coding." Give the agent clear context/constraints, ask it to plan, make
bounded changes, inspect diffs, run tests/static checks, and validate
assumptions. High-risk code receives stronger human review.

**Small code example / visual:**

``` text
Task -> AI gets context/constraints -> plan -> bounded change
     -> inspect diff -> tests/lint/typecheck -> human approval
```

### 209 - AI agent? ★★★

**TL;DR:** A model-driven system that can reason about a goal, choose
actions/tools, observe results and iterate rather than only producing
one response.

**Small code example / visual:**

``` text
Goal -> Model chooses action -> Tool -> Observation
 ^                                  |
 +------------- iterate ------------+
```

### 210 - Agent vs deterministic workflow? ★★★

**TL;DR:** Use deterministic code/workflows when steps/rules are known
and reliability matters; use agentic behavior where decisions require
flexible interpretation/planning. Combine them rather than making
everything autonomous.

**Small code example / visual:**

``` text
Known exact rule -> deterministic code
Ambiguous planning -> agent may help
Risky action -> checks + human approval
```

### 211 - Agentic loop? ★★★

**TL;DR:** Understand goal/context → decide next action → use tool →
observe result → update plan → repeat until completion/stop condition.

**Small code example / visual:**

``` text
Understand -> Plan -> Act -> Observe -> Verify
    ^                                  |
    +------------- repeat -------------+
```

### 212 - Context engineering? ★★★

**TL;DR:** Supplying the model the right instructions, repository
information, tool results and relevant state at the right time while
avoiding irrelevant context.

**Small code example / visual:**

``` tsx
<ThemeContext.Provider value={theme}>
  <App />
</ThemeContext.Provider>
```

### 213 - MCP? ★★★

**TL;DR:** Model Context Protocol is an open protocol for connecting AI
applications to external tools and data through standardized
servers/interfaces.

**Detailed:** Conceptually, instead of every AI client implementing
bespoke integrations for GitHub, databases, design tools, etc., MCP
provides a common integration model. Treat external MCP servers as
security boundaries and grant minimal permissions.

**Small code example / visual:**

``` text
AI client -> MCP -> GitHub
                -> Database
                -> Internal tools
Grant minimum required permissions.
```

### 214 - CLAUDE.md? ★★★

**TL;DR:** Persistent repository/project instructions for Claude
Code---architecture, conventions, commands, workflow expectations and
project-specific guidance.

**Small code example / visual:**

``` md
# CLAUDE.md
- Architecture: feature-based NestJS modules
- Run tests: npm test
- Validate all HTTP input
- Never edit generated files
```

### 215 - Skills? ★★

**TL;DR:** Reusable packaged task-specific instructions/knowledge that
Claude can apply for particular workflows without stuffing everything
into permanent project context.

**Small code example / visual:**

``` md
# Reusable API skill
1. inspect neighboring endpoint
2. add DTO validation
3. implement service logic
4. add tests
5. run lint/typecheck/tests
```

### 216 - Subagents? ★★

**TL;DR:** Specialized delegated agents with their own context/tool
scope that work on bounded tasks and report results back.

**Small code example / visual:**

``` text
Main agent
├─ test-review specialist
├─ security-review specialist
└─ docs specialist
Each gets a bounded task/context.
```

### 217 - Hooks? ★★

**TL;DR:** Deterministic commands/actions triggered at specific agent
lifecycle events, useful for formatting, validation, policy enforcement
or automation.

**Small code example / visual:**

``` bash
# deterministic post-change checks
npm run format
npm run lint
npm test
```

### 218 - Human-in-the-loop? ★★★

**TL;DR:** Require human review/approval at important decision or action
boundaries rather than granting unrestricted autonomy.

**Small code example / visual:**

``` text
AI proposes destructive migration -> approval boundary
Human reviews impact -> approve/reject -> only then execute
```

### 219 - Review AI code? ★★★

**TL;DR:** Treat it like untrusted code from a very fast contributor:
inspect diff, understand logic, check requirements/edge cases/security,
run tests/typecheck/lint, and verify behavior.

**Small code example / visual:**

``` bash
git diff
npm run typecheck
npm test
npm run lint
# plus human requirements/security/edge-case review
```

### 220 - Where not trust blindly? ★★★

**TL;DR:** Security/auth, cryptography, financial/data-integrity logic,
destructive migrations/commands, unfamiliar dependencies, concurrency,
and architecture decisions deserve especially strong verification.

**Small code example / visual:**
```text
AI-generated change touches:
- authentication
- payment amount calculation
- destructive DB migration
- concurrency/locking

=> require stronger review, tests, security/data-integrity checks, and human approval.
```

### 221 - AI-friendly repository? ★★★

**TL;DR:** Clear architecture/docs, predictable commands, strong
types/contracts, fast deterministic tests, lint/typecheck, small
modules, good naming, explicit conventions, and machine-readable project
instructions.

**Small code example / visual:**

``` text
README + architecture docs + AI instructions
Predictable scripts + strong TS contracts
Fast tests/lint/typecheck + small cohesive modules
```

### 222 - Guardrails? ★★

**TL;DR:** Controls that constrain or validate model behavior:
permissions, schema validation, allow/deny rules, deterministic checks,
tests, hooks, approval steps, sandboxing.

**Small code example / visual:**

``` ts
@UseGuards(AuthGuard, PermissionsGuard)
@Permissions("orders:write")
@Post()
create() {}
```

### 223 - Evaluate AI workflow? ★★★

**TL;DR:** Don't judge by demos. Define representative tasks/evals and
measure correctness, regression rate, latency, cost, security failures,
human review burden and productivity.

**Small code example / visual:**

``` text
Representative tasks -> measure correctness, regressions,
review time, latency, cost, security failures
Compare against baseline.
```

### 224 - Model changes in six months? ★★★

**TL;DR:** Tool-specific commands may age, but durable skills remain:
context, planning, tool use, delegation, verification, permissions,
deterministic guardrails and human ownership.

------------------------------------------------------------------------

**Small code example / visual:**
```text
Today: Claude Code
Tomorrow: another model/tool

Durable workflow stays:
context -> plan -> tools -> bounded changes -> verify -> guardrails -> human ownership
```

## Senior / Product Engineering

### 225 - Unfamiliar problem? ★★★

**TL;DR:** Clarify desired outcome/constraints → inspect existing
system/data → identify unknowns/risks → research/prototype smallest
uncertain part → choose approach → implement incrementally →
validate/measure.

**Small code example / visual:**

``` text
Goal -> constraints -> inspect system -> unknowns/risks
 -> smallest prototype -> implement -> validate/measure -> iterate
```

### 226 - Technical decision? ★★★

**TL;DR:** Problem → constraints → alternatives → decision → trade-offs
→ validation/outcome. Optimize for product requirements rather than
favorite technology.

**Small code example / visual:**

``` text
Problem -> constraints -> alternatives -> trade-offs
 -> simplest justified decision -> measure outcome
```

### 227 - Disagreement? ★★★

**TL;DR:** Align on the shared goal, understand the other reasoning,
compare options using evidence/constraints, prototype/measure if useful,
disagree respectfully, and commit once a decision is made.

**Small code example / visual:**

``` text
Shared goal -> understand both views -> evidence/trade-offs
 -> prototype/measure if useful -> decide -> commit
```

### 228 - Ownership? ★★★

**TL;DR:** Responsibility doesn't end when code is merged: understand
the product problem, surface risks, coordinate dependencies, ensure
quality/deployment/observability, and follow outcomes in production.

**Small code example / visual:**

``` text
Requirement -> code -> tests -> deploy -> monitor production outcome
Ownership does not stop at merge.
```

### 229 - Production incident? ★★★

**TL;DR:** Stabilize service first → communicate → gather evidence →
mitigate/rollback → diagnose root cause → verify recovery → blameless
follow-up with concrete prevention.

**Small code example / visual:**

``` text
Alert -> stabilize/rollback -> communicate -> diagnose
 -> verify recovery -> root cause -> prevention
```

### 230 - Improve without being asked? ★★★

**TL;DR:** Identify recurring friction/risk, quantify impact, propose
the smallest valuable improvement, align with team priorities, implement
it, and show the result.

**Small code example / visual:**

``` text
Recurring friction -> quantify impact -> small proposal
 -> align -> implement -> measure improvement
```

### 231 - PR review? ★★★

**TL;DR:** Check correctness, requirements, security/data integrity,
architecture, tests, readability/maintainability and operational impact.
Separate blockers from suggestions and explain why.

**Small code example / visual:**
```text
PR review priority:
1. correctness / requirement
2. security + data integrity
3. architecture / maintainability
4. tests
5. readability

"Blocker: race condition" is different from "Suggestion: rename variable".
```

### 232 - Maintainable code? ★★★

**TL;DR:** Clear intent, cohesive responsibilities, appropriate
abstractions, explicit contracts, tests around behavior, predictable
errors, minimal hidden coupling, and documentation where "why" isn't
obvious.

**Small code example / visual:**

``` ts
function calculateTotal(order: Order): number {
  return order.items.reduce((sum, i) => sum + i.price * i.qty, 0);
}
```

### 233 - Refactor or ship? ★★★

**TL;DR:** Assess whether existing design prevents safe delivery. Fix
blockers/risky debt now; defer cosmetic/low-impact improvements
explicitly. Avoid both reckless shipping and gold-plating.

**Small code example / visual:**

``` text
Threatens correctness/security/delivery? -> fix enough now
Otherwise -> ship maintainably + record intentional follow-up
```

### 234 - Communicate trade-offs? ★★★

**TL;DR:** Translate technology into outcomes: cost, time, reliability,
security, user impact and future flexibility. Present options and
recommendation without unnecessary jargon.

**Small code example / visual:**
```text
Engineer-speak:
"We should add Redis."

Product-oriented explanation:
"Repeated DB reads are driving p95 latency. A cache may reduce that,
but adds staleness/operational complexity. I would measure the DB bottleneck first."
```

### 235 - New codebase? ★★★

**TL;DR:** Get it running → understand product/user flows → trace one
request end-to-end → read architecture/tests/config/deployment → make a
small change → ask targeted questions → expand understanding
iteratively.

**Small code example / visual:**

``` text
Run app/tests -> understand user flow -> trace one request UI->API->DB
 -> read architecture/deploy docs -> make one small safe change
```

### 236 - High quality? ★★★

**TL;DR:** Code that solves the correct product problem reliably,
securely and maintainably---not merely elegant code. Quality includes
tests, observability, performance where required, operability and clear
trade-offs.

------------------------------------------------------------------------

**Small code example / visual:**

``` text
Correctness/security/data integrity = non-negotiable
Deadline -> reduce scope/complexity, not safety
Ship -> observe -> improve
```

------------------------------------------------------------------------

# HOW TO STUDY THIS VERSION

For every question:

1.  Read the **TL;DR** first.
2.  Look at the **small code example / visual** and explain what it
    demonstrates.
3.  Only then read the detailed answer if you need more depth.
4.  For ★★★ questions, be ready for a follow-up: **why, when, trade-off,
    failure case, or "what would you change?"**
5.  For snippets with output, cover the comments/output and predict it
    before checking.

# LAST-MINUTE REVIEW

If you only have 15 minutes, prioritize: event loop/microtasks;
closures/references; TypeScript narrowing/generics/unknown/keyof; Node
concurrency/libuv/blocking; NestJS lifecycle/DI/DTO/auth; REST
idempotency/errors/pagination; DB indexes/query
plans/transactions/races; React effects/state/server state;
Docker/CI/AWS deployment; and the senior answer structure **problem →
constraints → alternatives → decision → trade-offs → outcome**.
