# Frontend testing and delivery related questions

Instead of memorising 90 separate answers, remember this simple flow:

**Test the right things → automate checks → release safely → watch production → learn and improve.**

Below are **12 core interview questions**. Together, they cover almost all the questions from the earlier list.

---

## 1. What is your overall frontend testing strategy?

**Easy interview answer:**

> I use different tests for different levels of risk.
>
> I write unit tests for small business rules and utility functions. I use integration tests for components working together, such as a form calling an API and showing success or error states. Then I use E2E tests only for the most important user journeys, like login, checkout, or creating an account.
>
> My goal is not to test every line of code. My goal is to have confidence that important user behaviour works, while keeping the test suite fast and maintainable.

### Remember it as: **Small → Connected → Real journey**

* **Unit test:** one small piece
* **Integration test:** pieces working together
* **E2E test:** real user journey in a browser

### Covers

Test pyramid, test strategy, unit vs integration vs E2E, coverage, critical journeys, avoiding too many E2E tests.

---

## 2. What makes a good test?

**Easy interview answer:**

> A good test is clear, stable, and focused on something meaningful to the user or the business. Someone reading it should quickly understand what behaviour is expected.
>
> I avoid testing internal implementation details, such as a specific state variable or which internal function was called. Those tests break during harmless refactoring. Instead, I test what the user sees and does: click a button, enter text, submit a form, and see the expected result.

### Remember it as: **Clear, useful, stable**

A test should:

* Clearly explain expected behaviour
* Test something that matters
* Stay stable when internal code is refactored

### Covers

Maintainable tests, implementation details, meaningful coverage, avoiding brittle tests.

---

## 3. How do you test a React component?

**Easy interview answer:**

> With React Testing Library, I test the component in a similar way to how a user uses it. I render the component, find elements by accessible roles or labels, interact with them, and check the visible result.
>
> For example, for a login form, I test that a user can enter an email and password, submit the form, see validation errors when needed, see a loading state during the request, and see either success or an API error afterwards.

### Simple pattern: **Render → Act → Check**

```ts
render(<LoginForm />);

await user.type(screen.getByLabelText(/email/i), "arjun@test.com");
await user.click(screen.getByRole("button", { name: /sign in/i }));

expect(await screen.findByText(/welcome/i)).toBeInTheDocument();
```

### Covers

React Testing Library, forms, loading/error/empty states, user events, selecting elements, `data-testid`.

---

## 4. Why do you prefer React Testing Library over testing component internals?

**Easy interview answer:**

> I prefer React Testing Library because it encourages me to test from the user’s point of view. A user does not know or care whether I use `useState`, Redux, Context, or a particular internal method. They care whether the screen works.
>
> This makes tests more realistic and less fragile. I can refactor the component internally without having to rewrite tests if the user-visible behaviour remains the same.

### Good sentence to remember

> “I test behaviour, not implementation.”

### Covers

Testing user behaviour, avoiding state/internal-method testing, refactoring confidence.

---

## 5. How do you test API calls and API-dependent components?

**Easy interview answer:**

> I normally use MSW, Mock Service Worker, to mock API responses at the network level. This is closer to real application behaviour than mocking `fetch` or Axios inside every test.
>
> I test the important server situations: successful response, loading, empty result, validation error, unauthorised response, server error, and sometimes slow network behaviour. That gives me confidence that the UI handles real-world situations properly.

### Remember API states as: **Loading → Success → Empty → Error**

For authentication, also add:

* **401:** user is not logged in or session expired
* **403:** user is logged in but does not have permission

### Covers

MSW, API mocking, `fetch`/Axios mocks, 200/401/403/404/500, loading/error states, retries, cancellation, auth flows.

---

## 6. What is the difference between a mock, spy, stub, and fake?

**Easy interview answer:**

> In daily frontend work, people sometimes use these words loosely, but the simple difference is:
>
> * A **mock** replaces a real dependency with controlled behaviour.
> * A **spy** watches whether a real function was called and with what arguments.
> * A **stub** returns fixed values so the test can continue.
> * A **fake** is a lightweight working version of something real, such as an in-memory database.
>
> I use them carefully. If I mock too much, I may only prove that my mocks work rather than proving that the real application behaviour works.

### Covers

Mocks, spies, stubs, fakes, what to mock, avoiding over-mocking.

---

## 7. How do you test async code, debouncing, timers, and custom hooks?

**Easy interview answer:**

> For async UI, I wait for the expected user-visible result instead of adding arbitrary delays. For example, I use `findBy...` or `waitFor` when the UI changes after an API response.
>
> For debounce, polling, or retry logic, I use fake timers so the test remains fast and predictable. For custom hooks, I test them through a small test component or a hook testing utility, checking the values and actions the hook exposes.

### Important senior point

> I avoid `setTimeout` in tests just to “wait and hope.” I wait for a meaningful condition instead.

### Covers

Promises, timers, debounce/throttle, retries, hooks, async UI, avoiding flaky waiting.

---

## 8. What should be covered by E2E tests?

**Easy interview answer:**

> I use E2E tests for a small number of high-value user journeys that cross many parts of the system. For example: signing in, completing onboarding, purchasing a product, or submitting an important form.
>
> I would not use E2E tests for every button or every small validation rule because they are slower and more expensive to maintain. Those are better covered by unit or integration tests.

### Remember it as: **E2E protects money, access, and critical workflows**

Typical examples:

* Login and logout
* Payment or checkout
* Registration
* Core dashboard workflow
* Permissions or role-based access
* Critical data creation/editing flow

### Covers

Playwright/Cypress, E2E scope, test data, login flows, third-party integrations, E2E frequency.

---

## 9. How do you prevent and fix flaky tests?

**Easy interview answer:**

> Flaky tests usually happen because a test depends on timing, shared data, network instability, animations, or a previous test leaving behind state.
>
> I make tests deterministic: I control API responses, create isolated test data, wait for visible conditions instead of fixed timeouts, and reset state between tests. In Playwright, I also use traces, screenshots, and videos to understand failures in CI.
>
> I do not simply keep retrying a flaky test forever. Retries can help temporarily, but I still find and fix the real cause.

### Remember the causes as: **Time, data, state, network**

### Covers

Flaky tests, fixed waits, CI-only failures, traces/screenshots/videos, retries, cleanup and isolation.

---

## 10. Describe a good frontend CI/CD pipeline.

**Easy interview answer:**

> On every pull request, I want fast feedback first: formatting, linting, TypeScript checks, unit and integration tests, then a production build. For important applications, I also create a preview deployment so QA, product, and design can test the exact changes before merge.
>
> After merge, the application goes to staging and then production through an automated pipeline. E2E tests can run on the preview or staging environment, depending on how long they take and how critical the product is.

### Easy order to remember

**Code quality → Tests → Build → Preview → Deploy → Monitor**

| Step                   | Why it exists                |
| ---------------------- | ---------------------------- |
| Lint and format        | Catch simple mistakes        |
| Type check             | Catch TypeScript problems    |
| Unit/integration tests | Check application behaviour  |
| Production build       | Ensure it can actually build |
| Preview deployment     | Let people review the change |
| E2E tests              | Check major user journeys    |
| Production deploy      | Release safely               |
| Monitoring             | Catch real production issues |

### Covers

CI vs CD, PR checks, pipeline ordering, build validation, preview deployments, staging and production.

---

## 11. How do you release safely and roll back if something goes wrong?

**Easy interview answer:**

> I prefer small releases and feature flags for risky changes. A feature flag lets us deploy the code but enable it only for internal users, a small percentage of users, or one customer first.
>
> If there is a serious problem, the fastest response is usually to disable the feature flag. If the problem affects the whole release, we roll back to the last known stable version. I also make sure we have monitoring and a clear ownership plan so issues are noticed and handled quickly.

### Remember it as: **Release small → Observe → Expand or roll back**

### Covers

Feature flags, gradual rollout, canary releases, rollback, failed deployment, release confidence.

---

## 12. What do you monitor after deployment?

**Easy interview answer:**

> After release, I check whether users are facing errors and whether the application is still fast and usable. I look at JavaScript errors, failed API requests, page performance, Core Web Vitals, and key business flows such as successful sign-ins or completed payments.
>
> Tools like Sentry or Bugsnag help us capture frontend errors with useful context. If an issue happens only in production, I use error details, source maps, browser/device data, logs, and release information to reproduce it and fix it safely.

### Remember it as: **Errors, speed, user outcome**

* **Errors:** JavaScript crashes, failed API requests
* **Speed:** LCP, INP, CLS, slow pages
* **User outcome:** login success, conversion, completed workflow

### Covers

Sentry/Bugsnag/Datadog, Core Web Vitals, source maps, production bugs, release monitoring, success metrics.

---

# Accessibility and visual testing: short answers

These are commonly asked as follow-ups.

### How do you test accessibility?

> I build accessibility into component tests from the beginning. I use semantic HTML first, then correct labels, keyboard support, focus management, and ARIA only where needed. I use automated checks such as axe or Storybook accessibility checks, but I also manually test keyboard navigation and screen-reader-relevant behaviour because automation cannot catch everything.

### How do you test visual regressions?

> For shared UI components, Storybook is useful because it shows components in isolated states. I can connect it to visual regression tools such as Chromatic, Percy, or Playwright screenshots. This helps catch unintended visual changes, but I still review meaningful differences because screenshots cannot tell whether a design change was intentional.

---

# One strong “real experience” answer you can adapt

> In my projects, I try to make quality part of normal development rather than leaving it only to QA. I write unit tests for business logic, React Testing Library tests for important component behaviour, and Playwright or Cypress tests for the main user journeys.
>
> In CI, each pull request runs linting, TypeScript checks, tests, and a production build. A preview environment helps QA, product, and design review changes. For safer releases, I use feature flags where appropriate, and after deployment I monitor frontend errors, API failures, and performance through tools such as Bugsnag or Sentry.
>
> The main idea is simple: catch cheap problems early, test critical user behaviour properly, and make releases easy to observe and reverse.

If you remember only one line, remember this:

> “I test behaviour at the right level, automate quality checks in CI, release gradually when risk is high, and monitor production after deployment.”


---

# Most commonly asked questions regarding frontend testing and delivery

Here are the most important Senior Frontend interview questions for **Frontend Testing & Delivery**, grouped so they are easier to prepare.

## 1. Testing strategy and test pyramid

1. What is your overall testing strategy for a frontend application?
2. How do you decide what should be covered by unit, integration, and E2E tests?
3. Explain the test pyramid in frontend development.
4. When would you write a unit test versus an integration test?
5. Why can having too many E2E tests become a problem?
6. How do you balance test coverage, delivery speed, and confidence?
7. What does “good test coverage” mean to you? Is 100% coverage the goal?
8. How do you test critical user journeys differently from small UI details?
9. How do you make testing part of development rather than something done at the end?
10. What kinds of frontend code are usually not worth testing directly?

## 2. Unit testing JavaScript and TypeScript

11. How do you test a JavaScript or TypeScript function?
12. What makes a unit test reliable and easy to maintain?
13. What should be mocked in a unit test, and what should not?
14. What is the difference between a mock, spy, stub, and fake?
15. How do you test functions that call APIs or other modules?
16. How do you test error handling and edge cases?
17. How do you test asynchronous code, promises, and timers?
18. How do you test a debounce or throttle function?
19. How do you test code that depends on `Date`, randomness, browser storage, or environment variables?
20. How do you avoid tests becoming tightly coupled to implementation details?

## 3. React component testing

21. How do you test a React component using React Testing Library?
22. Why is React Testing Library usually preferred over testing component internals?
23. What do you mean by “test the user behaviour, not implementation details”?
24. How do you test loading, success, empty, and error states?
25. How do you test a form: validation, submission, disabled state, and API errors?
26. How do you test a component that fetches data?
27. How do you test custom React hooks?
28. How do you test Context, Redux, Zustand, or TanStack Query-dependent components?
29. How do you test routing and navigation in React Router or Next.js?
30. How do you test modals, dropdowns, portals, and tooltips?
31. How do you test a component with delayed UI updates or debounced search?
32. How do you test accessibility in React components?
33. How do you choose good queries in React Testing Library: role, label, text, or test ID?
34. When is `data-testid` acceptable, and when should you avoid it?
35. How do you prevent flaky React tests?

## 4. API mocking and integration testing

36. How do you mock API requests in frontend tests?
37. Why might you use MSW instead of mocking `fetch` or Axios directly?
38. How do you test different server responses: 200, 401, 403, 404, 500, timeout?
39. How do you test retry logic, request cancellation, or race conditions?
40. How do you test authentication flows on the frontend?
41. How do you test optimistic updates and rollback when an API request fails?
42. How do you test caching behaviour with TanStack Query or another data library?
43. How do you make sure your frontend assumptions match the backend API contract?
44. Have you used contract testing? When is it useful?

## 5. End-to-end testing

45. What is E2E testing, and what should it cover?
46. Which E2E tools have you used: Playwright, Cypress, Selenium? Why?
47. How do you choose which user journeys deserve E2E tests?
48. How do you test login flows without making tests slow or insecure?
49. How do you manage test data for E2E tests?
50. How do you test third-party integrations such as payments, analytics, or OAuth?
51. How do you run E2E tests in CI?
52. How do you debug an E2E test that fails only in CI?
53. What causes flaky E2E tests, and how do you fix them?
54. How do you handle waiting in E2E tests without using arbitrary timeouts?
55. How do you use screenshots, traces, videos, and reports to investigate failures?
56. Do you run E2E tests on every pull request or only before release?

## 6. Accessibility and visual testing

57. How do you test accessibility in a frontend application?
58. What automated accessibility checks can tools catch, and what do they miss?
59. How do you use tools such as axe, Lighthouse, or Storybook accessibility checks?
60. How do you test keyboard navigation and focus management?
61. How do you test visual regressions?
62. Have you used Chromatic, Percy, Playwright screenshots, or similar tools?
63. What are the limitations of screenshot-based visual testing?
64. How can Storybook help with component testing and visual regression testing?

## 7. CI/CD and delivery pipeline

65. Describe the CI/CD pipeline for a frontend application you worked on.
66. What checks should run when a pull request is opened?
67. In what order would you run linting, type-checking, unit tests, build, and E2E tests?
68. What is the difference between CI and CD?
69. What is the difference between continuous delivery and continuous deployment?
70. How do you make a frontend CI pipeline fast enough for developers?
71. How do you cache dependencies and build artifacts in CI?
72. How do you handle environment variables and secrets securely in CI/CD?
73. How do you manage separate environments such as development, staging, and production?
74. How do you make sure the production build is actually tested before release?
75. How do you handle failed deployments?
76. How do you roll back a frontend release?
77. What is a feature flag, and how does it make delivery safer?
78. How do preview deployments help the product, QA, and design teams?
79. How do you version and release a shared component library or design system?
80. How do you deploy a microfrontend independently without breaking the shell application?

## 8. Quality, monitoring, and production confidence

81. What do you monitor after a frontend release?
82. How do you detect frontend errors in production?
83. Have you used tools such as Sentry, Bugsnag, Datadog, or LogRocket?
84. What metrics matter after deployment: errors, Core Web Vitals, conversion, API failures?
85. How do you investigate a production-only bug?
86. How do you use source maps safely in production?
87. How do you perform a safe gradual rollout?
88. How do you know whether a release was successful?
89. What would you do if a deployment causes a serious issue for users?
90. How do you create a culture where quality is owned by the whole team, not only QA?

For a senior interview, the highest-priority areas are:

* Choosing the right level of test: unit vs integration vs E2E
* React Testing Library and user-focused tests
* API mocking with MSW
* Playwright or Cypress for critical journeys
* Avoiding flaky tests
* CI pipeline, preview deployments, feature flags, rollback
* Monitoring errors and performance after release
* Accessibility and visual regression testing

---

# Mapping of 90 questions with blueprint 12 questions

Not completely in the sense of giving a separate, detailed answer to every one of the 90 questions.

The 12 questions **cover all 90 topics at a high level**, but a few specialised areas—such as **contract testing, component-library versioning, microfrontend delivery, accessibility, and visual regression**—need short follow-up answers too.

Here is the exact mapping.

| Core question                                      | Initial questions it covers |
| -------------------------------------------------- | --------------------------- |
| **1. Overall frontend testing strategy**           | **1–10**                    |
| **2. What makes a good test?**                     | **11–20**                   |
| **3. How do you test a React component?**          | **21, 24–35**               |
| **4. Why React Testing Library / user behaviour?** | **22–23**                   |
| **5. API calls and API-dependent components**      | **36–44**                   |
| **6. Mock vs spy vs stub vs fake**                 | **13, 15, 36**              |
| **7. Async code, debounce, timers, and hooks**     | **17–19, 27, 31, 39**       |
| **8. What should E2E tests cover?**                | **45–56**                   |
| **9. Preventing flaky tests**                      | **34, 52–55**               |
| **10. Frontend CI/CD pipeline**                    | **51, 56, 65–74, 78**       |
| **11. Safe releases and rollback**                 | **75–80, 87–89**            |
| **12. Monitoring after deployment**                | **81–90**                   |
| **Accessibility and visual-testing follow-ups**    | **32, 57–64**               |

Here is the same mapping against the original list, in more detail.

## 1. Overall frontend testing strategy

Covers:

* **1.** Overall frontend testing strategy
* **2.** Choosing unit, integration, and E2E tests
* **3.** Test pyramid
* **4.** Unit versus integration testing
* **5.** Why too many E2E tests are a problem
* **6.** Coverage versus speed versus confidence
* **7.** Meaning of good test coverage
* **8.** Testing critical journeys differently
* **9.** Making testing part of development
* **10.** What not to test directly

## 2. What makes a good test?

Covers:

* **11.** Testing a JS/TS function
* **12.** Reliable, maintainable tests
* **13.** What to mock and what not to mock
* **14.** Mock, spy, stub, fake
* **15.** Testing functions that call APIs/modules
* **16.** Error handling and edge cases
* **17.** Async code, promises, timers
* **18.** Debounce or throttle
* **19.** Date, randomness, storage, environment variables
* **20.** Avoiding implementation-detail tests

Questions 13, 14, 15, 17–19 are then explained more deeply in questions 5–7.

## 3. How do you test a React component?

Covers:

* **21.** React Testing Library component testing
* **24.** Loading, success, empty, and error states
* **25.** Form validation, submission, disabled state, API errors
* **26.** Components that fetch data
* **27.** Custom hooks
* **28.** Context, Redux, Zustand, TanStack Query
* **29.** Routing and navigation
* **30.** Modals, dropdowns, portals, tooltips
* **31.** Delayed updates and debounced search
* **32.** Accessibility testing in React
* **33.** Role, label, text, and test IDs
* **34.** When to use `data-testid`
* **35.** Preventing flaky React tests

## 4. Why React Testing Library / user behaviour?

Covers:

* **22.** Why React Testing Library is preferred
* **23.** “Test user behaviour, not implementation details”

This is a very common follow-up to question 3.

## 5. API calls and API-dependent components

Covers:

* **36.** Mocking API requests
* **37.** MSW versus mocking `fetch` or Axios
* **38.** Testing API responses: success, auth errors, server errors
* **39.** Retry logic, cancellation, race conditions
* **40.** Authentication flows
* **41.** Optimistic update and rollback
* **42.** TanStack Query caching behaviour
* **43.** Frontend/backend API agreement
* **44.** Contract testing

For your background, you can say you would use **MSW** in tests and have clear API contracts through OpenAPI/Swagger or backend/frontend alignment. Do not claim contract testing experience unless you genuinely used it.

## 6. Mock vs spy vs stub vs fake

Covers:

* **13.** What to mock
* **14.** Difference between mock, spy, stub, fake
* **15.** Testing calls to APIs/modules
* **36.** API mocking, as a practical use case

## 7. Async code, debounce, timers, and hooks

Covers:

* **17.** Promises and timers
* **18.** Debounce/throttle
* **19.** Date/randomness/storage/env variables
* **27.** Custom hooks
* **31.** Debounced UI updates
* **39.** Retry/cancellation/race conditions

## 8. What should E2E tests cover?

Covers:

* **45.** Meaning and scope of E2E testing
* **46.** Playwright, Cypress, Selenium
* **47.** Which journeys deserve E2E tests
* **48.** Login flows
* **49.** E2E test data
* **50.** Third-party integrations
* **51.** Running E2E tests in CI
* **52.** CI-only E2E failures
* **53.** Flaky E2E tests
* **54.** Avoiding arbitrary waits
* **55.** Screenshots, traces, videos, reports
* **56.** When E2E tests run

## 9. Preventing flaky tests

Covers:

* **34.** Stable selectors and appropriate `data-testid` use
* **35.** Preventing flaky React tests
* **52.** Debugging CI-only E2E failures
* **53.** Causes and fixes for flaky tests
* **54.** Waiting correctly in E2E tests
* **55.** Debug artefacts such as traces and screenshots

## 10. Frontend CI/CD pipeline

Covers:

* **51.** E2E tests in CI
* **56.** E2E timing: PR, merge, nightly, pre-release
* **65.** Describing a CI/CD pipeline
* **66.** Pull-request checks
* **67.** Correct check order
* **68.** CI versus CD
* **69.** Continuous delivery versus continuous deployment
* **70.** Making CI faster
* **71.** Dependency/build caching
* **72.** Secrets and environment variables
* **73.** Development, staging, production environments
* **74.** Testing the production build
* **78.** Preview deployments

## 11. Safe releases and rollback

Covers:

* **75.** Failed deployments
* **76.** Rollback
* **77.** Feature flags
* **79.** Versioning/releasing a component library
* **80.** Independently deploying microfrontends
* **87.** Gradual rollout
* **88.** Knowing whether a release succeeded
* **89.** Serious production issues

Questions **79 and 80** are the two least directly covered by the original 12 answers. They deserve their own short preparation because they are architecture/delivery topics.

## 12. Monitoring after deployment

Covers:

* **81.** What to monitor
* **82.** Detecting frontend production errors
* **83.** Sentry, Bugsnag, Datadog, LogRocket
* **84.** Errors, Core Web Vitals, conversion, API failures
* **85.** Production-only bugs
* **86.** Safe source maps
* **87.** Gradual rollout
* **88.** Release success
* **89.** Major release incident
* **90.** Shared ownership of quality

## Accessibility and visual testing follow-ups

Covers:

* **32.** Accessibility in React components
* **57.** Accessibility testing approach
* **58.** What automated accessibility tools miss
* **59.** axe, Lighthouse, Storybook accessibility tools
* **60.** Keyboard navigation and focus management
* **61.** Visual regression testing
* **62.** Chromatic, Percy, Playwright screenshots
* **63.** Limits of screenshot testing
* **64.** Storybook for component and visual testing

So the accurate conclusion is:

* **The 12 questions are enough to understand and answer the whole category in a senior interview.**
* To cover the original 90 **more completely**, prepare these five focused follow-ups separately:

1. Why MSW, and how do you test API states?
2. How do you prevent flaky Playwright/Cypress tests?
3. How do you test accessibility beyond automated tools?
4. How do you version and release a shared component library?
5. How do you safely deploy and roll back a microfrontend?

Those five are the main gaps that can become deeper interview discussion.

---

# Missing popular questions and answers

A few questions overlap, so I’ll group them. This is the easier way to remember them in an interview.

# 1. Why use MSW, and how do you test API states?

## Why use MSW?

**Easy interview answer:**

> I prefer MSW, Mock Service Worker, because it intercepts requests at the network level. My component still makes a normal `fetch` or Axios request, but MSW returns a controlled fake server response.
>
> This is closer to real application behaviour than mocking Axios or `fetch` directly inside every test. It also keeps tests cleaner and lets the same API mock be reused across component tests, Storybook, and sometimes E2E-like local testing.

### Simple comparison

| Directly mocking Axios/fetch             | MSW                                      |
| ---------------------------------------- | ---------------------------------------- |
| Tests internal implementation            | Tests the request/response behaviour     |
| Can break if you switch Axios to `fetch` | Usually stays stable after that refactor |
| Mock setup often repeated per test       | Reusable request handlers                |
| Can feel less realistic                  | Closer to how the app talks to a server  |

### How do you test API states?

**Easy interview answer:**

> For any screen that fetches data, I test the important states a real user can see: loading, success, empty data, and error. For protected APIs, I also test unauthorised and forbidden responses.
>
> I do not only test the happy path, because users often experience slow connections, expired sessions, or server errors.

### Pattern to remember: **Loading → Success → Empty → Error**

For example, for a “Users” page:

* **Loading:** show spinner or “Loading users…”
* **Success:** show user list
* **Empty:** show “No users found”
* **Error:** show helpful error message and retry button
* **401:** redirect to sign-in or refresh session
* **403:** show “You do not have permission”
* **500:** show generic retryable server error

```ts
// MSW handler for a successful response
http.get("/api/users", () => {
  return HttpResponse.json([{ id: "1", name: "Arjun" }]);
});

// Override only for one error test
server.use(
  http.get("/api/users", () => {
    return new HttpResponse(null, { status: 500 });
  }),
);
```

Then the component test checks what the user sees:

```ts
render(<UsersPage />);

expect(screen.getByText(/loading users/i)).toBeInTheDocument();

expect(await screen.findByText("Arjun")).toBeInTheDocument();
```

---

# 2. How do you test TanStack Query caching?

**Easy interview answer:**

> I test caching at the behaviour level. I do not test TanStack Query’s internal implementation. I check that when a component asks for the same query again within its configured stale time, it uses cached data rather than making another request.
>
> I also test that invalidating a query or performing a successful mutation causes the data to refresh when needed.

### Think of it in three situations

1. **First visit:** API request happens and data is cached.
2. **Quick revisit:** cached data is reused; no unnecessary request.
3. **Data changes:** invalidate or update the cache so the UI does not show stale information.

```ts
const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false, staleTime: 60_000 },
  },
});
```

For the test, you can use an MSW handler or a mock request counter and check that mounting the same query again does not cause a second request while the data is fresh.

### Senior-level detail

> In tests, I create a new `QueryClient` for each test. Otherwise cache from one test can leak into another test and cause confusing failures.

Also remember:

* `staleTime`: how long data is considered fresh
* `gcTime` (previously `cacheTime`): how long unused cached data remains in memory
* `invalidateQueries`: marks data as stale so it can refetch

---

# 3. How do you prevent flaky Playwright/Cypress tests?

**Easy interview answer:**

> Flaky E2E tests usually depend on timing, shared data, unstable environments, or selectors that change easily. I make tests deterministic: I use reliable selectors, isolated test data, controlled network responses where appropriate, and I wait for meaningful UI conditions rather than fixed delays.
>
> If a test fails, I investigate the root cause instead of permanently hiding it behind retries.

### Remember the main causes: **Time, data, state, environment**

| Cause                       | Better approach                                                        |
| --------------------------- | ---------------------------------------------------------------------- |
| Fixed `wait(2000)`          | Wait for an element, API response, URL, or loading state to finish     |
| Shared test user/data       | Create unique data per test or reset data before each run              |
| One test depends on another | Every test should set up its own required state                        |
| Fragile CSS selector        | Prefer accessible roles, labels, or stable `data-testid`               |
| Animation/loading race      | Disable non-essential animations in test mode; wait for final UI state |
| Real third-party system     | Mock or use a stable sandbox/test environment                          |
| CI is slower than local     | Use Playwright/Cypress auto-waiting and inspect CI artefacts           |

### Good sentence to remember

> “A reliable E2E test waits for a condition, not for a number of milliseconds.”

---

# 4. How do you handle waiting in E2E tests without arbitrary timeouts?

**Easy interview answer:**

> I avoid arbitrary waits such as `waitForTimeout(2000)`, because they make tests slower and still unreliable. Instead, I wait for something meaningful: a button becoming enabled, a loading indicator disappearing, a URL changing, an API response finishing, or the expected text becoming visible.

### Playwright examples

```ts
await page.getByRole("button", { name: "Save" }).click();

await expect(page.getByText("Profile saved")).toBeVisible();
```

```ts
await page.waitForURL("**/dashboard");
```

```ts
await expect(page.getByTestId("loading-spinner")).toBeHidden();
```

Cypress works in a similar way because its commands automatically retry until the expected condition is true or the configured timeout is reached.

---

# 5. How do you run E2E tests in CI?

**Easy interview answer:**

> I run fast checks on every pull request: linting, type checking, unit tests, component/integration tests, and a production build. For E2E, the exact strategy depends on how long the suite takes and how critical the product is.
>
> Usually, I run a small smoke suite on every pull request or preview deployment, the full suite after merge to staging, and optionally a scheduled nightly run. Before an important release, the critical journeys must pass.

### Good practical approach

| When                   | What to run                                           |
| ---------------------- | ----------------------------------------------------- |
| Every pull request     | Fast smoke E2E tests for login and main workflow      |
| Preview environment    | Key changed-area E2E tests                            |
| After merge to staging | Full E2E suite                                        |
| Nightly                | Broader regression suite, multiple browsers if needed |
| Before major release   | All critical flows                                    |

### Why not run every E2E test on every pull request?

> A full suite can make feedback slow and expensive. I prioritise fast feedback on PRs, while still ensuring full coverage before release. The exact balance depends on the risk and size of the application.

---

# 6. How do you debug a Playwright/Cypress test that fails only in CI?

**Easy interview answer:**

> First, I do not assume it is only a CI problem. CI often reveals a timing, data, or environment issue that my local machine happens to hide.
>
> I inspect the failure artefacts: screenshots, videos, browser console logs, network logs, and especially Playwright traces. Then I compare environment variables, browser version, test data, API availability, timing, and parallel execution between local and CI.

### Debugging order to remember

**What did the user see? → What did the browser do? → What did the server return?**

1. **Screenshot/video**
   Did the screen look wrong? Was a modal covering the button? Did loading never finish?

2. **Trace**
   In Playwright Trace Viewer, inspect each action, DOM state, network request, and timing.

3. **Console and network logs**
   Did the browser throw an error? Did the API return 401, 500, or wrong data?

4. **Test data and state**
   Was another parallel test using the same account or record?

5. **CI configuration**
   Is a required secret or environment variable missing? Is CI using a different browser or base URL?

### Playwright example

```ts
use: {
  trace: "on-first-retry",
  screenshot: "only-on-failure",
  video: "retain-on-failure",
}
```

### Strong senior statement

> “Retries are useful for collecting evidence and keeping a pipeline moving temporarily, but they are not the real fix for a flaky test.”

---

# 7. How do you use screenshots, traces, videos, and reports?

**Easy interview answer:**

> I use them as evidence rather than guessing why a test failed. A screenshot shows the final page state. A video shows the whole user journey. A trace is especially useful in Playwright because it lets me inspect each action, DOM snapshot, network request, console output, and timing.
>
> In CI, I upload these artefacts when tests fail so developers can diagnose issues without first trying to reproduce everything locally.

### When each is useful

| Tool                 | Best for                                 |
| -------------------- | ---------------------------------------- |
| Screenshot           | What the UI looked like at failure       |
| Video                | What happened over the full test journey |
| Trace                | Exact step, DOM state, requests, timing  |
| HTML report          | Seeing patterns across test runs         |
| Console/network logs | JavaScript or backend/API problems       |

---

# 8. How do you test accessibility beyond automated tools?

**Easy interview answer:**

> Automated tools such as axe are useful and should run in CI, but they cannot tell us whether the experience is actually understandable and usable. I also test keyboard navigation, focus order, focus visibility, screen-reader labels, error announcements, and interactive components such as modals and menus.
>
> For important journeys, I manually test with keyboard-only navigation and, when possible, a screen reader. I also involve accessibility specialists or real users when the product has a high accessibility requirement.

### Remember: **Structure → Keyboard → Focus → Meaning**

1. **Structure**
   Use semantic HTML: buttons, links, headings, forms, labels.

2. **Keyboard**
   Can users navigate and operate everything using Tab, Enter, Space, and Escape?

3. **Focus**
   Is focus visible? Does it move correctly into and out of a modal? Does it return to the trigger when the modal closes?

4. **Meaning**
   Do labels, error messages, page titles, and status updates make sense to a screen-reader user?

### Important example: modal

For a modal, test that:

* Focus moves inside it when opened.
* Tab stays within the modal.
* Escape closes it, if appropriate.
* Focus returns to the button that opened it.
* The background cannot accidentally receive keyboard focus.

### What automation misses

Automated tools can detect many invalid ARIA attributes or missing labels, but they cannot reliably judge whether:

* Button wording is understandable
* Focus order is logical
* Error messaging is clear
* A keyboard flow feels usable
* Screen-reader announcements happen at the right moment

---

# 9. How do you version and release a shared component library?

**Easy interview answer:**

> I treat a shared component library like a product used by other engineering teams. It needs clear ownership, documentation, automated tests, visual regression checks, and a predictable release process.
>
> I use semantic versioning: patch releases for fixes, minor releases for backward-compatible features, and major releases for breaking changes. Each release has release notes and a migration guide when needed.

### Semantic versioning: easy version

| Version       | Meaning                     | Example                        |
| ------------- | --------------------------- | ------------------------------ |
| `1.0.1` patch | Bug fix, no breaking change | Fix button focus style         |
| `1.1.0` minor | New compatible feature      | Add a new Button variant       |
| `2.0.0` major | Breaking change             | Rename/remove a component prop |

### Release process

> A typical process is: create or update the component, add unit and accessibility tests, add Storybook stories for each important state, run visual regression checks, get design review if needed, then publish the package through CI. Consumer applications can upgrade using the versioned package and follow release notes.

### Good senior detail

> I try to deprecate before removing. For example, I mark an old prop as deprecated, document the replacement, give teams time to migrate, then remove it in the next major version.

This avoids suddenly breaking many applications.

---

# 10. How do you safely deploy and roll back a microfrontend?

**Easy interview answer:**

> Each microfrontend should have its own CI/CD pipeline, tests, and versioned deployment artefact. That allows a team to deploy one microfrontend without redeploying the whole application.
>
> However, independent deployment needs a clear compatibility contract with the shell: shared dependency rules, route ownership, authentication expectations, design-system versions, and a way for the shell to know which version to load.

### Safe deployment flow

1. Build and test the microfrontend in its own pipeline.
2. Publish a **versioned immutable artefact**, usually to a CDN.
3. Test it through a preview or staging environment.
4. Update a deployment manifest/configuration to point the shell to the new version.
5. Roll out gradually if the change is risky.
6. Monitor errors and user impact.
7. If needed, change the manifest back to the previous known-good version.

### Why a manifest helps

> The shell can load `checkout@2.4.0` today and return to `checkout@2.3.4` quickly if version 2.4.0 causes a problem. That rollback does not require rebuilding every other microfrontend.

### Important compatibility practices

* Use agreed public APIs/contracts between shell and microfrontends.
* Avoid casually changing shared dependency versions.
* Make backward-compatible changes where possible.
* Keep old versions available long enough for rollback.
* Use feature flags for risky functionality.
* Monitor errors per microfrontend and per release version.

---

# 11. What is continuous delivery versus continuous deployment?

**Easy interview answer:**

> Both mean that every change goes through automated checks and is kept in a releasable state. The difference is the final production step.
>
> With **continuous delivery**, the code is ready to release automatically, but a person or business decision triggers the production deployment.
>
> With **continuous deployment**, every change that passes all checks is automatically deployed to production without manual approval.

| Approach               | Production release                                      |
| ---------------------- | ------------------------------------------------------- |
| Continuous integration | Code is merged and tested frequently                    |
| Continuous delivery    | Production-ready automatically; manual release decision |
| Continuous deployment  | Automatically released to production after checks pass  |

### Practical answer for most companies

> Many teams use continuous delivery rather than full continuous deployment, especially when they have regulatory requirements, major customer risk, or want a business approval step. Feature flags can still let them deploy code frequently while controlling when users see it.
