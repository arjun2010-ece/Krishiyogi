## Asked in atleeast 2 interviews

Absolutely — these are very relevant for a Senior Frontend interview, especially because they test whether you understand the full delivery lifecycle, not just React.

### 1. How do you deploy in your team?

A strong senior-level answer is:

> In my team, deployment is usually automated through CI/CD. Once a PR is merged, the pipeline runs linting, type checks, unit tests, integration tests, and creates a production build.
>
> The application is then packaged, often as a Docker image, pushed to a container registry, and deployed to the target environment. If Kubernetes is used, Kubernetes pulls that image and runs it inside Pods.
>
> We normally deploy progressively across environments such as development, staging and production, and after deployment we monitor logs, errors and application health. If something goes wrong, we either roll back to the previous image/version or redeploy a known stable build.

A simple flow to remember:

```text
Developer pushes code
        ↓
Pull Request
        ↓
CI pipeline
        ↓
Lint + Typecheck + Tests
        ↓
Build application
        ↓
Build Docker image
        ↓
Push image to registry
        ↓
Deploy to Kubernetes
        ↓
Pods run application
        ↓
Monitoring / rollback
```

If they ask specifically about frontend, you can add:

> For a purely static frontend, another approach is to build the assets and deploy them directly to object storage/CDN, for example S3 + CloudFront, without running the frontend itself in Kubernetes.

That distinction is useful.

---

### 2. Difference between Docker image and Docker container?

Very common interview question.

**Docker image = blueprint/template.**

**Docker container = running instance of that image.**

For example:

```text
Dockerfile
   ↓
docker build
   ↓
Docker Image
   ↓
docker run
   ↓
Docker Container
```

You can say:

> A Docker image is an immutable packaged artifact containing the application, runtime, libraries and dependencies required to run it.
>
> A container is a running instance of that image.

A good analogy:

```text
Image     = class
Container = object/instance
```

Example:

```bash
docker build -t my-app .
```

creates:

```text
my-app image
```

Then:

```bash
docker run my-app
```

creates a running container.

And you can run multiple containers from the same image:

```text
my-app image
     ↓
 ┌───────────┐
 │Container 1│
 │Container 2│
 │Container 3│
 └───────────┘
```

---

### 3. How do Kubernetes and Pods work in deployment? Do we need Docker?

The clean interview answer:

> Kubernetes is a container orchestration platform. It doesn't normally build our application; it manages how containerized applications run in a cluster.
>
> We first create a container image, usually with Docker or another OCI-compatible tool, and push it to a registry. Kubernetes then pulls that image and runs it inside Pods.

Flow:

```text
Application
    ↓
Dockerfile
    ↓
Docker image
    ↓
Container Registry
    ↓
Kubernetes Deployment
    ↓
Pods
    ↓
Containers
```

Important distinction:

```text
Kubernetes
    ↓
Deployment
    ↓
ReplicaSets
    ↓
Pods
    ↓
Containers
```

A **Pod** is the smallest deployable unit in Kubernetes.

Usually:

```text
1 Pod
  ↓
1 application container
```

But a Pod can contain multiple tightly coupled containers.

For example:

```text
Pod
├── application container
└── sidecar container
```

If they ask:

**"Can Kubernetes work without Docker?"**

Answer:

> Yes. Kubernetes does not require Docker specifically. Kubernetes needs a container runtime compatible with the Container Runtime Interface, such as containerd or CRI-O.
>
> Docker is commonly used to build container images, but Kubernetes clusters today commonly run those images using containerd rather than the Docker Engine.

So don't say:

> Kubernetes runs Docker containers.

A better wording is:

> Kubernetes runs OCI-compatible containers.

---

### 4. Is `npm ci` used to install from package-lock.json?

Yes.

A concise answer:

> `npm ci` performs a clean and deterministic installation using `package-lock.json`. It is particularly suited to CI/CD environments because it installs exactly the dependency versions recorded in the lock file.

Key distinction:

```text
npm install
```

can update `package-lock.json`.

Whereas:

```text
npm ci
```

expects the lock file to already match `package.json`.

It also removes an existing `node_modules` before installation.

So:

```text
npm install
→ normal local development
→ may update package-lock.json
```

```text
npm ci
→ CI/CD
→ clean install
→ exact versions from package-lock.json
→ doesn't rewrite package-lock.json
```

Strong interview sentence:

> I generally use `npm ci` in CI pipelines because reproducibility matters — the build server should install exactly the same dependency tree that was committed.

---

# 5. How do you unit-test a JavaScript function that calls another function?

Suppose you have:

```javascript
export function calculateTotal(price, quantity) {
  return price * quantity;
}

export function checkout(price, quantity) {
  const total = calculateTotal(price, quantity);

  return total + 10;
}
```

There are actually **two things you might test**.

First, you can test the final behavior:

```javascript
test("calculates checkout total", () => {
  expect(checkout(100, 2)).toBe(210);
});
```

This is usually preferable because you're testing behavior rather than implementation details.

But they may ask specifically:

> How do you test that `calculateTotal()` was called?

Then you'd use a mock or spy.

Usually it is better if the dependency is in another module.

```javascript
// calculator.js

export function calculateTotal(price, quantity) {
  return price * quantity;
}
```

```javascript
// checkout.js

import { calculateTotal } from "./calculator";

export function checkout(price, quantity) {
  const total = calculateTotal(price, quantity);

  return total + 10;
}
```

Then with Jest:

```javascript
import * as calculator from "./calculator";
import { checkout } from "./checkout";

test("calls calculateTotal", () => {
  const spy = jest.spyOn(calculator, "calculateTotal");

  checkout(100, 2);

  expect(spy).toHaveBeenCalledWith(100, 2);

  spy.mockRestore();
});
```

However, a senior answer should include:

> I wouldn't automatically assert every internal function call. If the internal function is only an implementation detail, testing the observable result makes the test less brittle. I use mocks or spies when interaction with the dependency itself matters.

Excellent answer.

---

# 6. Playwright vs Cypress — at least two differences

You can easily give 4–5.

### Difference 1: Architecture

Cypress historically runs much of its test logic in or alongside the browser environment.

Playwright drives browsers externally using browser automation protocols.

From an interview perspective:

> Playwright generally gives you lower-level, more direct control over multiple browser contexts, tabs and browser instances.

---

### Difference 2: Multi-tab / multi-page support

Playwright has very strong built-in support for:

```text
multiple tabs
multiple windows
multiple browser contexts
multiple users
```

Example:

```javascript
const page1 = await context.newPage();
const page2 = await context.newPage();
```

Historically, Cypress's model made true multi-tab workflows less natural, though modern Cypress has improved cross-origin and multi-window scenarios.

For an interview:

> Playwright is generally more natural for complex multi-page or multi-user flows.

---

### Difference 3: Browser support

Playwright directly supports:

```text
Chromium
Firefox
WebKit
```

WebKit is particularly useful because it gives better Safari-engine coverage.

Cypress supports major browsers too, but Playwright's first-class WebKit support is a common reason teams choose it.

---

### Difference 4: Parallelism

Playwright has built-in parallel execution through workers.

```text
worker 1 → tests
worker 2 → tests
worker 3 → tests
```

Cypress also supports parallelization, especially through CI/cloud tooling, but Playwright's runner has strong local parallelization built in.

---

### Difference 5: Developer experience

Cypress traditionally has an excellent interactive test runner and debugging UI.

Playwright has:

```text
Trace Viewer
UI mode
screenshots
videos
network tracing
DOM snapshots
```

So a balanced answer:

> Cypress has historically been very developer-friendly for interactive debugging, while Playwright gives particularly strong browser automation, parallel execution, multiple contexts and cross-browser support.

Don't say:

> Playwright is better than Cypress.

Say:

> Which one I choose depends on the application's testing requirements.

---

# 7. Mock vs Spy in unit testing

This is a very common question.

The easiest distinction:

> A mock replaces behavior.
>
> A spy observes behavior.

There is some overlap because spies can also replace implementations, but that's the clean conceptual distinction.

---

## Mock example

Imagine:

```javascript
export async function getUser() {
  return fetch("/api/user").then(res => res.json());
}
```

Your component/function shouldn't make a real HTTP request during a unit test.

So you mock it:

```javascript
jest.mock("./api", () => ({
  getUser: jest.fn(),
}));
```

Then:

```javascript
getUser.mockResolvedValue({
  id: 1,
  name: "Arjun",
});
```

You've replaced the real function.

Conceptually:

```text
Real getUser()
      ↓
   removed
      ↓
Mock implementation
```

---

## Spy example

Imagine:

```javascript
const userService = {
  saveUser(user) {
    // real implementation
  },
};
```

Then:

```javascript
const spy = jest.spyOn(userService, "saveUser");

userService.saveUser({
  name: "Arjun",
});

expect(spy).toHaveBeenCalledWith({
  name: "Arjun",
});
```

By default, `jest.spyOn()` can still call the original implementation.

You're observing:

```text
saveUser()
   ↓
Spy watches call
   ↓
Original implementation still runs
```

Then clean it up:

```javascript
spy.mockRestore();
```

---

## But a spy can also mock

This is the interview nuance they may want.

You can do:

```javascript
jest
  .spyOn(userService, "saveUser")
  .mockReturnValue(true);
```

Now the spy is both:

```text
observing
+
replacing behavior
```

So the technically precise answer is:

> A mock is a general test double where we replace a dependency with controlled behavior. A spy wraps or observes an existing function so we can verify things like whether it was called, how many times it was called and which arguments it received. A spy can optionally replace the original implementation as well.

---

# A very likely follow-up: stub vs mock vs spy

Since they asked mock and spy, memorize this too.

```text
Stub
→ provides predefined output

Mock
→ replaces a dependency and can verify interactions

Spy
→ observes an existing function's calls
```

Example stub:

```javascript
getUser.mockResolvedValue({
  id: 1,
});
```

You're primarily saying:

> Whenever this dependency is called, return this value.

Spy:

```javascript
expect(spy).toHaveBeenCalledTimes(1);
```

You're interested in how the dependency was used.

---

## The 30-second versions to memorize

For the interview, these answers are enough:

**Docker image vs container**

> An image is an immutable packaged blueprint containing the application and its dependencies. A container is a running instance of that image, and multiple containers can run from the same image.

**Kubernetes**

> Kubernetes orchestrates containers. We build an OCI image, push it to a registry, and Kubernetes Deployments create and manage Pods that run containers from that image. Kubernetes doesn't require Docker specifically; runtimes such as containerd are commonly used.

**npm ci**

> `npm ci` performs a clean deterministic installation using `package-lock.json`, which makes it ideal for CI/CD pipelines.

**Mock vs spy**

> A mock replaces a dependency with controlled behavior. A spy observes an existing function so we can verify calls and arguments, although a spy can optionally replace its implementation too.

**Cypress vs Playwright**

> Both support E2E testing. Playwright has particularly strong multi-browser, multi-tab, browser-context and parallel testing capabilities, while Cypress is well known for its interactive developer experience and debugging workflow.

And for **"How do you deploy?"**, remember this chain:

```text
Code
 ↓
PR
 ↓
CI
 ↓
lint + typecheck + tests
 ↓
npm ci
 ↓
build
 ↓
Docker image
 ↓
registry
 ↓
Kubernetes deployment
 ↓
Pods
 ↓
monitoring
```

That gives you a very connected answer if they jump between **npm ci → Docker → Kubernetes → Pods → deployment**, which is probably exactly why those questions appeared together.


---

## Question about event loop asked :

```javascript
console.log('a');   // synchronous
console.log('b');   // synchronous

setTimeout(() => console.log('c'), 200);

setTimeout(() => console.log(d), 0);

Promise.resolve().then(() => console.log('f'));

var d = 20;
var f = 40;

console.log('e');
```

The output will be:

```text
a
b
e
20
f
c
```



Here’s the execution flow.

JavaScript first runs all synchronous code on the call stack:

```text
console.log('a') → a
console.log('b') → b
```

The two `setTimeout` callbacks are registered with the browser/runtime. They do **not** execute immediately, even the one with `0ms`.

Then:

```javascript
Promise.resolve().then(() => console.log('f'));
```

registers a Promise callback in the **microtask queue**.

Then:

```javascript
var d = 20;
var f = 40;
console.log('e');
```

execute synchronously, so we get:

```text
e
```

At this point synchronous execution is finished.

The queues conceptually look like:

```text
Microtask queue
----------------
() => console.log('f')


Macrotask / Task queue
----------------------
() => console.log(d)     // 0 ms

later:
() => console.log('c')   // 200 ms
```

The important event-loop rule is:

```text
Synchronous code
      ↓
Microtasks
      ↓
Next macrotask
```

So the Promise runs before the `setTimeout(..., 0)`:

```text
f
```

Then the zero-delay timer executes:

```javascript
console.log(d);
```

At this point:

```javascript
d = 20;
```

so:

```text
20
```

Finally, approximately 200ms later:

```text
c
```

Therefore:

```text
a
b
e
f
20
c
```

One correction to the sequence I wrote at the top: **`f` comes before `20`**, because Promise callbacks are microtasks and are processed before timer callbacks.

So the correct final answer is:

```text
a
b
e
f
20
c
```

### Critical interview follow-up: what about `var d`?

They may try to trick you with:

```javascript
setTimeout(() => console.log(d), 0);

var d = 20;
```

The callback does **not** execute when `setTimeout` is encountered. It executes later, after the synchronous code has completed.

By then:

```javascript
d = 20;
```

Therefore it prints:

```text
20
```

Even though `var d` is hoisted conceptually as:

```javascript
var d; // undefined

setTimeout(() => console.log(d), 0);

d = 20;
```

the callback reads `d` **when the callback actually executes**, not when it is registered.

Also note that:

```javascript
var f = 40;
```

has no effect on:

```javascript
Promise.resolve().then(() => console.log('f'));
```

because `'f'` is a **string literal**, not the variable `f`.

If it were instead:

```javascript
Promise.resolve().then(() => console.log(f));
```

then the output at that position would be:

```text
40
```

This is exactly the kind of question where Critical TechWorks is testing **event loop + microtasks/macrotasks + closures + hoisting** together.

