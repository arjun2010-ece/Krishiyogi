These are exactly the kinds of questions asked in **mid/senior frontend interviews** because they test whether you understand how the browser renders a page, not just React. Let's tackle them one by one.

* * * * *

1\. How would you reduce the Largest Contentful Paint (LCP) / First Contentful Paint (FCP)?
===========================================================================================

First, understand the metrics
-----------------------------

### First Contentful Paint (FCP)

> The time until the browser displays the **first visible content**.

For example:

```
User opens page

↓

White screen

↓

Logo appears

↑
FCP

```

* * * * *

### Largest Contentful Paint (LCP)

> The time until the **largest visible element** in the viewport is rendered.

Usually this is:

-   Hero image

-   Main heading

-   Large banner

-   Large paragraph

Example:

```
White page

↓

Logo appears
(FCP)

↓

Hero image appears
(LCP)

```

* * * * *

How do we improve them?
-----------------------

Remember the Critical Rendering Path:

```
Download HTML

↓

DOM

↓

CSS

↓

CSSOM

↓

Render Tree

↓

Layout

↓

Paint

```

To improve FCP/LCP, we reduce the work before Paint.

### 1\. Reduce render-blocking CSS ✅

Instead of

```
<link rel="stylesheet" href="style.css">

```

Inline the CSS needed for the first screen:

```
<style>
.hero {
    color: white;
}
</style>

```

The browser doesn't need to wait for another request.

* * * * *

### 2\. Use `defer` for JavaScript ✅

Instead of

```
<script src="app.js"></script>

```

use

```
<script defer src="app.js"></script>

```

HTML parsing continues while JS downloads.

* * * * *

### 3\. Optimize images ✅

Bad:

```
<img src="hero.jpg">

```

Better:

-   compress image

-   use WebP/AVIF

-   preload hero image if appropriate

* * * * *

### 4\. Lazy load below-the-fold images ✅

```
<img loading="lazy">

```

Images that aren't immediately visible don't delay rendering.

* * * * *

### 5\. Reduce JavaScript bundle size ✅

Instead of downloading

```
2 MB JavaScript

```

download

```
300 KB

```

Less download.

Less parsing.

Less execution.

* * * * *

### 6\. Reduce server response time

If HTML arrives faster,

everything else starts earlier.

* * * * *

### Interview answer

> To improve FCP and LCP, I would optimize the Critical Rendering Path by reducing render-blocking CSS, using `defer` for JavaScript, optimizing and lazy-loading images, reducing JavaScript bundle size, compressing assets, caching resources, and improving server response times. The goal is to show meaningful content as early as possible.

* * * * *

2\. What does `will-change` do?
===============================

Imagine this animation:

```
.card:hover {
    transform: scale(1.1);
}

```

Normally,

the browser may decide

> "I need a compositor layer."

Creating one takes time.

* * * * *

Instead,

you tell the browser beforehand:

```
.card {
    will-change: transform;
}

```

You're saying:

> "This property is about to change, prepare in advance."

The browser may create a compositor layer before the animation starts.

The animation becomes smoother.

* * * * *

Why is overusing it bad?
------------------------

Suppose you write

```
* {
    will-change: transform;
}

```

Now every element may get its own layer.

Problems:

-   huge GPU memory usage

-   more compositing work

-   worse performance

`will-change` is a hint, not a free optimization.

* * * * *

Interview answer:

> `will-change` tells the browser which properties are likely to change soon so it can prepare optimizations such as creating compositor layers. It should only be used on elements that actually animate because too many compositor layers increase memory usage and compositing cost.

* * * * *

3\. Difference between `DOMContentLoaded` and `load`
====================================================

This question is very common.

Imagine this page:

```
<body>

<img src="large.jpg">

<script src="app.js"></script>

</body>

```

* * * * *

DOMContentLoaded
----------------

This fires when

✅ HTML parsed

✅ DOM created

❌ Images may still be downloading

❌ Fonts may still be downloading

❌ Videos may still be downloading

Timeline

```
HTML downloaded

↓

DOM built

↓

DOMContentLoaded

↓

Images continue downloading

```

* * * * *

load
----

This waits for

-   HTML

-   CSS

-   Images

-   Fonts

-   Videos

-   iframes

Everything.

Timeline

```
HTML

↓

DOM

↓

Images

↓

Fonts

↓

Videos

↓

load

```

* * * * *

Interview answer

> `DOMContentLoaded` fires once the HTML has been completely parsed and the DOM has been built. It doesn't wait for images, fonts, or other external resources. The `load` event fires only after the entire page and all dependent resources have finished loading.

* * * * *

4\. If you change `display: none` to `block` inside a loop and read `offsetHeight` every time, what happens?
============================================================================================================

Example:

```
const items = document.querySelectorAll(".item");

items.forEach(item => {
    item.style.display = "block";      // WRITE

    console.log(item.offsetHeight);    // READ
});

```

* * * * *

Let's follow what the browser does.

Iteration 1

```
display:block

↓

Layout becomes invalid

↓

offsetHeight

↓

Browser must perform Layout immediately

↓

Returns height

```

* * * * *

Iteration 2

```
display:block

↓

Layout invalid again

↓

offsetHeight

↓

Layout again

```

* * * * *

Iteration 3

Same thing.

The browser repeatedly does:

```
WRITE

↓

Forced Layout

↓

WRITE

↓

Forced Layout

↓

WRITE

↓

Forced Layout

```

This is called

Forced Synchronous Layout
-------------------------

because

`offsetHeight`

forces the browser to calculate layout **immediately**, even if it wanted to postpone that work until the next rendering cycle.

Since it happens over and over in the loop, you've also created **layout thrashing**.

* * * * *

Better approach
---------------

Write everything first:

```
items.forEach(item => {
    item.style.display = "block";
});

```

Then read:

```
items.forEach(item => {
    console.log(item.offsetHeight);
});

```

Now the browser can perform **one layout calculation** instead of one per iteration.

* * * * *

Interview answer
----------------

> Changing an element from `display: none` to `block` invalidates the layout because the element now participates in the page layout. Reading `offsetHeight` immediately afterwards forces the browser to synchronously recalculate the layout before it can return the height. Doing this inside a loop repeatedly creates forced synchronous layouts and results in layout thrashing, which hurts performance. The fix is to batch DOM writes first, then perform all layout reads afterward.

* * * * *

Senior Interview Cheat Sheet
============================

| Question | Short Answer |
| --- | --- |
| **How do you improve FCP/LCP?** | Optimize the Critical Rendering Path: reduce render-blocking CSS, use `defer`, optimize/lazy-load images, reduce JS bundle size, compress and cache assets, and improve server response time. |
| **What does `will-change` do?** | It hints that a property will change soon so the browser can prepare optimizations, often by creating a compositor layer. Overusing it wastes GPU memory and can reduce performance. |
| **DOMContentLoaded vs load** | `DOMContentLoaded` fires after the HTML is parsed and the DOM is built. `load` waits for all resources (images, fonts, CSS, videos, iframes) to finish loading. |
| **`display: none → block` + `offsetHeight` in a loop** | Each write invalidates layout, and each `offsetHeight` read forces an immediate layout calculation. Repeating this causes forced synchronous layout and layout thrashing. |
