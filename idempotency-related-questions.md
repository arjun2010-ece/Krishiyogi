Think of idempotency as a **“don’t do it twice” safety rule**.

A user clicks “Pay” once, but because their network is slow, the app sends the request again. The server must not charge them twice.

## 1. What is idempotency? Why is it important?

> “Idempotency means that repeating the same request has the same final result as doing it once. It protects us when clients retry because of timeouts, network issues, double-clicks, or message redelivery. It is especially important when an action creates money movement, an order, or another irreversible side effect.”

Example: `POST /payments` is sent twice, but only one payment is created.

---

## 2. Which HTTP methods are naturally idempotent?

> “`GET`, `PUT`, `PATCH` and `DELETE` are generally designed to be idempotent because repeating them should leave the resource in the same state. `POST` is not naturally idempotent because each call may create a new resource. But HTTP method alone is not enough; the actual business behaviour matters.”

Examples:

* `GET /users/1` repeated → same user returned.
* `PUT /users/1` with the same data repeated → user still has that data.
* `DELETE /users/1` repeated → user remains deleted.
* `POST /orders` repeated → may create two orders, so needs protection.

Small nuance: a `PATCH` can be non-idempotent if it means “increase balance by €10.” Repeating it changes the balance again.

---

## 3. Which endpoints would you make idempotent?

> “I make endpoints idempotent when a retry could create a duplicate or costly side effect. Typical examples are payments, refunds, transfers, orders, bookings, subscriptions, account creation, sending important notifications, webhooks, and background-job consumers.”

Ask yourself:

> “If this request runs twice by accident, can it hurt the user or the business?”

If yes, it needs idempotency or another strong duplicate-protection mechanism.

---

## 4. Should every endpoint be idempotent?

> “No. I would not add idempotency keys to every endpoint because it adds storage, cleanup, and behaviour to maintain. I use it where duplicate execution is a real risk. For read-only endpoints, it is unnecessary. For simple updates, a database constraint or normal `PUT` behaviour may already be enough.”

So:

* `GET /products` → no need.
* `PUT /profile` → normally already safe.
* `POST /payment` → yes, strongly needed.
* `POST /send-email` → depends; probably yes for transactional emails.

---

## 5. How do you decide whether an endpoint needs it?

> “I look at three things: can the client retry it, does it create a side effect, and would duplicate execution cause harm? If the answer is yes, I add idempotency.”

Easy memory rule: **Retry + side effect + harm = idempotency.**

---

## 6. How would you make `POST /payments` idempotent?

> “The client generates a unique idempotency key for one payment attempt and sends it in a header. The server stores that key with the request status and result. If the same key comes again, the server returns the original result instead of creating another payment.”

Example:

```http
POST /payments
Idempotency-Key: 8b5d-payment-attempt-123
```

Server flow:

1. Receive request and key.
2. Check whether the key already exists.
3. If it exists and succeeded, return the saved payment response.
4. If it does not exist, create a record for that key.
5. Create the payment and save its final response.
6. Return that response.

---

## 7. Who creates the idempotency key?

> “Usually the client creates it, because it knows that two retries belong to the same user action. For example, the frontend creates one key when the user clicks Pay, and uses that same key for retries. A new payment attempt gets a new key.”

The important part is: **same action = same key; new action = new key.**

---

## 8. What if the same key comes with the same request?

> “I return the original result. I do not run the business action again.”

For example, the first request created payment `pay_123`. A retry returns `pay_123` again.

---

## 9. What if the same key comes with a different request body?

> “I reject it, usually with a conflict error. One idempotency key represents one specific action, so allowing different payloads would be unsafe and confusing.”

For example, a key used for €20 should not later be reused for €200.

---

## 10. What if two identical requests arrive at the same time?

> “An in-memory check is not enough because both requests may check before either saves anything. I use a database unique constraint on the idempotency key, often combined with a transaction. One request wins; the other detects the existing record and returns or waits for the original result.”

This is the important senior-level point: **the database is the final protection against concurrency.**

---

## 11. Database, Redis, or both?

> “For critical operations such as payments or orders, I prefer the database because it is durable and can use a unique constraint. Redis can help with speed or short-lived locks, but I would not rely on Redis alone for something financially important. In many systems, the database is the source of truth and Redis is optional optimisation.”

---

## 12. How long should keys be kept?

> “It depends on how long a client, queue, or external provider may retry. For payments, I might keep them for at least 24 hours or according to the provider’s retry window. The retention period should be documented and old records cleaned up safely.”

---

## 13. What if the payment succeeds, but the client gets a timeout?

> “This is exactly why idempotency exists. The client retries with the same key. The server finds the earlier successful operation and returns the original payment result instead of charging again.”

This is a very common real production scenario.

---

## 14. How do unique constraints help?

> “A unique database constraint makes it impossible to insert two records with the same idempotency key. Even if two server instances handle the request at the same time, the database prevents duplicate creation.”

For example:

```sql
UNIQUE (user_id, idempotency_key)
```

Including `user_id` avoids one user’s key conflicting with another user’s key.

---

## 15. How do you make background jobs and webhooks idempotent?

> “Queues and webhook providers can deliver the same message more than once, so I assume duplicates will happen. I store the event ID or message ID with a unique constraint. If I have already processed it, I safely ignore it or return the previously stored outcome.”

Example: Stripe sends the same payment webhook twice. Store its event ID; process it only once.

---

## 16. Idempotency vs retry

> “A retry means ‘try the request again.’ Idempotency means ‘it is safe if the request is tried again.’ Retrying without idempotency can create duplicates. Idempotency is what makes retries safe.”

---

## 17. Idempotency vs deduplication

> “They are related, but not exactly the same. Idempotency is an API contract: repeating the same action gives the same result. Deduplication is the technical process of detecting and removing duplicates. Deduplication can be one way to implement idempotency.”

---

## 18. How would you test it?

> “I would send the same request twice with the same idempotency key and confirm that only one order or payment exists. I would also test concurrent requests, retries after a timeout, the same key with a changed body, and failure cases.”

Key checks:

* One key, same request → one database record.
* One key, different request → rejected.
* Two simultaneous requests → one operation only.
* Retry after server response failure → original result returned.

---

## 19. What observability would you add?

> “I would log the idempotency key, user ID, request ID, operation status, and original resource ID, such as payment ID. I would add metrics for duplicate requests, key conflicts, stuck processing records, and failed operations. This helps us investigate whether retries are caused by network issues, frontend bugs, or provider problems.”

Never log sensitive information such as passwords, tokens, or full payment details.

---

## 20. What goes wrong without idempotency?

> “The main risk is duplicate side effects: double charges, duplicate refunds, repeated transfers, multiple orders, duplicate emails, or processing the same webhook twice. These issues are expensive because they damage customer trust and often need manual support work.”

---

## 21. Which authentication endpoints need idempotency?

> “I would not blindly add idempotency keys to every authentication endpoint. I look at the side effect and make repeated calls safe.”

Examples:

* **Logout:** should be idempotent. Logging out twice should still leave the user logged out.
* **Registration:** prevent duplicate accounts with a unique email constraint. Repeating the request should not create two accounts.
* **Password-reset request:** make it safe to repeat, but rate-limit it. Always return a generic response so attackers cannot discover whether an email exists.
* **Password-reset confirmation:** the reset token should be one-time use. A retry should not repeatedly change the password.
* **Login:** usually does not need a normal idempotency key, but repeated requests should not create unnecessary sessions or security events.
* **Refresh token:** needs extra care. With token rotation, a retry may accidentally use an old token. Use a short retry grace period or carefully track token reuse.

## One strong final interview answer

> “I use idempotency where retries can create duplicate side effects. For example, payments, orders, transfers, webhooks, and background jobs. I normally use a client-generated idempotency key, store it with the request hash and final response, and enforce uniqueness in the database so concurrent requests cannot create duplicates. A retry with the same key returns the original result; the same key with a different payload is rejected. The main principle is simple: a network retry should never charge a user twice or create duplicate business data.”


---

# Natural idempotent methods vs you code being actually idempotent (2 diff things)

“Naturally idempotent” means the **intended HTTP meaning** of that method is safe to repeat. It does **not** guarantee your code is idempotent.

For example:

* `GET /users/1` is naturally idempotent: reading a user repeatedly does not change them.
* `PUT /users/1` with `{ name: "Arjun" }` is naturally idempotent: setting the name to “Arjun” ten times leaves the same final state.
* `DELETE /users/1` is intended to be idempotent: after the first delete, the user remains deleted.

But your implementation can break this:

```ts
// Bad: PATCH is not idempotent here.
// Each retry adds another €10.
balance += 10;
```

```ts
// Idempotent: repeating this keeps the same final balance.
balance = 10;
```

So, no: “naturally” does not mean zero code. You still need to implement the endpoint according to that behaviour.

For a `POST` that creates something important, use an idempotency key.

```ts
// POST /payments
async createPayment(userId: string, key: string, amount: number) {
  const existing = await idempotencyRepo.findOne({ userId, key });

  // A retry: return the result from the first request.
  if (existing?.status === 'completed') {
    return existing.response;
  }

  // DB must enforce UNIQUE(userId, key)
  const record = await idempotencyRepo.create({
    userId,
    key,
    status: 'processing',
  });

  const payment = await paymentRepo.create({ userId, amount });

  const response = { paymentId: payment.id, status: 'success' };

  await idempotencyRepo.update(record.id, {
    status: 'completed',
    response,
  });

  return response;
}
```

The important database rule:

```sql
UNIQUE (user_id, idempotency_key)
```

Simple flow:

1. Frontend generates a key when user clicks **Pay**.
2. It sends that key with the request.
3. Server stores it before creating the payment.
4. If the same request is retried with the same key, return the old result.
5. The unique database constraint stops two simultaneous requests from creating two payments.
