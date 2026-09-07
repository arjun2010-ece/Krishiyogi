# Popular Frontend architecture, scalibility and performance questions
Answers are easy to memorise and revise also, we can add few more in this list.

---

## First, use this simple pattern for most answers

When they ask an architecture or performance question, think:

> “What is the problem? How would I find the real cause? What is the simplest safe fix? How would I check that it worked?”

That alone makes your answer structured and senior.

---

## 1. How would you structure a large frontend application?

> “I usually organise the code by feature. So instead of having one big folder for all components, one for all API calls, and one for all hooks, I keep related things together.
>
> For example, a `payments` feature would contain its own pages, components, API calls, hooks, types, and tests. This makes it easier for a developer to understand and change one area without touching unrelated code.
>
> Then I keep only genuinely common things in shared folders—for example buttons, inputs, common layout components, the API client, and utility functions.
>
> The main goal is simple: each feature should be easy to find, easy to own, and safe to change.”

**Remember:** Keep related code together. Share only what is actually shared.

---

## 2. What should go into a design system or shared component library?

> “I would put common UI building blocks in the design system: buttons, inputs, dropdowns, modals, typography, colours, spacing, and accessibility behaviour.
>
> But I would not put business-specific components there. For example, a reusable `Button` belongs in the design system, but a `CryptoStakingSummary` or `CheckoutTotal` should stay inside its own feature.
>
> I also would not make a component shared too early. First I would see the same pattern used in a few places. Then I would extract it carefully.”

**Remember:** Shared UI is good. Shared business logic usually becomes confusing.

---

## 3. How do you manage state in a large React app?

> “I first ask: is this data coming from the backend, or is it only UI state?
>
> If it comes from the backend—for example user data, transactions, or products—I use TanStack Query. It handles fetching, caching, loading states, retries, and refreshing data.
>
> If it is local UI state—for example whether a modal is open, an input value, or a selected tab—I keep it inside the component where possible.
>
> I use Context for things that are needed almost everywhere, such as the logged-in user, theme, or language. I would use Zustand or Redux only when several distant parts of the app need to share and update the same client-side state.”

**Remember:**

* Backend data → TanStack Query
* Small UI state → component state
* App-wide stable data → Context
* Complex shared UI state → Zustand/Redux

---

## 4. How do you keep components separate from API logic?

> “I try not to make UI components call backend URLs directly. A component should mainly focus on showing information and responding to user actions.
>
> I normally use a hook or service in between. For example, a `useUserProfile` hook can fetch and update user data, while the `UserProfile` component only displays it.
>
> I also keep common network setup in one API client—for example the base URL, auth token, error handling, and request timeout. This avoids repeating the same logic in every feature.”

**Remember:** Component shows UI. Hook handles feature logic. API client handles network details.

---

## 5. How do you handle authentication and permissions?

> “On the frontend, I handle the user experience: showing the right screens, redirecting an unauthenticated user to sign in, and hiding actions they cannot use.
>
> But I would never rely on the frontend for real security. A user can change frontend code in their browser, so the backend must always check whether they are allowed to perform an action.
>
> So the frontend improves the experience, while the backend protects the data.”

**Remember:** Frontend hides; backend protects.

---

## 6. How do you make a frontend scalable for many developers?

> “For me, frontend scalability is not only about handling more users. It also means that more developers can work on the product without constantly blocking each other.
>
> I would make ownership clear: for example, one team owns payments and another team owns the dashboard. I would also agree on shared standards for TypeScript, testing, accessibility, code review, error handling, and the design system.
>
> This gives teams freedom to work in their areas, but the product still feels consistent to the user.”

**Remember:** Clear ownership + shared standards.

---

## 7. How would you migrate a legacy frontend safely?

> “I would avoid rewriting everything at once. Big rewrites take a long time, create risk, and often stop feature delivery.
>
> Instead, I would improve the application step by step. For example, new files can be written in TypeScript first, then important old areas can be migrated gradually.
>
> Before replacing something, I would make sure the current behaviour is understood and covered by tests where it matters. Once the new version is stable, we can remove the old code.
>
> This lets the business continue moving while the technical debt is reduced.”

**Remember:** Improve gradually; do not stop the whole product for a rewrite.

---

## 8. When would you use microfrontends?

> “I would not use microfrontends just because an application is large. They add complexity.
>
> I would consider them when different teams own separate parts of a product and need to release independently—for example, one team owns checkout and another owns account management.
>
> If we use microfrontends, we still need shared rules for things like login, routing, error tracking, the design system, and dependency versions. Otherwise, the product can start feeling like several unrelated websites.
>
> If teams release together and work closely, I would usually prefer one well-organised frontend application because it is simpler.”

**Remember:** Microfrontends solve an organisational problem, not just a code problem.

---

## 9. A page is slow to load. What would you do?

> “I would not start by randomly adding lazy loading or memoisation. First, I would measure the problem.
>
> I would use browser tools and Lighthouse to check whether the main issue is large JavaScript files, slow API calls, large images, fonts, third-party scripts, or too much work happening in the browser.
>
> Then I would fix the biggest issue first. For example, if images are the problem, I would optimise and correctly size them. If JavaScript is large, I would split the code so users download only what they need for that page.
>
> After the change, I would compare the before-and-after numbers and monitor real users in production.”

**Remember:** Measure first. Fix the biggest bottleneck. Check the result.

---

## 10. How do you explain Core Web Vitals simply?

> “I think of Core Web Vitals as three user feelings:
>
> LCP is: ‘Can I see the main content quickly?’
> INP is: ‘Does the page react quickly when I click or type?’
> CLS is: ‘Does the page jump around while it is loading?’
>
> For LCP, I focus on the main image or main content and reduce things that block it.
>
> For INP, I look for heavy JavaScript or expensive updates after a user action.
>
> For CLS, I make sure images and dynamic content have reserved space, so the layout does not shift.”

| Metric | Simple meaning               |
| ------ | ---------------------------- |
| LCP    | Main content appears quickly |
| INP    | Page reacts quickly          |
| CLS    | Page does not jump around    |

---

## 11. How do you fix unnecessary React re-renders?

> “First, I would check whether re-renders are actually causing a user-visible problem. React re-rendering is normal; it is only a problem when it becomes expensive.
>
> I would use React DevTools Profiler to see which component is rendering often and why.
>
> A common fix is moving state closer to the components that need it. For example, if only one small filter panel needs a value, I would not store it at the top of the entire page.
>
> If profiling shows that an expensive child component keeps rendering with unchanged props, then I might use `React.memo`. I use `useMemo` for an expensive calculation and `useCallback` when a stable function reference is genuinely needed.”

**Remember:** Do not optimise blindly. Find the re-render, then fix its cause.

---

## 12. How do you optimise large tables or lists?

> “If a page renders thousands of rows at once, the browser has too much work to do. I would use virtualization, meaning only the rows currently visible on screen are rendered.
>
> I would also paginate data from the API instead of downloading everything at once. For tables with filtering or sorting, I would debounce user input where needed and avoid recalculating large data on every keystroke.
>
> For dashboards, I would update only the part that changed rather than re-rendering the whole page.”

**Remember:** Do not render or fetch what the user cannot see yet.

---

## 13. How do you make search and data fetching feel fast?

> “For a search box, I would debounce the input, so we do not send an API request for every single key press.
>
> I would cache recent results, reuse an identical request if it is already running, and cancel or ignore older requests when the user has typed something new.
>
> That last point matters because a slow old request can otherwise return after the latest request and show incorrect results.
>
> For large lists, I would use pagination or infinite scrolling instead of requesting everything at once.”

**Remember:** Debounce, cache, reuse, latest result wins.

---

## 14. How do you prevent performance problems from returning?

> “After fixing a performance issue, I would make it measurable. For example, I would add real-user monitoring for Core Web Vitals, set bundle-size limits in CI, and review performance-sensitive changes during code review.
>
> The aim is not only to make the page faster today. It is to make it difficult for the same problem to quietly return after a few releases.”

**Remember:** Fix it once, then add a guardrail.

---

# Two natural closing lines for interviews

For architecture:

> “I try to keep the system simple at first, make boundaries clear, and only add more structure when the product and team genuinely need it.”

For performance:

> “I prefer evidence over assumptions: measure the user problem, fix the biggest cause, verify the improvement, and prevent regression.”


Yes—**the 14 answers cover almost all 45 questions**, because many of those questions are different versions of the same core topic.

| Original question area                                           | Covered by |
| ---------------------------------------------------------------- | ---------- |
| App structure, folder structure, boundaries, shared code         | 1          |
| Design system, shared components, consistency                    | 2          |
| Local/global/server state, Context, Redux/Zustand, Query         | 3          |
| API layer, auth, RBAC, errors, analytics, config                 | 4–5        |
| Teams, ownership, standards, monorepo                            | 6          |
| Legacy migration, JS → TS, refactoring                           | 7          |
| Microfrontends, independent releases, versioning                 | 8          |
| Slow initial load, bundles, images, SSR/SSG/ISR, Core Web Vitals | 9–10       |
| React re-renders, memoisation, expensive UI work                 | 11         |
| Large lists, tables, dashboards, Web Workers                     | 12         |
| Search, caching, pagination, deduplication, races, retries       | 13         |
| Monitoring, performance budgets, preventing regressions          | 14         |

A few original questions are only mentioned briefly and are worth remembering as short add-ons:

* **Feature flags:** “I use feature flags to release risky changes gradually, test with a small audience, and roll back without redeploying.”
* **Memory leaks:** “I check for uncleaned timers, event listeners, subscriptions, WebSockets, and requests that continue after a component unmounts.”
* **Web Workers:** “I use them for heavy CPU work, such as processing a large file or complex calculation, so the browser UI does not freeze.”
* **SSR vs SSG vs ISR:** “I choose based on how often content changes: SSG for mostly static pages, ISR for pages that can refresh periodically, SSR for request-specific content, and client rendering for highly interactive private areas.”

So yes: learn the **14 answers as your foundation**, then keep these four short add-ons ready for follow-up questions.




---
# List of actual questions


Here are the most important Senior Frontend interview questions in this area. These are especially common for React/TypeScript roles.

### Frontend architecture

1. How would you structure a large React application so it stays maintainable as teams and features grow?

2. How do you decide between feature-based folders, layer-based folders, or domain-driven modules?

3. What belongs in a shared component library/design system, and what should remain feature-specific?

4. How do you prevent a shared component library from becoming too generic or difficult to change?

5. How would you design state management for a large application? When would you use local state, Context, Redux/Zustand, and TanStack Query?

6. What is the difference between client state and server state, and why should they be managed differently?

7. How do you handle cross-cutting concerns such as authentication, permissions, error handling, analytics, feature flags, and logging?

8. How do you design a frontend API layer so UI components are not tightly coupled to backend endpoints?

9. How would you architect role-based access control in a frontend application? What must still be enforced on the backend?

10. How do you handle configuration across local, staging, and production environments?

11. How would you introduce a new frontend framework, design system, or major architectural change into an existing application?

12. When would microfrontends be appropriate, and when would you avoid them?

13. If using microfrontends, how would you handle shared dependencies, routing, authentication, communication, versioning, and deployments?

14. How do you avoid circular dependencies and “shared utils” folders becoming a dumping ground?

15. How do you make frontend architectural decisions consistent across several teams?

### Scalability

16. What does “scalable frontend architecture” mean to you beyond handling more users?

17. How would you scale a frontend codebase maintained by many engineers working in parallel?

18. How do you define ownership boundaries between teams in a large frontend application?

19. How do you make independent deployments safe for multiple frontend teams?

20. How do you handle backward compatibility when frontend and backend are released independently?

21. How would you migrate a legacy JavaScript/React application to TypeScript incrementally?

22. How do you safely break a large component or monolith frontend into smaller modules?

23. How do feature flags support safe releases and gradual migrations?

24. How do you ensure consistency in accessibility, styling, testing, and error handling across a large product?

25. How would you manage and version a design system used by multiple applications?

### Performance

26. A web app has a slow initial load. How would you diagnose and improve it?

27. Which Core Web Vitals matter most—LCP, INP, and CLS—and what usually causes each to be poor?

28. How do you identify whether a performance problem is caused by JavaScript, rendering, network requests, images, or third-party scripts?

29. How do you reduce JavaScript bundle size?

30. Explain code splitting, lazy loading, dynamic imports, and route-based chunking. When can they make UX worse?

31. When should you use SSR, SSG, ISR, or client-side rendering?

32. How do you optimize images, fonts, and other static assets for performance?

33. How do you prevent unnecessary React re-renders?

34. When should you use `React.memo`, `useMemo`, and `useCallback`—and when should you not?

35. How would you diagnose a React component that renders too often?

36. How do long lists affect performance, and when would you use virtualization?

37. How do you optimize a dashboard with many charts, tables, filters, and frequent live updates?

38. How do you prevent expensive computations from blocking the UI?

39. When would you use Web Workers, and what are their limitations?

40. How do you optimize API fetching: caching, request deduplication, pagination, prefetching, cancellation, and retries?

41. How do you handle a search input that triggers API calls efficiently?

42. How do you avoid race conditions when multiple requests are in flight?

43. How do you measure real-user performance in production rather than relying only on Lighthouse?

44. How do you set performance budgets and stop performance regressions in CI/CD?

45. What are common causes of memory leaks in React applications, and how do you find them?

### Strong scenario questions

These are particularly likely at Senior level:

* “Our React dashboard becomes slow after users leave it open for an hour. How would you investigate?”
* “Initial load is 6 seconds on mobile. Give us your diagnosis and improvement plan.”
* “We have ten teams working in one frontend repository. How would you organize it?”
* “Our shared component library is slowing teams down. What would you change?”
* “A page re-renders every time a user types in an unrelated input. How do you debug it?”
* “We need to migrate from a legacy frontend to React/TypeScript without stopping feature delivery. What is your strategy?”
* “The backend is slow and unreliable. What frontend architecture choices improve user experience?”
* “We need independent releases for separate product areas. Would you choose microfrontends?”
* “How would you ensure performance, accessibility, and consistency do not degrade as the product grows?”

For interviews, prepare each answer in this pattern: **diagnose → choose trade-offs → implement incrementally → measure results → prevent regression**.

---
# Mapping above 14 questions with these 14 blueprint short questions

Yes—here is the direct mapping to the **original 45-question list**.

| Original # | Initial question (shortened)                                    | Simplified answer to use                            |
| ---------: | --------------------------------------------------------------- | --------------------------------------------------- |
|          1 | Structure a large React app                                     | **1. Structure a large frontend**                   |
|          2 | Feature vs layer vs domain folders                              | **1**                                               |
|          3 | Shared design system vs feature-specific code                   | **2. Design system**                                |
|          4 | Prevent shared library becoming too generic                     | **2**                                               |
|          5 | State management in a large app                                 | **3. State management**                             |
|          6 | Client state vs server state                                    | **3**                                               |
|          7 | Auth, permissions, errors, analytics, flags                     | **4. API layer** + **5. Auth and permissions**      |
|          8 | Design an API layer                                             | **4**                                               |
|          9 | Role-based access control                                       | **5**                                               |
|         10 | Local/staging/production configuration                          | **4** — mention environment variables/configuration |
|         11 | Introduce framework/design-system/architecture change           | **7. Legacy migration**                             |
|         12 | When to use microfrontends                                      | **8. Microfrontends**                               |
|         13 | MFE dependencies, routing, auth, versions, deployment           | **8**                                               |
|         14 | Avoid circular dependencies/shared-utils mess                   | **1** — feature boundaries and limited shared code  |
|         15 | Keep architecture decisions consistent                          | **6. Scale teams**                                  |
|         16 | What does scalable frontend mean?                               | **6**                                               |
|         17 | Scale codebase for many engineers                               | **6**                                               |
|         18 | Ownership boundaries between teams                              | **6**                                               |
|         19 | Safe independent deployments                                    | **8**                                               |
|         20 | Frontend/backend backward compatibility                         | **8** — add API versioning/gradual rollout          |
|         21 | JavaScript to TypeScript migration                              | **7**                                               |
|         22 | Break frontend monolith into modules                            | **7**                                               |
|         23 | Feature flags and safe releases                                 | **Add-on:** feature flags                           |
|         24 | Keep accessibility/testing/styling consistent                   | **2** + **6**                                       |
|         25 | Manage/version a design system                                  | **2**                                               |
|         26 | Diagnose a slow initial load                                    | **9. Slow page load**                               |
|         27 | LCP, INP, CLS                                                   | **10. Core Web Vitals**                             |
|         28 | Find whether issue is JS/network/images/rendering               | **9**                                               |
|         29 | Reduce JavaScript bundle size                                   | **9**                                               |
|         30 | Code splitting/lazy loading/dynamic imports                     | **9**                                               |
|         31 | SSR vs SSG vs ISR vs CSR                                        | **Add-on:** rendering strategy                      |
|         32 | Optimise images, fonts, static assets                           | **9**                                               |
|         33 | Prevent unnecessary React re-renders                            | **11. React re-renders**                            |
|         34 | `React.memo`, `useMemo`, `useCallback`                          | **11**                                              |
|         35 | Diagnose a component rendering too often                        | **11**                                              |
|         36 | Large lists and virtualization                                  | **12. Large lists/tables**                          |
|         37 | Optimise large dashboard/charts/live updates                    | **12** + **13. Data fetching**                      |
|         38 | Stop expensive work blocking UI                                 | **12** + **Add-on:** Web Workers                    |
|         39 | When to use Web Workers                                         | **Add-on:** Web Workers                             |
|         40 | Caching, dedupe, pagination, prefetching, cancellation, retries | **13**                                              |
|         41 | Efficient search input                                          | **13**                                              |
|         42 | Multiple in-flight requests/race conditions                     | **13**                                              |
|         43 | Measure real-user production performance                        | **14. Prevent regressions**                         |
|         44 | Performance budgets and CI                                      | **14**                                              |
|         45 | React memory leaks                                              | **Add-on:** memory leaks                            |

So the **14 main answers cover questions 1–45**, while these five are just short add-ons for follow-ups:

1. **Feature flags** — question 23
2. **Backward-compatible APIs/releases** — question 20
3. **SSR/SSG/ISR/CSR** — question 31
4. **Web Workers** — questions 38–39
5. **Memory leaks** — question 45

You do not need a completely new big answer for those five; you only need a few clear sentences ready when the interviewer goes deeper.
