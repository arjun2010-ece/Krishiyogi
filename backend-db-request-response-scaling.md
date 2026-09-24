# Requests, Connection Pools and DB Limits: How Backend Load Really Works

A guide for junior backend developers using Node.js and PostgreSQL.

**What you will learn:**

1. The two different kinds of connection in a backend system
2. What a connection pool is, and how it differs from the DB's own `max_connections`
3. What happens step by step when many requests arrive together
4. What "the server broke down" actually means
5. How to load test and find your real limit
6. When to increase the pool, and when not to

---

## Terms Used in This Guide

The word "client" alone is avoided in this guide because it can mean different things. These three names are used instead.

| Name | What it is | Example |
| --- | --- | --- |
| **Browser / App** | What the end user uses to send requests | Chrome, a mobile app |
| **Backend (Node.js)** | Your Node.js application process, running on a machine | An Express or NestJS app |
| **DB server (Postgres)** | The machine that runs Postgres, and the Postgres program on it | PostgreSQL |

Two more basic terms:

- **Machine:** a computer (or VM, or container) with its own CPU, RAM and disk.
- **Process:** a program that is running on a machine. One machine can run many processes at the same time.

---

## 1. The Big Picture

### 1.1 Two different kinds of connection

Most confusion comes from mixing these two up.

|  | HTTP/TCP connection | DB connection |
| --- | --- | --- |
| Between | Browser/App and Backend (Node.js) | Backend (Node.js) and DB server (Postgres) |
| Opened by | The Browser/App, for each user | The Backend's connection pool |
| Limited by | OS and server limits (thousands) | Pool size (client side) and `max_connections` (server side) |
| Reused? | Sometimes (keep-alive) | Yes, this is the whole point of a pool |

The pool has **nothing to do with how many HTTP connections Node accepts**. It only limits how many DB queries run at the same time.

### 1.2 The request chain

A request passes through a chain of components. Each has its own limit.

```
Browser/App -> Backend (Node.js event loop) -> Connection pool (inside the backend) -> DB connections -> DB server CPU / disk
```

| Component | Limit | Set by |
| --- | --- | --- |
| Node.js | One thread runs your JS; heavy CPU work per request slows everything | Your code |
| Connection pool | e.g. 10 concurrent queries; the rest wait in a queue | App/ORM config |
| Postgres connections | e.g. 100 total, from all clients combined | DB config (`max_connections`) |
| Postgres CPU / disk | How many queries can truly run in parallel, and how fast | Hardware and query quality |

> **Key idea:** your maximum load is set by the first component that runs out. That component is the **bottleneck**. Load testing is how you find out which one it is.

---

## 2. Connection Pool

### 2.1 What it is

A connection pool is a capability of your **backend process**, not of the database. It is a set of already-open connections to the DB, held by your app (through the driver or ORM, such as `pg`, Prisma, TypeORM or Knex) and reused across requests.

Why pool at all: the **backend** is the side that opens each connection to the DB server. Opening one (TCP, authentication, TLS) is slow, and on the DB server every connection gets its own Postgres process (see section 3.5) that uses memory. Reusing connections avoids both costs.

### 2.2 What "pool size = 10" means

- Your app holds up to 10 open connections to Postgres.
- A request that needs a query **borrows** a connection, runs the query (or a whole transaction), then **returns** it.
- At most **10 queries or transactions run concurrently** from that process.
- An 11th request that needs the DB while all 10 are busy **waits in a queue** inside your app. If it waits longer than the acquire timeout, it fails with an error such as "timeout acquiring connection".

### 2.3 You always have a pool, even if you never configured one

If you never touched pool settings, your driver or ORM already created one with a default size. For example, `pg` (node-postgres) defaults to 10. The setup works, but you don't yet know its limits. Step one of any performance work is finding out the real numbers.

### 2.4 The pool is per process

If you run 4 instances (or 4 Node cluster workers, or 4 containers), each with a pool of 10, Postgres can see up to **40** connections.

```
total DB connections = pool size x number of app processes
```

### 2.5 How many Node.js processes do we normally run?

A Node.js process runs your JavaScript on **one thread**, so one process uses about one CPU core for your code. To use a machine with several cores, you run several Node processes. Two widely used setups:

| Setup | How | Typical use |
| --- | --- | --- |
| Several Node processes on one machine | PM2 cluster mode or Node `cluster`, usually one process per CPU core | Simple deployments on a single VM |
| Many small containers, each running **one** Node process | Docker plus an orchestrator (ECS, Kubernetes, etc.) behind a load balancer | Common in modern deployments |

Practical rules:

- Roughly **1 Node process per available CPU core**.
- At least **2 instances** in production, so one crash or one deploy does not take the app down.
- Load test one instance first, then add instances only when you need more capacity.
- In every setup, **each Node process has its own pool**. So total DB connections = pool size x total Node processes across all machines.

### 2.6 Why is the pool configured in the ORM?

Because the ORM (or the driver under it) is not just a query wrapper. It is the **client library that owns the connections**. It lives inside your Node process, opens the sockets to Postgres, and therefore manages them. The config sits where the code that opens the connections lives.

---

## 3. The DB's Own Limit: `max_connections`

Postgres has its own global cap, `max_connections` (default 100). Check it with:

```sql
SHOW max_connections;
```

### 3.1 Pool size vs. `max_connections`

Both limits exist because they protect different sides.

|  | Pool size | `max_connections` |
| --- | --- | --- |
| Where it lives | Backend (Node.js process) | DB server (Postgres) |
| Purpose | Reuse connections, and cap how many queries this one backend process sends at once | Protect the DB server from being overwhelmed by all backends and tools combined |
| Who knows about it | Only that one backend process | The DB server, which sees every connection from every backend and tool |

The Browser/App is never involved in either limit.

One backend process cannot know how many other backend processes or tools are connected to the DB server, so it cannot manage the DB server's global limit. The DB server cannot reuse the backend's connections for it. Both limits are needed.

### 3.2 What happens when `max_connections` is exceeded

It is a **hard cap**, not a slowdown mechanism. New connections are **rejected** with an error such as "too many clients". The DB server does not get slower because of this cap. It gets slower when more queries need CPU than the CPU can serve (see section 5.1).

### 3.3 What else uses connections?

`max_connections` must cover more than your app:

- Migration jobs and cron workers
- Admin tools and monitoring
- Old and new instances that overlap during a deploy
- A few slots Postgres reserves for superusers

### 3.4 Why a huge `max_connections` is not the goal

- Each connection gets its own Postgres process on the DB server, and that process uses memory (section 3.5).
- The DB server's capacity comes from its CPU cores, memory and disk, not from the number of connections it allows (sections 3.6 and 3.7).
- Raising `max_connections` only lets more connections in. It does not make the DB server faster.

### 3.5 What does "each connection is a separate process" mean?

"Server" can mean a machine or a program. Here it is one DB **machine** running the Postgres **program**. When the backend opens a connection, Postgres starts a **new process on that same machine**, dedicated to that connection. (Postgres documentation calls this a "backend process", but it lives inside the DB server, not in your Node.js app.)

```
Backend (Node.js)               DB server (one machine: CPU, RAM, disk)
pool connection 1  ----------->  Postgres process #1
pool connection 2  ----------->  Postgres process #2
...
pool connection 10 ----------->  Postgres process #10
```

- Connections do **not** go to different machines. They go to different processes on the **same** DB machine, and those processes share its CPU, RAM and disk.
- Each Postgres process handles one query at a time and uses memory (a few MB at minimum, more for heavy queries).
- 100 connections therefore means 100 processes on one machine, which is why a very large `max_connections` costs memory even if most connections are idle.

### 3.6 How many queries can a DB server run in parallel?

A CPU core does one thing at a time. The operating system gives each running process tiny time slices (a few milliseconds) and switches between them very quickly.

So "4 cores = only 4 queries" is not exactly right, and neither is "100 queries at once":

- At any single instant, at most 4 queries are **executing on the CPU** (one per core).
- But a query is not always using the CPU. It also waits for disk reads, locks and the network. While it waits, its core is free for another query. So somewhat more than 4 queries can be usefully **in progress**.

| Query type | Where its time goes | Useful concurrency on 4 cores (rough) |
| --- | --- | --- |
| CPU-heavy (big sorts, aggregations) | Almost all CPU | About 4, the number of cores |
| Typical web queries (mixed) | CPU plus some disk/network waiting | Roughly 8 to 16 |
| Disk-heavy (data not in memory) | Mostly waiting for disk | More, limited by disk speed |

These are rules of thumb. Measure with a load test.

**Example, 8-core DB server:**

- 8 CPU-heavy queries at once: each gets a full core and runs at full speed.
- 16 of the same queries at once: each gets about half a core, so each takes about twice as long. The number of queries finished per second is the same as with 8.

Extra concurrency beyond what the CPU can serve does not add throughput. It only makes every query slower.

### 3.7 Pool size, connections and CPU cores: three limits in a row

Example: backend pool = 20, DB server has 8 cores and `max_connections` = 100. At the same moment, 100 requests each need a DB query.

1. **Pool (in the backend):** only 20 queries are sent to the DB server. The other 80 wait in the pool queue.
2. **DB connections:** 20 connections are in use. That is well below 100, so `max_connections` is not the limit here.
3. **CPU (on the DB server):** 20 Postgres processes now compete for 8 cores. The operating system rotates them in short slices, so about 8 execute at any instant. The other 12 are not waiting for a whole query to finish. They take turns every few milliseconds, so all 20 make progress, each more slowly than if it were alone.

So a request can wait in **two queues**: the pool queue (in the backend) and the CPU queue (on the DB server). Both add latency.

Note that `max_connections` = 100 does **not** mean 100 queries run in parallel. It is only how many connections the DB server will accept from all backends and tools combined. At any moment most of them are usually idle. With one backend and a pool of 10, the DB server never sees more than 10 active queries from it.

For a mixed workload, a pool of 20 on an 8-core DB server is reasonable. A pool of 100 on the same server would likely be too much.

### 3.8 What if we have more than one DB server?

Your understanding is right: capacity comes from CPU cores, memory and disk, and connections are only the way in. More DB machines add more CPU, memory and disk. Two DB machines with `max_connections` = 100 each can accept 200 connections and have twice the CPU.

But Postgres does not spread work across machines by itself. You have to set it up:

| Option | What it does | When |
| --- | --- | --- |
| Read replicas | Copies of the data on other machines; the app sends reads there, writes still go to the one primary | Read-heavy apps |
| Splitting data across machines (sharding) | Different data lives on different machines | Very large systems; complex |
| Separate DBs per service | Each service has its own DB server | Separate applications |

The simplest first step is usually a bigger DB machine (more cores) and fixing slow queries.

---

## 4. What Happens When 100 Requests Arrive Together

Assume one Node instance, one Postgres, and a pool of 10.

```
100 requests arrive -> Node accepts all 100 and starts all 100 handlers
   |- 40 don't need the DB -> finish right away, unaffected by the pool
   '- 60 need the DB -> each calls pool.query()
        |- 10 get a connection -> sent to Postgres
        '- 50 wait in the pool's queue (in your app's memory)
             -> as each of the 10 finishes, the next waiter takes its connection
```

Points to notice:

1. Node accepts all 100 HTTP connections. The pool does not limit this.
2. Node is asynchronous, so it interleaves all handlers on the event loop while they wait for I/O.
3. The pool only matters at **the one step** where a handler runs a DB query. Only that step is processed in "batches" as connections free up.
4. Waiting requests are not dropped. They queue. If one waits past the acquire timeout, it errors.
5. Requests that don't touch the DB never ask the pool for anything.

### 4.1 Which requests use the pool?

Step by step:

1. Every request from a Browser/App needs an HTTP/TCP connection to the backend. (Browsers may reuse one connection for several requests with keep-alive.)
2. The backend runs your handler code.
3. **Only if the handler runs a DB query**, it borrows a connection from the pool. A handler that does not query the DB never touches the pool.
4. When the query (or transaction) finishes, the connection goes back to the pool.

So if one request touches the DB and another doesn't, that is 2 HTTP requests but **at most 1 DB connection in use**. The pool's connections were opened earlier by the backend, and they are lent out only while a query or transaction runs. A request that runs several queries borrows a connection per query, or holds one for the whole transaction.

---

## 5. What Does "The Server Broke Down" Mean?

It is not one thing. The general symptom is: **latency keeps growing, then requests time out or fail**. The cause depends on which layer is full.

| Layer that is full | What happens | Symptom |
| --- | --- | --- |
| Pool | Queue of waiting requests grows, each waits longer | Latency rises, then "timeout acquiring connection" errors |
| Postgres CPU / disk | Queries themselves slow down because too many run in parallel; this also drains the pool more slowly, so the queue grows | Query time rises, then the queue grows too |
| Node CPU | Event loop is busy, so everything is delayed, including requests that don't need the DB | Global slowdown |
| Memory | Pending requests pile up faster than they finish | Process crashes (out of memory) |

### 5.1 Overload in simple numbers

Say the DB server has 4 CPU cores and a typical query needs about 10 ms of CPU time.

- One core can finish about 100 such queries per second, so 4 cores can finish about **400 queries per second**. That is the DB server's capacity.
- If 300 queries per second arrive: fine. Each finishes in roughly 10 to 20 ms.
- If 400 arrive: right at the limit. Latency starts to rise.
- If 800 arrive: only 400 can be finished per second, so 400 more queries are left unfinished every second. The queue keeps growing, and latency goes from 20 ms to 200 ms to 2 seconds to 45 seconds and beyond, for as long as the overload lasts.

What the user sees:

1. Pages get slow.
2. The Browser/App, load balancer or proxy gives up after its timeout (often somewhere between 5 and 60 seconds, depending on setup). The user gets an error or a timeout.
3. Users refresh or apps retry, which adds even more requests.
4. The backend often keeps working on requests the browser already abandoned. That is wasted work that makes the overload worse.

This is why overloaded systems tend to collapse instead of degrading slowly. Find your limit **before** it happens with a load test, and set timeouts deliberately so overload fails fast.

The real picture is a little worse than this simple math. With many queries in parallel there is extra overhead (switching between processes, lock contention, memory pressure), so throughput can drop below the theoretical 400.

---

## 6. Finding Your Limit: Load Testing

A load testing tool such as [Autocannon](https://github.com/mcollina/autocannon) sends many requests and reports how many were handled in a given time, plus latency.

### 6.1 Step-by-step process

**Step 1: Write down your current limits.** Check your pool size (config or ORM docs) and run `SHOW max_connections;`.

**Step 2: Decide what "good" means.** For example: p99 latency under 300 ms and error rate under 1%. "Maximum requests per second" is meaningless if latency is terrible or requests fail at that rate.

**Step 3: Load test one realistic endpoint.** Pick an endpoint that really queries the DB, and use a DB with realistic data volume (an empty table hides slow queries).

```bash
autocannon -c 10 -d 30 http://localhost:3000/users
```

- `-c` is the number of concurrent HTTP connections from the tester to **your Node server**.
- `-d` is the duration in seconds.
- This `-c` is **not** the DB pool. They are different things.
- Run the tester from a different machine if possible, otherwise it competes with your app for CPU.

**Step 4: Increase concurrency in steps.** Run `-c 10`, then `20`, `50`, `100`, `200`. Write down requests/sec and p99 latency for each. You will see this pattern:

- At first, more concurrency gives more requests/sec.
- Then requests/sec **stops growing** while latency **keeps rising**. That is the saturation point (your practical max load).
- Push further and errors and timeouts appear.

**Step 5: At the saturation point, find which component is full.**

| Check | How | What it means |
| --- | --- | --- |
| Node CPU near 100% or event loop lag | `top`, or `perf_hooks.monitorEventLoopDelay` | Node is the bottleneck |
| Requests waiting for a pool connection | `pool.waitingCount` (in `pg`) | Pool is the bottleneck |
| DB CPU / disk | Server metrics, `top` on the DB host | DB hardware is the bottleneck |
| Active DB connections and running queries | `SELECT state, count(*) FROM pg_stat_activity GROUP BY state;` | Shows how many connections are actually busy |
| Slow queries | `pg_stat_statements`, `EXPLAIN ANALYZE` | Query or index problem |

**Step 6: Match the symptom to the fix.**

| What you see | Fix |
| --- | --- |
| Waiting count high, DB CPU low | Increase pool size |
| DB CPU high, queries slow | Add indexes, rewrite queries, cache. Do **not** grow the pool |
| Node CPU 100%, DB idle | Reduce CPU work per request, or run more Node processes |
| Connections stuck in `idle in transaction` | Fix code that holds a transaction open, or leaks connections |
| "too many connections" from Postgres | Total (pool x instances) exceeds `max_connections`; lower the pool or add PgBouncer |

**Step 7: Change one thing, then re-run the same test.** Compare with the previous numbers. Changing several things at once means you won't know what helped.

**Step 8: Scale out only after one instance is understood.** If one instance handles X requests/sec and you need more, run more instances. Then check the multiplication: `pool size x instances <= max_connections` (with headroom for deploys and other clients). If it doesn't fit, put PgBouncer in front of Postgres.

---

## 7. Sizing the Pool

### 7.1 Quick calculation: pool size and throughput

If each query takes 20 ms and the pool has 10 connections:

- One connection handles 1000 / 20 = 50 queries/sec.
- The pool ceiling is 10 x 50 = **500 queries/sec** (assuming one query per request).

If your test plateaus near 500 requests/sec with the pool queue growing, the pool is the limit. If it plateaus at 200 requests/sec while the pool queue is empty, look elsewhere.

Slow queries hurt a lot: halving query time doubles the ceiling with no config change.

### 7.2 Checklist before increasing the pool

1. **DB connection budget.** Total = pool size x instances, including deploy overlap, migration jobs and admin tools. Keep it comfortably under `max_connections`.
2. **Autoscaling.** If instances scale out, connections multiply. An external pooler (PgBouncer, RDS Proxy) is the usual fix.
3. **DB resources.** Extra connections beyond what the CPU and disk can serve add contention, not throughput.
4. **Where the time is going.** Requests waiting for a connection while DB CPU/IO is low means the pool is the bottleneck. DB CPU high means fix queries first.
5. **Long-held connections.** A transaction held open during an external API call, or a forgotten release (a leak), drains the pool regardless of its size. Fix these first.
6. **Timeouts.** Set the acquire timeout and idle timeout deliberately.

### 7.3 When to increase vs. not

| Increase | Don't increase |
| --- | --- |
| High pool wait time, DB CPU/IO has headroom | DB CPU or IO already saturated |
| Many short queries, few instances | Many instances already; total near `max_connections` |
| Traffic is clearly parallel and the pool is small | Slow queries, missing indexes or long transactions are the real cause |
|  | Connection leaks |

### 7.4 Single Node, single Postgres: should the pool go up to `max_connections`?

No. `max_connections` is a ceiling to stay under, not a target. Raise the pool in steps (10, 20, 30), re-run the load test each time, and stop when throughput stops improving or DB CPU is saturated. For a small single DB that point is often somewhere around 10 to 30, not 100.

A commonly cited starting formula for the DB-side optimum is roughly `(cores x 2) + effective_spindle_count`, which is often smaller than people expect.

### 7.5 Fix order when the system is overloaded

1. Fix slow queries and indexes, and add caching. Cheapest, usually the biggest win.
2. Increase the pool, only if Postgres has CPU/IO headroom.
3. Add more Node instances (recompute pool x instances against `max_connections`).
4. Scale the DB: bigger machine, or read replicas for read-heavy load.

---

## 8. Common Misconceptions

| Misconception | Reality |
| --- | --- |
| "A pool of 10 means only 10 requests can be handled" | Node accepts and runs all requests. The pool limits only concurrent **DB queries**. |
| "Each request opens a new DB connection" | Connections are opened once and reused. |
| "Requests that don't use the DB use a connection" | They never touch the pool. |
| "Pool size and `max_connections` are the same thing" | One is a client-side cap per process, the other a server-side cap across all clients. |
| "Set the pool to `max_connections` for best performance" | Beyond the DB's real parallelism, more connections make things slower. |
| "Raising `max_connections` adds DB capacity" | It only allows more connections. |
| "Autocannon `-c 100` means 100 DB connections" | It means 100 HTTP connections to your server. |
| "A 4-core DB server runs exactly 4 queries" | At most 4 execute on the CPU at one instant, but queries also wait on disk and locks, so roughly 2 to 4 times the core count can be usefully in progress. |
| "`max_connections` = 100 means 100 queries run in parallel" | It is only how many connections are accepted. Most are idle, and CPU cores decide real parallelism. |
| "Each connection goes to a different server" | Each connection gets its own process on the same DB machine. |
| "More DB machines automatically share the load" | Only if the app is set up for it (read replicas, splitting data). |

---

## 9. One-Paragraph Summary

The pool caps concurrent DB connections per process, not concurrent requests. Node accepts and runs all requests; only the DB step queues. I load test with increasing concurrency until throughput plateaus and latency spikes, then check which layer is saturated: Node's event loop, the pool, or Postgres CPU/IO. I fix that layer, re-test, and only then scale horizontally, keeping pool size x instances under the DB's `max_connections`. Raising the pool helps only while Postgres still has spare capacity.

---

## 10. Check Your Understanding

Try answering each question yourself before reading the answer.

**Q1. One request touches the DB and another doesn't. Is that 2 DB connections?** No. It is 2 HTTP requests but at most 1 DB connection. The request that doesn't touch the DB never asks the pool for anything. The other borrows an existing pool connection only while its query runs.

**Q2. 100 users send requests at once. Does the pool decide how many the backend can handle?** No. Node accepts all 100 HTTP connections and starts all 100 handlers. The pool only limits how many DB queries run concurrently. Requests waiting for a connection queue up and proceed as connections free up, but only the DB step is queued.

**Q3. If the pool is small, are requests processed in batches?** Only the DB portion. Requests that need the DB are served as pool connections free up. Requests that don't need the DB are unaffected.

**Q4. What does it mean when a server "breaks down"?** Latency grows and requests time out or fail. The cause could be a full pool queue, a saturated Postgres CPU/disk, a busy Node event loop, or memory exhaustion. Diagnose which layer is full before changing anything.

**Q5. Does Postgres slow down when it hits `max_connections`?** No. It rejects new connections with an error. Slowdown comes from CPU/disk saturation when too many queries run in parallel.

**Q6. Why does the ORM configure the pool if the DB already has a limit?** The ORM or driver owns the connections inside your process, so it manages the pool. The DB's limit is a separate, global cap for all clients. Each side protects itself.

**Q7. Single Node and single Postgres. Should I raise the pool until it reaches `max_connections`?** No. Raise it gradually and load test each time. Stop when throughput stops improving or DB CPU saturates, which usually happens far below `max_connections`.

**Q8. Autocannon shows 2000 requests/sec with a pool of 10. How is that possible?** The pool limits concurrency, not total throughput. Queries are short (a few ms), so each connection is reused many times per second, and some requests may not hit the DB at all (cache, static responses).

**Q9. Node is single-threaded. Why would you need more than one DB connection?** The event loop doesn't block on I/O, so many requests can be waiting on DB responses at the same time. A connection handles one query at a time, so each in-flight query needs its own connection.

**Q10. You run 5 instances with a pool of 20 each, and Postgres `max_connections` is 100. What could go wrong?** Total possible connections is 100, exactly the limit, leaving no room for migrations, admin tools, reserved slots, or old and new instances overlapping during a deploy. Connection errors are likely under load or during deploys. Lower the pool, or put PgBouncer in front.

**Q11. Does a 4-core DB server run only 4 queries at a time?** At most 4 queries execute on the CPU at one instant. But queries also wait on disk, locks and the network, so more than 4 can be usefully in progress. For typical web queries, roughly 2 to 4 times the core count. For CPU-heavy queries, about the core count. Beyond that, extra concurrency only makes each query slower.

**Q12. Two DB machines, each with `max_connections` = 100: is capacity doubled?** The CPU, memory and disk are doubled, and 200 connections can be accepted, but Postgres does not split work between machines by itself. You need read replicas or a split of the data, and the app must send queries to the right machine. More connections alone never add processing power.

**Q13. What does "each connection is a separate process" mean?** The DB server is one machine. Postgres starts one new process on that machine for every connection. Connections therefore go to different processes on the same machine, sharing its CPU, RAM and disk.

**Q14. How are Node.js apps usually run in production?** Roughly one Node process per CPU core, either several processes on one machine (PM2 cluster mode) or many small containers with one Node process each behind a load balancer. Use at least 2 instances. Each process has its own pool.

**Q15. Pool = 20, DB server has 8 cores. 100 requests need the DB at once. What happens?** 20 queries are sent to the DB server; 80 wait in the pool queue in the backend. On the DB server, 20 Postgres processes share 8 cores by taking turns in short time slices, so all 20 progress but each more slowly. Requests can wait in two places: the pool queue and the CPU queue.

**Q16. A request doesn't need the DB. Does it open any connection?** It needs the HTTP/TCP connection from the Browser/App to the backend, like every request. It never touches the pool, so it uses no DB connection.
