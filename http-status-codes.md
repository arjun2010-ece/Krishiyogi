Categories of HTTP Status Codes
-------------------------------

There are five categories of HTTP status codes:

-   **1XX (informational codes)**: The server received the request and is processing it
-   **2XX (success codes)**: The server successfully received and processed the request
-   **3XX (redirection codes)**:The server received the request, but there's a redirect to another destination ([301 or 302](https://www.semrush.com/blog/301-vs-302-redirect/) are common)
-   **4XX (client error codes)**:The requested resource couldn't be found or reached due to a client error
-   **5XX (server error codes)**: The server ran into an error when processing the request



Here are the HTTP status codes most commonly asked in backend interviews. You do not need to memorise every code—understand the **situation** in which you would use each one.

A simple way to remember the groups:

* **2xx** → request succeeded
* **4xx** → client sent something wrong
* **5xx** → server failed

## Success — 2xx

| Code             | Meaning                                | Typical backend use                                           |
| ---------------- | -------------------------------------- | ------------------------------------------------------------- |
| `200 OK`         | Request succeeded                      | Fetch data, update data, successful login                     |
| `201 Created`    | A new resource was created             | `POST /users`, `POST /orders`                                 |
| `202 Accepted`   | Accepted, but processing happens later | Video processing, email campaign, long-running background job |
| `204 No Content` | Succeeded, but no response body        | Successful delete or logout                                   |

Interview answer:

> “I use `200` for a normal successful response, `201` when a new resource was created, `202` when work is accepted for asynchronous processing, and `204` when the action succeeds but there is nothing useful to return.”

---

## Client errors — 4xx

| Code                        | Meaning                                                | Typical backend use                                                 |
| --------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------- |
| `400 Bad Request`           | Request is malformed or invalid                        | Invalid JSON, missing required query parameter                      |
| `401 Unauthorized`          | User is not authenticated                              | Missing, expired, or invalid access token                           |
| `403 Forbidden`             | User is authenticated but lacks permission             | Normal user tries to access admin endpoint                          |
| `404 Not Found`             | Resource or route does not exist                       | `GET /users/999` where user does not exist                          |
| `405 Method Not Allowed`    | Route exists, but HTTP method is unsupported           | Calling `POST /users/1` when only `GET` is allowed                  |
| `409 Conflict`              | Request conflicts with current data/state              | Duplicate email; same idempotency key used with a different payload |
| `422 Unprocessable Content` | Request format is valid, but business validation fails | Order quantity exceeds available stock; invalid state transition    |
| `429 Too Many Requests`     | Rate limit exceeded                                    | Too many login or password-reset attempts                           |

The most important distinction:

> “`401` means you are not logged in or your token is invalid. `403` means we know who you are, but you are not allowed to do this.”

`400` vs `422`:

> “I use `400` when the request itself is malformed, for example invalid JSON. I use `422` when the request is structurally valid but breaks a business rule, such as trying to order more stock than exists.”

Some teams use `400` for all validation errors. That is also common—be consistent in your API.

---

## Server errors — 5xx

| Code                        | Meaning                                                        | Typical backend use                                                |
| --------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------ |
| `500 Internal Server Error` | Unexpected server-side failure                                 | Unhandled exception, unexpected database error                     |
| `502 Bad Gateway`           | Gateway/proxy got an invalid response from an upstream service | Nginx/API gateway cannot get a valid response from another service |
| `503 Service Unavailable`   | Service is temporarily unavailable                             | Maintenance, overloaded service, dependency temporarily down       |
| `504 Gateway Timeout`       | Gateway waited too long for an upstream service                | API gateway times out waiting for another backend                  |

Interview answer:

> “I return `500` for unexpected errors. `502`, `503`, and `504` usually appear in distributed systems, where a gateway or service depends on another service. I log the real error internally, but return a safe, consistent error message to the client.”

---

## A very common REST endpoint example

| Endpoint               | Successful response | Common failures                  |
| ---------------------- | ------------------: | -------------------------------- |
| `GET /users/:id`       |               `200` | `401`, `404`                     |
| `POST /users`          |               `201` | `400`/`422`, `409`               |
| `POST /login`          |               `200` | `400`, `401`, `429`              |
| `PUT /users/:id`       |      `200` or `204` | `400`/`422`, `401`, `403`, `404` |
| `DELETE /users/:id`    |               `204` | `401`, `403`, `404`              |
| `POST /payments`       |      `201` or `200` | `400`/`422`, `409`, `402`, `503` |
| `POST /reports/export` |               `202` | `401`, `403`, `429`              |

One extra code sometimes asked for payments:

* `402 Payment Required` — historically reserved and not used consistently. Some payment APIs use it for payment-related failures, but do not assume it is standard behaviour. `422` or a provider-specific error is often clearer.

## Strong concise interview answer

> “I group status codes into success, client errors, and server errors. For success, I mainly use `200`, `201`, `202`, and `204`. For client errors, the most important are `400` for malformed requests, `401` for missing or invalid authentication, `403` for insufficient permission, `404` for missing resources, `409` for conflicts such as duplicate email or idempotency-key mismatch, `422` for business-rule validation, and `429` for rate limiting. For unexpected backend failures, I use `500`, while `502`, `503`, and `504` usually relate to gateway or dependency problems.”
