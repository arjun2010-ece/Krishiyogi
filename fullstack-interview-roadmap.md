# 1. Research 1:  

**For backend/full-stack roles, focus on these areas:**

* Node.js and TypeScript
* API design and integrations
* Databases and data modelling
* Authentication and security
* System design
* Background jobs and messaging
* Cloud and deployment
* Testing
* Monitoring and debugging

Based on the descriptions reviewed, this is the preparation guide I’d use for you. Since frontend is already your strength, put your effort into **building, deploying and maintaining the backend behind a feature**.

**1. Node.js and TypeScript — build reliable backend services**

* Understand the event loop, asynchronous execution and what blocks requests.
* Handle promises, errors, timeouts and concurrent operations.
* Know when to use streams, worker threads and background jobs.
* Use TypeScript effectively, while understanding that incoming data still needs runtime validation.
* Learn **NestJS** well: modules, controllers, services, dependency injection, guards, pipes and exception filters.
* Understand the Express request/middleware model beneath the framework.

**Your target:** independently structure a backend, implement business logic and diagnose unexpected behaviour.

**2. API design and integrations — build APIs other applications can depend on**

* Design REST resources, routes, HTTP methods and status codes.
* Implement input validation, consistent errors, pagination, filtering and sorting.
* Understand authentication, authorisation, rate limiting and API versioning.
* Handle idempotency: repeated requests should not accidentally repeat a payment or booking.
* Integrate external APIs with timeouts, bounded retries and useful error handling.
* Implement webhooks with signature verification and duplicate-event handling.
* Learn GraphQL fundamentals: schemas, resolvers, authorisation and the N+1 problem.
* Document APIs using **OpenAPI/Swagger**.

**Your target:** build more than CRUD endpoints—make their behaviour predictable when requests fail or repeat.

**3. Databases and data modelling — make data correct and queries efficient**

Start with **PostgreSQL**:

* Model entities, relationships, primary keys, foreign keys and constraints.
* Write SQL queries: joins, aggregations, filtering and pagination.
* Understand indexes and investigate queries using `EXPLAIN ANALYZE`.
* Use transactions and understand isolation, locking and race conditions.
* Write safe schema migrations.
* Understand connection pooling and common ORM performance problems.
* Use **Prisma or TypeORM**, while remaining comfortable with SQL.

Then learn:

* **Redis:** caching, expiry, invalidation and session storage.
* **MongoDB:** document modelling, embedding versus referencing, indexes and aggregation—particularly for roles using it.

**Your target:** explain how your database prevents double bookings, duplicate records and inconsistent updates.

**4. Authentication and security — control who can do what**

* Distinguish authentication from authorisation.
* Understand sessions, cookies, JWTs and their trade-offs.
* Learn OAuth 2.0 and OpenID Connect; integrate an identity provider such as **Auth0**.
* Implement role-based and resource-level permissions.
* Enforce tenant isolation: one customer must never access another customer’s data.
* Understand SQL injection, XSS, CSRF, CORS and secure cookie settings.
* Handle passwords, secrets and sensitive logs safely.
* Apply least privilege to both application users and cloud services.

**Your target:** enforce permissions in the backend and prove them with tests.

**5. System design — explain how the parts fit together**

* Separate controllers, business logic and persistence concerns.
* Understand modular monoliths versus microservices and when each makes sense.
* Design stateless services that can run across multiple instances.
* Understand load balancing, caching, database bottlenecks and horizontal scaling.
* Choose between synchronous API calls and asynchronous messaging.
* Understand consistency, partial failures, retries and duplicate processing.
* Explain decisions in terms of requirements, complexity, reliability and cost.

**Your target:** design a booking, order or notification system and explain what happens when a component fails.

**6. Background jobs and messaging — handle work outside the request**

* Move slow tasks—emails, exports and document processing—to workers.
* Understand producers, consumers, acknowledgements and concurrency.
* Implement retries with backoff, dead-letter queues and failure recovery.
* Make consumers idempotent.
* Understand the problem of saving data successfully but failing to publish its event.
* Learn one queue practically: **AWS SQS or BullMQ with Redis**.
* Learn what RabbitMQ and Kafka are used for; go deeper when a target role requires them.

**Your target:** recover from a worker crash without losing work or repeating business effects.

**7. Cloud and deployment — get your backend into production**

**Choose AWS first** based on the reviewed descriptions. Focus on:

* **Docker:** images, containers, Dockerfiles, networking and environment configuration.
* **ECS/Fargate:** deploy and operate a containerised Node application.
* **RDS/Aurora:** run PostgreSQL, manage connections and understand backups.
* **S3:** store files and implement controlled uploads/downloads.
* **IAM:** roles, permissions and temporary credentials.
* **Networking:** VPC basics, security groups, private database access, DNS and HTTPS.
* **SQS and Lambda:** background processing and event-driven tasks.
* **GitHub Actions:** automate tests, builds and deployments.
* **Terraform:** create repeatable infrastructure.
* Safe releases: health checks, compatible database migrations and rollback.

Learn **Kubernetes basics** afterward: pods, deployments, services, configuration, probes and logs. Deep cluster administration can wait.

**Your target:** deploy your service yourself, explain the deployment and recover from a bad release.

**8. Testing — prove business rules and failure handling**

* Unit-test business logic.
* Integration-test APIs against a real test database.
* Test authentication, permissions and tenant isolation.
* Test duplicate requests, concurrent updates and failing dependencies.
* Mock external services appropriately.
* Add a few end-to-end tests for critical workflows.
* Run tests automatically in CI.

Use **Jest or Vitest**, plus **Supertest** for HTTP integration tests.

**Your target:** demonstrate that important behaviour remains correct under failure, not just that the happy path works.

**9. Monitoring and debugging — understand what happens after deployment**

* Write structured logs with request/correlation IDs.
* Understand metrics: latency, error rate, throughput and resource usage.
* Use traces to follow requests through services and dependencies.
* Investigate slow queries, exhausted connection pools, memory growth and event-loop blocking.
* Set actionable alerts and understand basic incident response.

Start with **CloudWatch and OpenTelemetry**. Understand the purpose of tools such as Datadog, Grafana and Sentry.

**Your target:** investigate a slow or failing application using evidence.

**How I’d prioritise your preparation**

1. **First:** Node/NestJS → API design → PostgreSQL → authentication.
2. **Next:** meaningful tests → background jobs → Docker/AWS deployment.
3. **Then:** monitoring → failure recovery → deeper system design.

Practise system-design reasoning and testing throughout.

Use **one project** to connect everything: a small booking application with users, permissions, PostgreSQL, background notifications, automated tests and an AWS deployment. Keep its frontend simple.

Your central goal is to confidently say: **“I can design the API and database, secure the feature, test it, deploy it and troubleshoot it in production.”**


# 1. Research 2:  

# JS Fullstack Interview Prep Roadmap
*Reverse-engineered from ~40 LinkedIn job postings (Portugal, UK, Germany, Netherlands, Spain, France) — September 2026*

## How to read this
Skills are grouped by how often they showed up in real job descriptions. Tier 1 = don't walk into an interview without being fluent in these. Tier 2 = expect at least one question. Tier 3 = differentiators that get you past screening rounds for mid/senior roles.

---

## Tier 1 — Must be fluent (60%+ of postings)

| Skill | What "fluent" looks like in an interview |
|---|---|
| React | Component lifecycle, hooks (useState/useEffect/useMemo/useCallback), state management approaches, why re-renders happen |
| Node.js | Event loop, async patterns (callbacks → promises → async/await), how Node handles I/O |
| TypeScript | Interfaces vs types, generics, utility types, why it matters for a team codebase |
| REST API design | Resource naming, status codes, idempotency, pagination, versioning |
| Agile/Scrum | Be ready to talk fluently about sprint ceremonies — this is a soft-skill screen, not a coding one |
| CI/CD | What a pipeline does stage by stage (lint → test → build → deploy), why it matters |

**Status check against your NestJS prep doc:** your existing material already covers guards/pipes/interceptors/exception filters — that's Node.js + REST API design territory, so you're already deep in Tier 1. Good foundation.

---

## Tier 2 — Expect at least one question (45–60%)

| Skill | Interview angle |
|---|---|
| Docker | What a Dockerfile does, why containers vs VMs, docker-compose basics |
| AWS / cloud | Not deep AWS certs — just "have you deployed something to the cloud and what did that involve" |
| SQL (Postgres/MySQL) | Joins, indexing basics, N+1 query problem |
| MongoDB / NoSQL | When you'd reach for NoSQL over SQL, schema design tradeoffs |
| Testing (Jest) | Unit vs integration tests, mocking, what you'd test in a guard/pipe/service |

**Gap to close:** this is likely your next study block after NestJS internals. Testing especially — "how would you test this guard" is a very natural NestJS interview follow-up question and ties directly into your existing prep.

---

## Tier 3 — Differentiators for mid/senior roles (25–40%)

| Skill | Why it matters |
|---|---|
| NestJS (specifically) | Showed up more than expected — especially UK/Spain senior postings, almost always paired with TypeScript + Postgres/Mongo + GraphQL or REST. **This validates your current prep focus directly.** |
| GraphQL | More common in senior/enterprise postings than startups — resolvers, schema design, N+1 problem (Dataloader) |
| Next.js | Increasingly replacing plain React — SSR/SSG concepts, when you'd reach for it |
| Microservices | Senior-level question territory — service boundaries, communication patterns (REST/queues), data consistency |

---

## Suggested prep order (reverse-engineered priority)

1. **Lock down Tier 1** — you're most of the way there via NestJS/Node fundamentals. Make sure React fundamentals are equally spoken-fluent, not just recognized.
2. **Testing next** — highest-frequency gap relative to what's in your current prep doc. Practice explaining how you'd unit test a guard, pipe, and service in NestJS specifically — this is a very likely real interview question given your prep focus.
3. **SQL + Docker basics** — not deep expertise, just enough to speak concretely for 2-3 minutes each.
4. **NestJS depth + GraphQL exposure** — this is where you differentiate for mid/senior roles, and it's already your stated focus.
5. **Microservices concepts** — lighter touch, mostly relevant if targeting senior titles.

---

## Notes on methodology
Based on reading individual job description text from ~40 LinkedIn postings surfaced via targeted search (not a full scrape — LinkedIn blocks that without login). Treat percentages as directional signal from real postings, not a controlled statistical sample. Portugal/EU postings specifically also consistently required fluent English even for local roles — worth having your technical explanations ready in English regardless of interview language.
