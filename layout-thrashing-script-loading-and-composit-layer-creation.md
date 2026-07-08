1\. What is layout thrashing?
-----------------------------

**Layout thrashing** happens when JavaScript repeatedly does this pattern:

```
read layout
write layout
read layout
write layout

```

Example bug:

```
const boxes = document.querySelectorAll(".box");

boxes.forEach((box) => {
  const height = box.offsetHeight;   // READ layout
  box.style.height = height + 10 + "px"; // WRITE layout
});

```

Problem: every time you write `style.height`, the browser's layout becomes outdated. Then the next `offsetHeight` forces the browser to recalculate layout immediately.

Better fix: **read first, write later**.

```
const boxes = document.querySelectorAll(".box");

const heights = Array.from(boxes, (box) => box.offsetHeight); // READ all first

boxes.forEach((box, index) => {
  box.style.height = heights[index] + 10 + "px"; // WRITE all later
});

```

Even better for many updates:

```
requestAnimationFrame(() => {
  boxes.forEach((box, index) => {
    box.style.height = heights[index] + 10 + "px";
  });
});

```

Simple rule:

```
Bad:
read → write → read → write

Good:
read → read → read → write → write → write

```

Common layout-reading properties:

```
offsetWidth
offsetHeight
clientWidth
clientHeight
scrollWidth
scrollHeight
getBoundingClientRect()
getComputedStyle()

```

* * * * *

2\. Why do `async` and `defer` change page load behavior?
---------------------------------------------------------

Normal script:

```
<script src="app.js"></script>

```

Behavior:

```
HTML parsing starts
↓
Browser finds script
↓
HTML parsing stops
↓
Script downloads
↓
Script executes
↓
HTML parsing continues

```

So normal scripts are **parser-blocking**.

* * * * *

### `defer`

```
<script defer src="app.js"></script>

```

Behavior:

```
HTML parsing continues
↓
Script downloads in parallel
↓
Script executes after HTML parsing is complete
↓
Before DOMContentLoaded

```

Use `defer` for most app scripts.

Good for:

```
<script defer src="main.js"></script>

```

Important: multiple `defer` scripts execute **in order**.

* * * * *

### `async`

```
<script async src="analytics.js"></script>

```

Behavior:

```
HTML parsing continues
↓
Script downloads in parallel
↓
Script executes immediately when downloaded

```

When it executes, it can still pause HTML parsing.

Use `async` for independent scripts like:

```
<script async src="analytics.js"></script>

```

Important: multiple `async` scripts do **not** guarantee order.

* * * * *

3\. What creates a new compositor layer?
----------------------------------------

A compositor layer is like a separate visual sheet that the browser can move/fade using the GPU.

Common triggers:

```
transform: translateZ(0);
transform: translate3d(...);
will-change: transform;
will-change: opacity;
position: fixed;
opacity animation;
filter;
video;
canvas;

```

Example:

```
.card {
  will-change: transform;
}

```

This may promote `.card` to its own compositor layer.

Why useful?

```
.card:hover {
  transform: translateY(-8px);
}

```

The browser can often animate this without layout and repaint.

* * * * *

Downside of too many compositor layers
--------------------------------------

Too many layers are bad because they consume GPU memory.

Problems:

```
Too many layers
↓
More GPU memory usage
↓
More layer management cost
↓
More compositing work
↓
Possible jank / lag / worse performance

```

Bad example:

```
* {
  will-change: transform;
}

```

This tells the browser to prepare many elements as separate layers. That can make performance worse.

Better:

```
.card:hover {
  transform: translateY(-8px);
}

```

Or use `will-change` only shortly before animation:

```
.card {
  transition: transform 200ms;
}

.card:hover {
  will-change: transform;
  transform: translateY(-8px);
}

```

Interview answer:

> Layout thrashing happens when JavaScript repeatedly mixes layout reads and layout writes, forcing the browser to recalculate layout many times. Fix it by batching reads first and writes later. `defer` downloads scripts in parallel and executes them after HTML parsing, while `async` downloads in parallel and executes as soon as ready. New compositor layers are often created by transform, opacity, fixed elements, video/canvas, filters, or `will-change`, but too many layers increase memory usage and can hurt performance.
