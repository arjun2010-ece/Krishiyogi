**1. Core Web Vitals / Initial Load Performance**

*Scenario:* "Our web app's initial load time is 6 seconds and LCP is failing Core Web Vitals. How do you diagnose and fix it?"

1. **Auditing:** Run Lighthouse / Chrome DevTools Performance tab to identify main-thread bottlenecks and long tasks.
2. **Code Splitting:** Implement dynamic `import()` and route-based chunking to shrink the initial bundle.
3. **Asset Optimization:** Audit third-party scripts, convert images to WebP/AVIF, enforce caching headers.
4. **Rendering Strategy:** Shift non-critical client rendering to SSR or ISR to cut Time-to-First-Byte.

*Why this matters: A senior engineer profiles before touching code — junior candidates jump straight to "add lazy loading" without confirming it's actually the bottleneck.*

---

**2. Memory Leak in a Long-Running SPA**

*Scenario:* "Users report the app freezes and tab crashes after about 20 minutes of continuous use. How do you find and fix the leak?"

1. **Reproduce & Measure:** Use Chrome DevTools Memory tab, take heap snapshots over time to confirm a growing detached-node or listener trend.
2. **Isolate:** Use the Allocation Instrumentation timeline to pinpoint which component/action triggers growth.
3. **Root Cause:** Check for uncleaned `setInterval`/`setTimeout`, unremoved event listeners, or missing cleanup in `useEffect`.
4. **Fix:** Add cleanup functions, use `AbortController` for fetches, and verify with a follow-up heap diff.

*Why this matters: Seniors diagnose with heap snapshots and comparisons; mid-level engineers guess-and-check by reading code line by line.*

---

**3. Unnecessary Re-renders / Large List Performance**

*Scenario:* "Our dashboard with a 5,000-row table becomes laggy on every keystroke in the search box. How do you fix it?"

1. **Auditing:** Use React DevTools Profiler to confirm which components re-render on each keystroke.
2. **Isolate Cause:** Check for missing memoization (`React.memo`, `useMemo`, `useCallback`) and unstable prop references.
3. **Windowing:** Implement list virtualization (`react-window` / `react-virtual`) so only visible rows render.
4. **Debounce:** Debounce the search input to reduce render frequency at the source.

*Why this matters: Senior answers fix the actual render trigger (virtualization + memoization); junior answers just wrap everything in `useMemo` without profiling first.*

---

**4. State Management Issues at Scale**

*Scenario:* "Two API calls update the same piece of state, and users occasionally see stale or flickering data. How do you approach this?"

1. **Reproduce:** Add logging/React DevTools state inspection to confirm a race condition between concurrent requests.
2. **Root Cause:** Identify that the later-dispatched request isn't guaranteed to resolve last.
3. **Fix — Cancellation:** Use `AbortController` or a request-ID guard to discard stale responses.
4. **Fix — Architecture:** Move to a data-fetching library (React Query/SWR) that handles race conditions and caching natively.

*Why this matters: Seniors name the race condition explicitly and reach for cancellation, not just "add a loading spinner" which papers over the bug.*

---

**5. Intermittent Production Bug (Hydration Mismatch)**

*Scenario:* "We're seeing a console warning about hydration mismatches in production, and some users see flickering content on page load. How do you debug this?"

1. **Auditing:** Read the exact hydration warning in the console — it names the mismatched element/attribute.
2. **Isolate:** Check for non-deterministic rendering: `Date.now()`, `Math.random()`, browser-only APIs (`window`, `localStorage`) running during SSR.
3. **Root Cause:** Confirm server-rendered HTML and client-rendered HTML diverge due to environment-dependent logic.
4. **Fix:** Guard browser-only code with `useEffect` or `typeof window !== 'undefined'`, or use `suppressHydrationWarning` only as a last resort.

*Why this matters: Seniors read the actual mismatch message instead of guessing; they know hydration bugs are almost always non-determinism between server and client.*

---

**6. Flaky Third-Party API / Network Failure Handling**

*Scenario:* "Our checkout flow depends on a third-party payment API that fails intermittently, and users are abandoning carts. How do you handle this?"

1. **Auditing:** Check Network tab / logs to quantify failure rate and identify if it's timeout, 5xx, or rate-limit related.
2. **Resilience:** Implement retry logic with exponential backoff for transient failures.
3. **UX Strategy:** Add optimistic UI or a clear loading/error state so users aren't left guessing.
4. **Fallback:** Add a circuit breaker or graceful degradation path (e.g., queue the request, notify the user) if retries exhaust.

*Why this matters: Seniors separate retryable errors from permanent ones and design for the failure, not just wrap the call in a try/catch.*

---

**7. Accessibility Regression Shipped to Production**

*Scenario:* "A screen-reader user reported they can't complete our sign-up form anymore after a recent redesign. How do you investigate and fix it?"

1. **Auditing:** Run axe DevTools / Lighthouse accessibility audit on the form to catch automated violations.
2. **Manual Test:** Tab through the form and test with a screen reader (VoiceOver/NVDA) to catch what automated tools miss.
3. **Root Cause:** Check for missing `label`/`aria-*` associations, broken focus order, or non-semantic elements (`div` used as button).
4. **Fix:** Restore semantic HTML and proper ARIA attributes, then add an automated a11y check (e.g., `jest-axe`) to CI to prevent regression.

*Why this matters: Seniors combine automated + manual testing and add a regression guard; junior answers stop at "add alt text."*

---

**8. Frontend Security Issue (XSS / Exposed Tokens)**

*Scenario:* "A security review flagged that user-generated content in our comments section can execute arbitrary scripts. How do you fix it?"

1. **Auditing:** Identify where user input is rendered — check for `dangerouslySetInnerHTML` or unescaped template injection.
2. **Root Cause:** Confirm raw HTML/script from user input is being rendered without sanitization.
3. **Fix:** Sanitize with a library like DOMPurify before rendering, or avoid raw HTML rendering entirely.
4. **Harden:** Add a Content-Security-Policy header to block inline scripts as a defense-in-depth layer.

*Why this matters: Seniors treat CSP as a second layer, not the fix — sanitization at the render point is the actual root-cause solution.*

---

**9. Core Web Vitals — Layout Shift (CLS)**

*Scenario:* "Our CLS score is failing because content jumps around as the page loads. How do you diagnose and fix it?"

1. **Auditing:** Use Chrome DevTools Performance tab or Lighthouse to record and visually replay the layout shift.
2. **Isolate:** Check for images/ads/embeds without reserved dimensions, and web fonts causing FOUC/FOIT reflow.
3. **Root Cause:** Confirm elements are injected above existing content without space being reserved.
4. **Fix:** Set explicit `width`/`height` (or `aspect-ratio`) on media, preload critical fonts, reserve space for dynamic content (ads/banners).

*Why this matters: Seniors reserve layout space proactively; junior answers try to fix it after the fact with CSS patches.*

---

**10. Debouncing vs. Throttling in Practice**

*Scenario:* "Our live search fires an API call on every keystroke and it's overwhelming the backend. How do you fix it, and would you debounce or throttle?"

1. **Auditing:** Confirm via Network tab that every keystroke triggers a request.
2. **Decision:** Debounce (wait for pause in typing) is correct here — throttle is for continuous events like scroll/resize, not discrete input completion.
3. **Fix:** Implement a debounce (e.g., 300-500ms) on the input handler before firing the request.
4. **Enhance:** Add request cancellation (`AbortController`) so an in-flight stale request doesn't overwrite a newer result.

*Why this matters: Seniors know debounce and throttle solve different problems and can justify the choice — not just "add a delay."*

---

**11. Closures / Event Loop Gotcha**

*Scenario:* "A `for` loop with `setTimeout` is logging the same final value for every iteration instead of each index. Why, and how do you fix it?"

1. **Diagnose:** Confirm the loop uses `var`, which is function-scoped, so all callbacks share one variable reference by the time they run.
2. **Explain Root Cause:** The event loop defers `setTimeout` callbacks until after the synchronous loop finishes, so all closures see the final value.
3. **Fix — Simple:** Replace `var` with `let`, which creates a new binding per iteration.
4. **Fix — Alternative:** Wrap in an IIFE to capture the value per iteration if `let` isn't an option (legacy code).

*Why this matters: Seniors explain both the closure and the event-loop timing — not just "use let," but why it works.*

---

**12. Bundle Size / Webpack-Level Optimization**

*Scenario:* "Our production bundle is 3MB and keeps growing with every feature. How do you investigate and reduce it?"

1. **Auditing:** Run `webpack-bundle-analyzer` (or equivalent for Vite/esbuild) to visualize what's contributing size.
2. **Root Cause:** Identify duplicate dependencies, unused exports, or large libraries imported in full (e.g., all of Lodash/Moment).
3. **Fix:** Tree-shake with ES module imports, replace heavy libraries (Moment → date-fns/Day.js), enable code splitting per route.
4. **Guardrail:** Add a bundle-size budget/CI check (e.g., `bundlesize`, `size-limit`) to catch regressions before merge.

*Why this matters: Seniors add a guardrail so the problem doesn't recur — junior answers stop once the current bundle is smaller.*

---

**13. CORS Errors in Production**

*Scenario:* "Users report API calls failing with a CORS error, but it works fine locally. How do you debug and resolve it?"

1. **Auditing:** Check the browser console/Network tab for the exact CORS error (missing header vs. preflight failure vs. credentials issue).
2. **Root Cause:** Confirm whether the backend's `Access-Control-Allow-Origin` doesn't include the production domain, or a preflight `OPTIONS` request is failing.
3. **Fix:** Update backend CORS config to explicitly allow the production origin (avoid `*` if credentials are used).
4. **Clarify Ownership:** Confirm this is a backend/infra fix, not something patchable from the frontend — proxying in dev is not a production solution.

*Why this matters: Seniors correctly identify CORS as a backend-configuration issue and explain preflight behavior, rather than trying to "fix" it with frontend hacks.*

---

**14. TypeScript — `any` Creeping Into a Codebase**

*Scenario:* "Code review keeps finding `any` types slipping into PRs, and a bug shipped because of it. How do you address this at a team level?"

1. **Auditing:** Run `tsc --noImplicitAny` and lint rules (`@typescript-eslint/no-explicit-any`) to quantify current usage.
2. **Root Cause:** Identify common causes — untyped third-party libraries, rushed API response typing, generic overuse avoidance.
3. **Fix:** Add proper types/interfaces for API responses (or generate from OpenAPI/GraphQL schema), use `unknown` + narrowing instead of `any` where type is genuinely uncertain.
4. **Guardrail:** Enforce the ESLint rule in CI so new `any` usage fails the build, with an explicit escape hatch (`// eslint-disable-next-line` + comment) for rare exceptions.

*Why this matters: Seniors fix it systemically with tooling and CI enforcement, not just by manually retyping the one file that broke.*

---

**15. Testing Strategy for a Flaky Test Suite**

*Scenario:* "Our E2E tests pass locally but fail randomly in CI about 20% of the time. How do you approach fixing this?"

1. **Auditing:** Check CI logs/screenshots for the failure pattern — timing-related vs. environment-related vs. test-order-dependent.
2. **Root Cause:** Commonly a race condition — test asserts before an async UI update/network call resolves.
3. **Fix:** Replace fixed `sleep()`/arbitrary waits with condition-based waits (`waitFor`, `findBy*` queries) that poll until state settles.
4. **Prevent Recurrence:** Isolate test state (no shared fixtures/global state) and run suspect tests in isolation with `--repeat` to confirm the fix.

*Why this matters: Seniors treat flaky tests as real bugs in test design, not something to just retry until green.*

---

**16. CSS Layout — Flexbox/Grid Overflow Bug**

*Scenario:* "A flex container with dynamic content is causing text to overflow its parent instead of wrapping or truncating. How do you fix it?"

1. **Diagnose:** Inspect via DevTools to confirm the flex item has no `min-width: 0` (flex items default to `min-width: auto`, which prevents shrinking below content size).
2. **Root Cause:** Long unbroken text (URLs, IDs) inside a flex child ignores the container's width constraint.
3. **Fix:** Set `min-width: 0` on the flex child, then apply `overflow: hidden` + `text-overflow: ellipsis` or `word-break: break-word` depending on desired behavior.
4. **Verify:** Test with real dynamic content (long strings, empty strings) not just placeholder text.

*Why this matters: Seniors know the `min-width: auto` flexbox default by name — it's one of the most common "invisible" CSS bugs mid-level engineers can't explain.*

---

**17. WebSockets / Real-Time Data Sync**

*Scenario:* "Our live dashboard using WebSockets shows stale data after a user's laptop sleeps and wakes up. How do you handle this?"

1. **Diagnose:** Confirm the WebSocket connection silently dies on sleep (no `close` event fires immediately) and the UI has no reconnection logic.
2. **Root Cause:** No heartbeat/ping-pong mechanism to detect a dead connection, and no reconnection strategy.
3. **Fix:** Implement a heartbeat (ping/pong) to detect dead connections quickly, and exponential-backoff auto-reconnect on `close`/`error`.
4. **Data Integrity:** On reconnect, re-sync state via a REST fetch or "catch-up" event rather than assuming the WebSocket stream picks up seamlessly.

*Why this matters: Seniors treat reconnection and state re-sync as a single problem — junior answers just add `ws.reconnect()` without addressing stale data after the gap.*

---

**18. PWA / Offline Caching Strategy**

*Scenario:* "We want the app to remain usable when a user loses internet connection mid-session. How do you approach this?"

1. **Scope:** Clarify what "usable" means — read-only cached view vs. full offline write support (changes the entire approach).
2. **Auditing:** Use Chrome DevTools Application tab / Lighthouse PWA audit to check current caching baseline.
3. **Fix — Static Assets:** Register a Service Worker with a cache-first strategy for app shell/static assets.
4. **Fix — Data:** Use stale-while-revalidate for API data, and queue mutations (e.g., via IndexedDB + Background Sync API) to replay when connection returns.

*Why this matters: Seniors ask a clarifying scope question first — "offline support" means very different engineering effort depending on read-only vs. read-write.*

---

**19. Infinite Scroll Performance Degradation**

*Scenario:* "Our infinite-scroll feed gets noticeably laggy after a user scrolls through a few hundred items. How do you fix it?"

1. **Auditing:** Use React DevTools Profiler / Performance tab to confirm DOM node count is growing unbounded.
2. **Root Cause:** Every fetched item stays mounted in the DOM indefinitely — no virtualization or unmounting of off-screen items.
3. **Fix:** Implement windowing (`react-window`/`react-virtual`) to keep only visible + buffer items mounted.
4. **Guardrail:** Cap in-memory item count or paginate-and-discard older items if virtualization alone isn't sufficient.

*Why this matters: Seniors identify unbounded DOM growth as the root cause, not just "add pagination," which doesn't fix already-rendered lag.*

---

**20. Form Validation at Scale**

*Scenario:* "Our multi-step signup form has validation logic duplicated across steps, and a recent bug let invalid data through on step 3. How do you redesign this?"

1. **Auditing:** Map out where validation currently lives — confirm it's scattered per-component instead of centralized.
2. **Root Cause:** No single source of truth for validation rules, so steps drift out of sync as the form evolves.
3. **Fix:** Centralize schema-based validation (Zod/Yup) shared across all steps, validated both on blur/step-change and final submit.
4. **Defense-in-Depth:** Never trust client-side validation alone — confirm the same rules are enforced server-side.

*Why this matters: Seniors immediately flag that client-side validation is UX, not security, and design a single schema instead of patching step 3 in isolation.*

---

**21. Image-Heavy Page Optimization (Deep Dive)**

*Scenario:* "Our product listing page has 100+ images and LCP is consistently over 4 seconds. Beyond format conversion, what else do you check?"

1. **Auditing:** Use Chrome DevTools Network tab filtered by image type, sorted by size/time, to find the worst offenders.
2. **Root Cause:** Check for missing `loading="lazy"` on below-the-fold images, oversized images serving desktop resolution to mobile, and no `srcset`/responsive sizing.
3. **Fix:** Add `srcset`/`sizes` for responsive images, lazy-load below-the-fold, and identify/preload the actual LCP element explicitly (`fetchpriority="high"`).
4. **Infrastructure:** Serve via a CDN/image optimization service (Cloudinary, Next/Image) that handles format + resizing automatically.

*Why this matters: Seniors go beyond format conversion to explicitly identify and prioritize the LCP element itself — most candidates stop at "use WebP."*

---
