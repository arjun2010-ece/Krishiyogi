The statement in the screenshot is **mostly correct**, but there is one important detail:

> **A DOM change *can* trigger style recalculation, layout (reflow), and paint --- but not every DOM change triggers all three.**

The browser is smart. It only performs the work that is actually needed.

The browser rendering pipeline (simple sequence)
------------------------------------------------

Imagine you execute:

```
div.style.width = "200px";

```

The browser goes through these steps:

### 1\. DOM changes

The DOM tree is updated.

```
Old:
<div width="100px">

↓

New:
<div width="200px">

```

Nothing is visible on the screen yet.

* * * * *

### 2\. Style Recalculation

The browser asks:

> "What should this element's final styles be now?"

It recalculates CSS for this element (and sometimes its children).

For example:

```
.box {
  color: blue;
}

```

becomes

```
width = 200px
color = blue
display = block
margin = ...

```

This step determines the computed styles.

* * * * *

### 3\. Layout (Reflow) --- only if needed

Now the browser asks:

> "Did this style change affect size or position?"

If yes, it recalculates the layout.

Example:

Changing

```
width
height
padding
margin
display
font-size

```

changes the size or position.

The browser recalculates things like:

-   width

-   height

-   x position

-   y position

It may also need to move neighboring elements.

* * * * *

### 4\. Paint --- only if pixels changed

Now the browser asks:

> "What should the screen look like?"

It redraws pixels.

Examples:

-   text

-   background

-   border

-   shadow

-   image

* * * * *

### 5\. Composite (GPU)

Finally, the browser combines all painted layers and displays the updated screen.

This is what you actually see.

* * * * *

Complete sequence
=================

```
JavaScript

↓

DOM changes

↓

Style Recalculation

↓

Layout (if needed)

↓

Paint (if needed)

↓

Composite

↓

Screen updates

```

* * * * *

Examples
========

### Example 1: Change text color

```
div.style.color = "red";

```

```
DOM change
↓

Style recalculation ✅

↓

Layout ❌
(no size changed)

↓

Paint ✅

↓

Composite

```

* * * * *

### Example 2: Change width

```
div.style.width = "300px";

```

```
DOM change

↓

Style recalculation ✅

↓

Layout ✅
(size changed)

↓

Paint ✅

↓

Composite

```

* * * * *

### Example 3: Change transform

```
div.style.transform = "translateX(100px)";

```

```
DOM change

↓

Style recalculation ✅

↓

Layout ❌

↓

Paint ❌ (often skipped)

↓

Composite ✅

```

This is why `transform` and `opacity` animations are very fast---they usually only require the GPU compositing step.

Easy interview answer
---------------------

> **When the DOM changes, the browser first updates the DOM, then recalculates styles. If the change affects an element's size or position, it performs layout (reflow). If the visual appearance changes, it repaints the affected pixels. Finally, it composites the layers and displays the updated result on the screen. Not every DOM change triggers all these steps---only the ones that are necessary.**
