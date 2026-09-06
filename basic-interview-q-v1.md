For a backend role asking for 8 years of experience, interviewers will expect more than Node.js syntax. You should demonstrate production experience in API design, databases, security, concurrency, distributed systems, testing, deployment, observability, and technical decision-making.

Since your strongest background is frontend/full-stack, answers should be honest: connect them to your real NestJS, MongoDB, Redis, authentication, Docker, Kubernetes, AWS, and fintech/Web3 experience without claiming eight years exclusively in backend.

# Part 1 — Basic Node.js questions

### 1. What is Node.js?

Node.js is a JavaScript runtime built on the V8 engine. It allows JavaScript to run outside the browser and is commonly used to build APIs, real-time applications, background workers, and command-line tools.

Its event-driven, non-blocking I/O model makes it effective for applications handling many concurrent network or database operations.

---

### 2. Is Node.js single-threaded?

JavaScript execution is primarily single-threaded, but Node.js itself is not entirely single-threaded.

* JavaScript runs on the main event-loop thread.
* Some operations are handled by the operating system.
* The libuv thread pool handles operations such as filesystem access, some DNS calls, and cryptography.
* Worker threads can execute CPU-intensive JavaScript in parallel.

A good interview phrase:

> “Node.js uses a single main JavaScript thread, but it achieves concurrency through the event loop, operating-system APIs, a worker pool, and optionally worker threads.”

---

### 2.1: Is Node.js single-threaded? How does it use multi-core systems?

**A:** JavaScript *execution* in Node runs on a single thread — one call stack, one thing running at a time. But Node isn't purely single-threaded under the hood: it uses **libuv**, which maintains a background **thread pool** (default size 4) for operations like file system access, DNS lookups (`dns.lookup`), crypto (`pbkdf2`, `scrypt`), and zlib compression.

To actually use multiple CPU cores, Node offers two separate mechanisms:
- **Cluster module** — spawns multiple **Node processes** (not threads), each with its own event loop and memory space, typically load-balanced across cores.
- **worker_threads** — true multi-threading within a single process, useful for CPU-bound work without spinning up full processes.

---

### 2.2: Does JavaScript have its own event loop? How is it different from Node's event loop?

**A:** This is the key point: **JavaScript the language has no event loop at all** — it's not part of the ECMAScript spec. The JS engine (e.g., V8) only provides a call stack, heap, and execution model. The event loop is implemented by the **host environment** that embeds the engine.

- **Browser event loop**: defined loosely by the WHATWG/HTML spec. Has macrotask queues (setTimeout, UI events) and microtask queues (Promises, MutationObserver), and interleaves rendering/paint steps between tasks.
- **Node event loop**: implemented by **libuv**, structured into distinct **phases** per tick:
  `timers → pending callbacks → idle/prepare → poll (I/O) → check (setImmediate) → close callbacks`
  No rendering concerns, since there's no DOM.

Same underlying concept (pull callbacks off queues once the call stack is empty), but genuinely different implementations and mechanics. Bonus point: in Node, `process.nextTick()` callbacks run *before* Promise microtasks, and both queues are fully drained between each event loop phase — a common source of "guess the output" trick questions.

---

### 2.3: If Node is async, why can it still get blocked?

**A:** The event loop only helps with work that can be *delegated* — I/O, timers, and select operations handled via the libuv thread pool. It does nothing for synchronous, CPU-bound code. If you run a heavy loop, `JSON.parse` on a huge payload, or `fs.readFileSync`, that code executes directly on the main thread and blocks everything — no other callbacks, timers, or I/O events can fire until it finishes.

Async doesn't mean "won't block" — it means the I/O portion is offloaded so the thread isn't idly waiting on it. CPU-bound work still blocks the single JS thread regardless of how "async" your code looks.

**Note:**
- The above `fs.readFileSync` method is using `fs` package which should have been handled by **libuv thread pool** but it is a wrong way of thinking.
- The `fs`/ `crypto` / `dns` / `zlib` module by default is not handed to the **libuv** threadpool but these modules **async, callback-based functions use the thread pool**.
- All of above module has 2 types of methods, sync and async like `fs.readFileSync()`(sync) vs `fs.readFile()` (async). Sync is handled on main thread, while async is on **libuv thread pool**
- Similarly, `zlib.gzip()`(async) vs `zlib.gzipSync()`(sync). Same in case of **crypto** module too.
- **Sync** in the name is your signal that **libuv** is not involved at all but main thread is involved.
---

### 3. Explain the Node.js event loop

The event loop lets Node.js process asynchronous operations without blocking while waiting for them to finish.

Simplified order:

1. Execute synchronous code.
2. Process `process.nextTick()` callbacks.
3. Process Promise microtasks.
4. Continue through event-loop phases such as timers, polling and `setImmediate()`.
5. Repeat while work remains.

```js
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

The Promise callback is a microtask, so it executes before the timer callback.

---

### 4. What is blocking versus non-blocking code?

Blocking code prevents the main thread from processing other requests until the operation finishes.

```js
const data = fs.readFileSync("file.txt");
```

Non-blocking code starts the operation and allows Node.js to continue processing other work:

```js
const data = await fs.promises.readFile("file.txt");
```

`await` pauses the current async function, not the entire Node.js event loop.

---

### 5. When is Node.js a poor choice?

Node.js is less suitable when the main process must perform heavy CPU computations, such as video encoding, image processing, or complex mathematical calculations.

Those tasks can block the event loop. Possible solutions include:

* Worker threads
* Separate worker services
* Job queues
* Specialized services written in another language

---

### 6. What is the difference between CommonJS and ES modules?

- They are two different systems used in JavaScript to **organize code into separate, reusable files**.

CommonJS uses:

```js
const service = require("./service");
module.exports = service;
```

ES modules use:

```js
import service from "./service.js";
export default service;
```

ES modules are the JavaScript standard and support static analysis and top-level `await`. CommonJS remains common in older Node.js projects.

---

### 7. What is middleware?

Middleware is logic executed during the request-response pipeline before the final route handler.

Common uses include:

* Logging
* Authentication
* Correlation IDs
* CORS
* Rate limiting
* Request parsing

Middleware should generally handle cross-cutting HTTP concerns rather than business logic.

---

### 8. How do you handle errors in asynchronous Node.js code?

Use `try/catch` around awaited operations and allow errors to reach centralized error handling.

```ts
async function getUser(id: string) {
  try {
    return await repository.findById(id);
  } catch (error) {
    logger.error({ error, id }, "Failed to retrieve user");
    throw error;
  }
}
```
I do 3 things here:

* **Never swallow errors silently** — an empty ```catch {}``` block (or a ```catch``` that just logs and returns ```undefined```) hides bugs and makes production issues nearly impossible to debug.

* **Convert expected errors, don't hide them** — if ```findById``` fails because the user genuinely doesn't exist, that's an expected case. Convert it into a proper domain/HTTP error (e.g. throw a ```NotFoundException```) instead of leaking a raw database error to the client.

* **Let unexpected errors bubble up** — errors you didn't anticipate (a DB connection drop, a bug) shouldn't be caught-and-hidden at every layer. Let them reach one **centralized error handler** (like a global exception filter) so they're handled consistently everywhere, not differently in every function.

```I avoid swallowing errors. I log useful context, convert expected errors into domain or HTTP errors, and let unexpected errors reach global exception handling.```

---

### 9. What are streams?

Streams process data incrementally instead of loading the complete data into memory.

```ts
createReadStream("large-file.csv").pipe(response);
```

They are useful for:

* Large files
* Uploads and downloads
* Data transformation
* Compression
* Network communication

Streams provide memory efficiency and support backpressure.

---

### 10. What is backpressure?

Backpressure occurs when data is produced faster than the consumer can process it.

Node.js streams control this by pausing the producer when the consumer’s internal buffer becomes full. Using `pipe()` or `pipeline()` normally manages this automatically.

Without backpressure, memory usage can continuously grow.

# Part 2 — NestJS fundamentals

### 11. Why use NestJS instead of plain Express?

**Simple answer:** Express gives you a blank canvas. NestJS gives you a **canvas with a frame** already built — so every developer on the team builds things the same way.
(NestJS provides a structured application architecture on top of Express or Fastify.)

What it gives you out of the box:

* Modules and dependency injection (a system that hands your classes their dependencies automatically)
* Controllers (handle requests) and providers (handle logic)
* Guards, pipes, interceptors and filters (built-in checkpoints for security, validation, and error handling)
* Built-in testing tools
* Support for WebSockets and microservice integrations

```One-line memory hook: "Express = freedom. NestJS = structure." Pick NestJS when the app will grow and multiple people will touch the code.```

---

### 12. Explain modules, controllers and providers

* **Module:**  A module bundles together everything needed to handle **one feature or one area of your app**. it includes:
  	* The controller(s) for that feature (handle the requests)
  	* The provider(s)/service(s) for that feature (do the logic)
  	* The repository for that feature (talks to the DB)
  	* Sometimes DTOs, entities, or other supporting classes for that feature
* **Controller:** Takes incoming requests and returns responses.
* **Provider:** Contains real business logic.
* **Repository:** Talks to the database

```ts
@Module({
  controllers: [UsersController],
  providers: [UsersService, UsersRepository],
  exports: [UsersService],
})
export class UsersModule {}
```

Concrete example:

If your app is an e-commerce site, you'd likely have:

```
UsersModule    → UsersController, UsersService, UsersRepository, User entity
OrdersModule   → OrdersController, OrdersService, OrdersRepository, Order entity
ProductsModule → ProductsController, ProductsService, ProductsRepository, Product entity

```

We use modules in general to organise the code better in a single place instead of scattering it throughout the codebase.

I keep controllers thin and place business rules in services or domain-level components.

---

### 13. How does dependency injection work in NestJS?

Simple answer: Instead of a class creating its own tools, NestJS hands it the tools it needs — like a chef who doesn't buy their own ingredients, because the kitchen manager delivers them.

Here, ```UsersService``` doesn't create ```UsersRepository``` itself. NestJS's container ("the kitchen manager") creates it and hands it over.


```ts
@Injectable()
export class UsersService {
  constructor(
    private readonly usersRepository: UsersRepository,
  ) {}
}
```

Why this matters (in plain terms):

- Less coupling — classes don't need to know how to build their dependencies, just what they need.
- Easier testing — in tests, you can hand a class a fake dependency (mock) instead of the real one (like swapping a real oven for a toy oven during a cooking class demo).
- Centralized control — one place (the container) manages how objects are created.

---

### 14. What is a DTO?

A DTO defines the expected shape of data crossing an application boundary.

Simple answer: A DTO (Data Transfer Object) is a form template — it says exactly what data is allowed to come in (or go out) of API endpoint, and nothing else.

Think of it like a job application form: it only has fields for name, email, and experience — you can't scribble in random extra info and have it accepted.

Please remember: A DTO is not your database table.

```ts
export class CreateUserDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(8)
  password: string;
}
```

---

### 15. What is a pipe?

A pipe validates or transforms input before it reaches a controller method.

Simple answer: A pipe is a security checkpoint at the airport — it checks your bag (the incoming data) before you're allowed through, and can also repack it into the right shape.

```ts
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
    transform: true,
  }),
);
```

What this specific setup does, in plain terms:

* whitelist: true → throws away any fields that aren't in the DTO ("you can't bring that in your bag")
* forbidNonWhitelisted: true → instead of silently dropping extra fields, it rejects the request entirely
* transform: true → automatically converts data into the right type (e.g. a string "5" becomes the number 5)

Memory hook: Pipes clean and check the data before it reaches your controller.

---

### 16. What is a guard?

A guard decides whether a request may access a route. It is a checkpoint on a route.
We have other checkpoints also on different parts of code like ***pipes, interceptors and filters***.

```ts
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles("admin")
@Get()
findAll() {}
```

examples:
* Authentication guards
* Authorization guards

Authentication guards verify identity. Authorization guards check whether that identity has permission to perform the operation.

---

### 17. What is an interceptor?

An interceptor is a **checkpoint** that wraps around the **controller's handler** — it can run code before the handler executes and again after it returns, and it can change what goes in or what comes out.

```Request → Interceptor (before) → Controller handler → Interceptor (after) → Response ```

Because it sits on both sides of the handler, it's used for:

* Reshaping the response before it's sent back (e.g. wrapping every response in a consistent { data: ... } structure)
* Measuring execution time — start a timer before, log the duration after
* Caching — return a cached result before the handler even runs, or store the result after
* Logging what came in and what went out
* Timeouts — cut off requests that take too long

How it compares to the other checkpoints:

* Guard → checkpoint on the route: decides if a request may access it at all.
* Pipe → checkpoint on the incoming data: cleans and validates it before the controller sees it.
* Interceptor → checkpoint around the handler itself: runs extra logic before and after it executes, and can reshape the result.


Interceptors are conceptually similar to middleware around method execution, while guards primarily make access decisions.

---

### 18. What is an exception filter?

An exception filter is a checkpoint that catches errors thrown anywhere in the request pipeline — guards, pipes, interceptors, controller, or service — and converts them into a single, consistent response before it reaches the client.

```
Middleware → Guards → Interceptors → Pipes → Controller → Service
                            ↓ (error thrown at any point)
                      Exception Filter → Response

```

Without a filter, an error thrown deep inside a service would either :
 * crash the app or 
 * send the client a raw, unformatted error. 

The filter sits at the end of the pipeline and reshapes any error into a predictable format, for example:

```json
{
  "statusCode": 404,
  "code": "USER_NOT_FOUND",
  "message": "User not found",
  "correlationId": "req-123"
}
```

**How it compares to the other checkpoints:** 

- Guards, pipes, and interceptors all operate on the normal, successful path of a request. 
- An exception filter only activates when something in that path throws an error — it's the single exit point for failures, so every part of the app returns errors in the same shape instead of each controller handling them differently.

---

### 19. Explain the NestJS request lifecycle

A useful simplified order is:

```text
Middleware → Guards → Interceptors (before) → Pipes
→ Controller → Service
→ Interceptors (after) → Exception filters
```

The exact error path depends on where the exception occurs, but this model is sufficient for most interview discussions.

---

### 20. What provider scopes exist in NestJS?

Common provider scopes are:

* **Singleton/default:** One instance is shared across the application.
* **Request:** A new instance is created for every request.
* **Transient:** A separate instance is created for each consumer.

Singleton is usually preferred. Request-scoped providers can add overhead and should be used only when request-specific state genuinely requires them.

# Part 3 — API and application design

### 21. How do you design a REST API?

I focus on:

* Resource-oriented URLs
* Correct HTTP methods and status codes
* Input validation
* Consistent error responses
* Pagination, filtering and sorting
* Idempotency where required
* Versioning and backward compatibility
* Authentication, authorization and rate limiting
* Documentation using OpenAPI

Example:

```text
GET    /v1/orders
GET    /v1/orders/:id
POST   /v1/orders
PATCH  /v1/orders/:id
DELETE /v1/orders/:id
```

---

### 22. PUT versus PATCH?

* `PUT` conventionally replaces the complete resource representation.
* `PATCH` applies a partial update.

Both can be designed idempotently. Sending the same request multiple times should leave the resource in the same final state.

---

### 23. What is idempotency?

An operation is idempotent when repeating it has the same intended effect as executing it once.

For a payment or order endpoint, the client supplies an idempotency key:

```text
Idempotency-Key: checkout-abc-123
```

The server stores the key and result atomically. A repeated request returns the previous result instead of creating a second payment.

---

### 24. How would you implement pagination?

For small or stable datasets, offset pagination is simple:

```text
GET /users?page=3&limit=20
```

For large or frequently changing datasets, cursor pagination is safer:

```text
GET /users?cursor=eyJpZCI6MTIzfQ&limit=20
```

Cursor pagination avoids increasingly expensive offsets and reduces skipped or duplicated records when rows are inserted during navigation.

---

### 25. How do you version an API?

Possible approaches include:

* `/v1/users`
* Header-based versions
* Media-type versions

I introduce a new version only for breaking changes. Additive fields normally do not require a new version. I also define a deprecation period and monitor whether old clients still use the previous version.

---

### 26. How do you structure a large NestJS application?

I prefer feature-based modules:

```text
src/
  orders/
    application/
    domain/
    infrastructure/
    presentation/
    orders.module.ts
  payments/
  users/
  shared/
```

The important principles are:

* Organize around business capabilities.
* Keep controllers thin.
* Prevent database details from leaking everywhere.
* Avoid a large generic `utils` or `common` dumping ground.
* Expose narrow module APIs.

I introduce full domain-driven layering only when the business complexity justifies it.

# Part 4 — Databases

### 27. SQL versus NoSQL?

SQL databases are suitable when relationships, transactions, joins and strong consistency are important.

Document databases are useful when data is naturally aggregate-shaped, the schema changes frequently, or denormalized reads are beneficial.

I choose based on data access patterns and consistency requirements—not merely anticipated traffic.

---

### 28. What is a database index?

An index is an additional data structure that helps the database find records without scanning the entire table or collection.

Indexes improve reads but add:

* Storage cost
* Write overhead
* Maintenance cost

I design indexes using actual query patterns and verify them using tools such as PostgreSQL `EXPLAIN ANALYZE` or MongoDB `explain()`.

---

### 29. What is a composite index?

A composite index contains multiple fields:

```sql
CREATE INDEX idx_orders_customer_created
ON orders(customer_id, created_at DESC);
```

Column order matters. This index is useful for queries filtering by `customer_id` and ordering or filtering by `created_at`. It may not efficiently support queries using only `created_at`.

---

### 30. What is the N+1 query problem?

It happens when the application performs one query for a list and then one additional query for every item.

```text
1 query for orders
100 queries for their customers
```

Solutions include:

* Joins
* Batch queries
* Eager loading
* DataLoader for GraphQL
* Carefully chosen denormalization

---

### 31. What is a transaction?

A transaction groups operations so they succeed or fail as one unit.

```ts
await dataSource.transaction(async manager => {
  await manager.decrement(Account, senderId, "balance", amount);
  await manager.increment(Account, receiverId, "balance", amount);
});
```

Transactions protect database consistency. They do not automatically make external calls—such as sending messages—transactional.

---

### 32. Explain ACID

* **Atomicity:** All transaction operations succeed or all are rolled back.
* **Consistency:** Data remains valid according to defined constraints.
* **Isolation:** Concurrent transactions do not improperly interfere.
* **Durability:** Committed changes survive failures.

---

### 33. Optimistic versus pessimistic locking?

**Optimistic locking** assumes conflicts are rare and detects them using a version number:

```sql
UPDATE products
SET stock = stock - 1, version = version + 1
WHERE id = $1 AND version = $2;
```

If zero rows are updated, another request changed the record first.

**Pessimistic locking** locks the record before modification, such as `SELECT ... FOR UPDATE`.

Optimistic locking improves concurrency. Pessimistic locking is useful when conflicts are frequent and correctness requires serialized access.

---

### 34. How do you prevent race conditions when updating stock?

I do not read stock and later write a calculated value without protection.

Use an atomic conditional update:

```sql
UPDATE products
SET stock = stock - 1
WHERE id = $1 AND stock > 0;
```

Then verify that exactly one row was updated. Depending on the broader workflow, I may also use a transaction, row lock, or optimistic version.

# Part 5 — Authentication and security

### 35. Authentication versus authorization?

* **Authentication:** Who is the user?
* **Authorization:** What is the user allowed to do?

A valid JWT proves identity but does not automatically mean the user may access every resource.

---

### 36. How does JWT authentication work?

1. The user authenticates.
2. The server issues a short-lived access token.
3. The client sends it with later requests.
4. The server validates its signature, issuer, audience and expiry.
5. Authorization rules are applied.

JWT payloads are encoded, not encrypted. Sensitive information should not be placed inside them.

---

### 37. Access token versus refresh token?

* Access tokens are short-lived and used for API access.
* Refresh tokens live longer and obtain new access tokens.

Refresh tokens should be stored securely, rotated after use, and revocable. For browser applications, secure, `HttpOnly`, appropriately configured cookies are often safer than storing long-lived tokens in JavaScript-accessible storage.

---

### 38. How do you store passwords?

Use a password-hashing algorithm such as Argon2 or bcrypt with a suitable work factor and a unique salt.

Never store plain-text passwords or encrypt them reversibly.

Also consider:

* Login throttling
* Account lockout policies
* MFA
* Password reset token expiry
* Preventing user enumeration

---

### 39. How do you secure a NestJS API?

I use layered controls:

* Validate and sanitize input.
* Authenticate and authorize every protected operation.
* Use parameterized queries or a safe ORM.
* Configure CORS explicitly.
* Apply rate limits.
* Set security headers.
* Store secrets outside source control.
* Redact secrets and personal data from logs.
* Enforce request-size limits and timeouts.
* Patch dependencies and scan images.
* Use least-privilege database and cloud credentials.

---

### 40. What is the difference between CORS and CSRF?

**CORS** is a browser policy controlling whether JavaScript from one origin can read responses from another origin.

**CSRF** tricks a browser into sending an authenticated request using automatically attached credentials, usually cookies.

CORS alone is not complete CSRF protection. Cookie-based authentication may require `SameSite` cookies, CSRF tokens and origin validation.

# Part 6 — Caching and Redis

### 41. Why use Redis?

Redis is commonly used for:

* Caching
* Rate limiting
* Sessions
* Distributed coordination
* Short-lived data
* Pub/sub
* Job-queue infrastructure

It is fast, but persistence and consistency requirements must be considered before treating it as the primary source of truth.

---

### 42. Explain cache-aside

With cache-aside:

1. Read from Redis.
2. On a miss, read from the database.
3. Store the result in Redis with a TTL.
4. Return the result.
5. On writes, update or invalidate the relevant cache.

```ts
const cached = await redis.get(key);
if (cached) return JSON.parse(cached);

const user = await repository.findById(id);
await redis.set(key, JSON.stringify(user), { EX: 300 });

return user;
```

---

### 43. What is cache invalidation?

Cache invalidation ensures cached data does not remain incorrect after the source changes.

Strategies include:

* Delete on write
* Update on write
* Short TTL
* Versioned cache keys
* Event-driven invalidation

TTL is a safety net, not always the complete consistency strategy.

---

### 44. What is a cache stampede?

A cache stampede happens when a popular key expires and many requests simultaneously query the database.

Solutions include:

* Request coalescing
* Distributed locking
* Stale-while-revalidate
* TTL jitter
* Proactive refresh

# Part 7 — Messaging and distributed systems

### 45. When would you use a queue?

I use a queue when work:

* Does not need to finish during the HTTP request
* Needs retries
* Can be processed asynchronously
* Must absorb traffic spikes
* Requires independent scaling

Examples include emails, report generation, webhooks and transaction processing.

---

### 46. What does “at least once delivery” mean?

A message can be delivered more than once. Therefore, consumers must be idempotent.

I may store a processed message ID under a unique constraint or design the database update so applying the same event repeatedly does not duplicate its effect.

---

### 47. How do you handle retries?

I retry only transient failures, using:

* Exponential backoff
* Jitter
* Maximum attempt limit
* Clear timeout
* Dead-letter queue
* Metrics and alerts

Validation failures and other permanent errors should not be retried indefinitely.

---

### 48. What is the transactional outbox pattern?

A normal transaction cannot atomically update a database and publish to a message broker.

The outbox pattern solves this by:

1. Updating business data.
2. Inserting an event into an outbox table in the same transaction.
3. A worker publishes pending events.
4. Published events are marked complete.
5. Consumers process events idempotently.

This avoids losing an event between database commit and message publication.

---

### 49. What is eventual consistency?

Eventual consistency means different services may temporarily hold different views of data, but they converge after events are processed.

A production design must explain:

* What temporary inconsistency users may see
* How failures are retried
* How duplicate events are handled
* How missing events are detected
* How reconciliation repairs inconsistencies

---

### 50. Microservices versus modular monolith?

I usually begin with a well-structured modular monolith unless independent scaling, deployment or team ownership clearly requires separate services.

Microservices provide autonomy and independent scaling but introduce:

* Network failures
* Eventual consistency
* Distributed tracing
* More complex testing and deployments
* Cross-service version management

A senior engineer should not choose microservices simply because the application may grow.

# Part 8 — Performance and reliability

### 51. How would you investigate a slow API?

My approach:

1. Check latency percentiles, error rates and recent deployments.
2. Trace the request across services.
3. Measure database queries and inspect execution plans.
4. Check connection-pool saturation, CPU, memory and event-loop lag.
5. Inspect external dependency latency.
6. Optimize only after locating the actual bottleneck.

I compare p50, p95 and p99 because averages can hide poor tail latency.

---

### 52. How do you detect event-loop blocking?

I monitor event-loop delay and correlate it with CPU usage and slow requests.

Typical causes include:

* Large synchronous loops
* Synchronous filesystem operations
* Large JSON parsing or serialization
* Expensive regular expressions
* Cryptographic work
* Excessive logging

CPU-heavy work should be optimized, chunked, moved to workers, or processed by a separate service.

---

### 53. What is connection pooling?

Creating a database connection for every request is expensive. A pool maintains reusable connections.

The pool must be sized with awareness of:

* Number of application replicas
* Database connection limit
* Expected concurrency
* Query duration

If 20 pods each open 50 connections, the database may receive 1,000 connections and become overloaded.

---

### 54. What are timeouts and circuit breakers?

A timeout prevents a request from waiting indefinitely.

A circuit breaker temporarily stops calls to a failing dependency:

* **Closed:** Calls are allowed.
* **Open:** Calls fail quickly.
* **Half-open:** Limited probe calls test recovery.

They should be combined with bounded retries, fallback behavior, metrics and alerts.

---

### 55. How do you handle graceful shutdown?

When receiving a termination signal:

1. Mark the instance unready.
2. Stop accepting new traffic.
3. Finish or time out in-flight requests.
4. Stop consuming new jobs.
5. Close database and broker connections.
6. Exit cleanly.

In NestJS:

```ts
app.enableShutdownHooks();
```

The deployment platform must allow enough termination time for this process.

# Part 9 — Testing

### 56. How do you test a NestJS application?

I use a testing pyramid:

* Unit tests for domain and service logic
* Integration tests for repositories and infrastructure
* API tests for validation, guards and controllers
* A smaller set of end-to-end tests for critical workflows
* Contract tests for important service boundaries

I prioritize business rules and failure paths rather than chasing a coverage number.

---

### 57. How do you unit-test a NestJS service?

```ts
const module = await Test.createTestingModule({
  providers: [
    UsersService,
    {
      provide: UsersRepository,
      useValue: {
        findById: jest.fn(),
      },
    },
  ],
}).compile();

service = module.get(UsersService);
repository = module.get(UsersRepository);
```

The repository is replaced because the service should be tested independently from the real database.

---

### 58. Mock versus spy?

* A **mock** replaces a dependency or defines its behavior.
* A **spy** observes calls to an existing method and may optionally replace its implementation.

I mock external boundaries, but avoid mocking every internal method because that makes tests tightly coupled to implementation details.

---

### 59. How do you test database code?

For meaningful repository tests, I prefer a real database-compatible environment—often an isolated container—rather than mocking SQL behavior.

The test should verify:

* Constraints
* Transactions
* Queries
* Index-dependent behavior where relevant
* Serialization and mapping

Mocks cannot reliably reproduce actual database semantics.

# Part 10 — Deployment and operations

### 60. Explain your deployment process

An interview-ready answer aligned with your experience:

> “We used GitHub and GitHub Actions for CI/CD. A pull request triggered linting, unit tests, integration tests and a production build. After merge, the pipeline built a versioned Docker image and pushed it to a container registry. Kubernetes deployed that image, while Rancher helped us manage workloads and environments on AWS. We used readiness and liveness probes, configuration through environment-specific secrets, rolling deployments, centralized monitoring and a rollback to the previous image if health metrics degraded.”

---

### 61. Docker image versus container?

* A Docker image is an immutable application package.
* A container is a running instance of that image.

One image can be used to create multiple containers.

---

### 62. Readiness versus liveness probe?

* **Readiness:** Can this instance receive traffic?
* **Liveness:** Is this process alive, or should it be restarted?
* **Startup probe:** Has a slow-starting application finished initializing?

A readiness check may consider critical initialization. A liveness check should not restart every instance merely because a shared downstream database is temporarily unavailable.

---

### 63. How do you manage configuration and secrets?

Configuration can come from environment variables or a configuration service. Secrets should come from a secure secret manager or Kubernetes secrets integrated with appropriate access controls.

I validate required configuration during startup and never log secret values.

# Part 11 — Advanced scenario questions

### 64. Design an order-creation API that prevents duplicate orders

A strong answer:

1. Require an idempotency key.
2. Authenticate the user and validate the request.
3. Create a unique database constraint on user plus idempotency key.
4. Create the order and outbox event in one transaction.
5. Return the stored result for repeated requests.
6. Process payment and notifications through reliable, idempotent consumers.

The database constraint is essential because an application-only check can race.

---

### 65. An endpoint suddenly receives ten times more traffic. What do you do?

1. Confirm whether traffic is legitimate and identify affected endpoints.
2. Apply rate limiting and protect expensive operations.
3. Check CPU, memory, event-loop lag, connection pools and dependency saturation.
4. Scale stateless instances where downstream capacity permits.
5. Cache hot reads and queue asynchronous work.
6. Optimize the measured bottleneck.
7. Add capacity tests and alerts to prevent recurrence.

Scaling the API alone can overload the database, so I consider the complete dependency chain.

---

### 66. A third-party API is unreliable. How do you protect your system?

I use:

* Strict connection and response timeouts
* Retries only for safe, transient failures
* Exponential backoff and jitter
* Circuit breaker
* Concurrency limits
* Caching or fallback where appropriate
* Queue-based processing for non-immediate work
* Monitoring by provider and error category

For non-idempotent requests, I do not retry unless the provider supports idempotency.

---

### 67. How would you process one million records?

I would not load them all into memory.

I would:

* Read them in cursor-based batches or through a stream.
* Process with bounded concurrency.
* Use bulk database operations.
* Store checkpoints for resumability.
* Make processing idempotent.
* Send permanent failures to a dead-letter mechanism.
* Monitor throughput, error rate and memory.

---

### 68. How would you design a rate limiter?

A distributed rate limiter can use Redis with a token-bucket or sliding-window algorithm.

The Redis update should be atomic, typically through a Lua script or a suitable atomic command. The key can include user, API key, tenant or IP address.

The design must also define:

* Limit period
* Burst allowance
* Correct `429` response
* `Retry-After` header
* Behavior when Redis becomes unavailable

---

### 69. How do you maintain backward compatibility?

I prefer additive changes:

* Add optional fields rather than rename existing fields.
* Do not unexpectedly change field meanings.
* Support old event schemas during migration.
* Version genuinely breaking APIs.
* Use consumer-driven contract tests.
* Measure old-version usage before removal.
* Announce a clear deprecation window.

---

### 70. How do you approach a production incident?

1. Assess customer and business impact.
2. Stabilize the system by rollback, feature flag, rate limit or failover.
3. Communicate status and ownership.
4. Use logs, metrics and traces to identify the cause.
5. Recover and verify customer-visible behavior.
6. Write a blameless postmortem.
7. Track concrete prevention actions.

During the incident, mitigation is usually more important than immediately finding the perfect fix.

# Questions about seniority and leadership

### 71. What is expected from a senior backend engineer?

A senior engineer should:

* Own systems, not only tickets.
* Clarify ambiguous requirements.
* Make and explain architectural trade-offs.
* Design for failure, security and operability.
* Review designs and mentor engineers.
* Coordinate with product, frontend, DevOps and security.
* Improve engineering practices.
* Connect technical choices to customer and business outcomes.

---

### 72. How do you make technical decisions?

> “I first clarify functional and non-functional requirements such as traffic, latency, consistency, security and delivery constraints. I compare the simplest viable options, document their trade-offs, and involve the engineers who will operate the system. For high-impact decisions I write a short ADR. After implementation, I verify the decision using production metrics and revisit it if the assumptions change.”

---

### 73. Tell me about a backend architecture you worked with

A version aligned with your actual experience:

> “In my recent project, the application used a React frontend with a NestJS backend in a monorepo. The backend exposed APIs for authentication, portfolio information and blockchain-related workflows. MongoDB stored application data, while Redis supported short-lived and frequently accessed information. We integrated external wallet and blockchain providers, so timeout handling, idempotency and reliable error mapping were important. Authentication evolved from SIWE with nonce verification and session cookies to JWT-based authentication provided through Dynamic. The services were packaged with Docker, deployed to Kubernetes on AWS and managed through Rancher. My focus was on clear module boundaries, shared contracts between frontend and backend, secure authentication and observable failure handling.”

Only claim the areas you personally owned; describe other areas as team architecture.

# Recommended preparation sequence

Given your existing JavaScript and frontend strength, study in this order:

1. **Node internals:** Event loop, streams, memory, worker threads and error handling.
2. **NestJS:** Modules, DI, lifecycle, guards, pipes, interceptors and filters.
3. **API design:** REST, validation, pagination, idempotency and error contracts.
4. **Databases:** SQL, MongoDB, indexes, transactions, locking and query optimization.
5. **Security:** JWT, cookies, OAuth, authorization, OWASP risks and secret management.
6. **Redis/queues:** Caching, invalidation, retries, idempotent consumers and outbox.
7. **System design:** Scaling, consistency, failure handling and service boundaries.
8. **Operations:** Docker, Kubernetes, CI/CD, observability and incident management.
9. **Senior stories:** Ownership, mentoring, trade-offs, production failures and customer impact.

For an eight-year-level role, prepare at least six detailed STAR stories:

* A difficult production incident
* A performance improvement
* An architectural decision
* A security or authentication challenge
* A disagreement and how you resolved it
* A project you influenced beyond your assigned ticket

The most important adjustment is to avoid answering only with definitions. Start with the definition, then explain the production trade-off, and finish with an example from your experience.
