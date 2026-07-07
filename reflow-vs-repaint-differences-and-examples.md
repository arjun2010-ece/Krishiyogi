This is one of the **most frequently asked frontend interview questions**, and many developers confuse the two.

The easiest way to remember them is:

> **Reflow = Recalculate the layout (size & position)**\
> **Repaint = Redraw the pixels (appearance only)**

* * * * *

First, let's understand the difference
======================================

Imagine this webpage:

```
+----------------------------------+
|  🏠 Home                         |
|                                  |
|  Hello World                     |
|                                  |
|  [ Submit ]                      |
+----------------------------------+

```

Now let's see what happens for different changes.

* * * * *

What is Reflow (Layout)?
========================

Reflow happens when the browser needs to answer:

> **"Where should elements be, and how big should they be?"**

It recalculates:

-   width

-   height

-   x-position

-   y-position

Sometimes it also needs to move neighboring elements.

* * * * *

Example 1 --- Change width
------------------------

Initially

```
+-----------+
|  Button   |
+-----------+

```

JavaScript

```
button.style.width = "300px";

```

Now the button becomes larger.

```
+-------------------------------+
|          Button               |
+-------------------------------+

```

The browser must calculate:

-   new width

-   new height

-   whether nearby elements should move

✅ Reflow occurs

✅ Repaint occurs

* * * * *

Example 2 --- Add a new element
-----------------------------

```
const p = document.createElement("p");
document.body.appendChild(p);

```

Before

```
Title

Button

```

After

```
Title

Button

New Paragraph

```

The browser must calculate positions again.

✅ Reflow

✅ Repaint

* * * * *

Example 3 --- Increase font size
------------------------------

```
heading.style.fontSize = "40px";

```

Old

```
Hello

```

New

```
HELLO

```

The larger text may push everything below it downward.

So the browser recalculates the layout.

✅ Reflow

✅ Repaint

* * * * *

What is Repaint?
================

Repaint happens when:

> **The position and size stay the same, but the appearance changes.**

The browser only redraws pixels.

* * * * *

Example 1 --- Change text color
-----------------------------

```
heading.style.color = "red";

```

Before

```
BLACK TEXT

```

After

```
RED TEXT

```

Nothing moved.

Only the color changed.

❌ No Reflow

✅ Repaint

* * * * *

Example 2 --- Change background
-----------------------------

```
div.style.background = "blue";

```

Before

```
⬜⬜⬜⬜

```

After

```
🟦🟦🟦🟦

```

Same size.

Same position.

Only new pixels are drawn.

❌ No Reflow

✅ Repaint

* * * * *

Example 3 --- Change border color
-------------------------------

```
div.style.borderColor = "green";

```

Only the border color changes.

Nothing moves.

❌ No Reflow

✅ Repaint

* * * * *

A visual comparison
===================

### Reflow

```
Before

A
B
C

```

Increase height of A

```
After

AAAA

B

C

```

Everything below moves.

Browser recalculates layout.

* * * * *

### Repaint

```
Before

🔵 Button

```

Change color

```
After

🔴 Button

```

Same location.

Only redraw pixels.

* * * * *

Relationship
============

A very important rule:

```
Reflow

↓

always causes

↓

Repaint

```

Because after calculating a new layout, the browser must draw it again.

* * * * *

But

```
Repaint

↓

does NOT cause

↓

Reflow

```

Because nothing moved.

* * * * *

Think of it like moving furniture in a room:

### Reflow

Move the sofa.

Now you also need to move the table.

Everything's position changes.

* * * * *

### Repaint

Paint the sofa blue.

Its position doesn't change.

Only its appearance changes.

* * * * *

Interview table
===============

| Change | Reflow | Repaint |
| --- | :-: | :-: |
| `width` | ✅ | ✅ |
| `height` | ✅ | ✅ |
| `margin` | ✅ | ✅ |
| `padding` | ✅ | ✅ |
| `font-size` | ✅ | ✅ |
| Add/remove element | ✅ | ✅ |
| `color` | ❌ | ✅ |
| `background-color` | ❌ | ✅ |
| `border-color` | ❌ | ✅ |
| `visibility: hidden` | ❌ | ✅ |
| `opacity` | ❌ *(usually)* | Often handled during compositing |
| `transform: translate()` | ❌ | Often no repaint; handled by compositing |

> **Note:** Modern browsers optimize some properties such as `transform` and `opacity`. Instead of repainting, they often move or fade an already-painted layer during the **compositing** stage, which is why these properties are recommended for smooth animations.

* * * * *

One thing interviewers love to ask
==================================

> **Why are `transform` and `opacity` considered faster for animations?**

Because they **usually don't trigger Reflow** and often **don't even trigger Repaint**. The browser can simply update the **Composite** step by moving or blending an existing layer using the GPU.

```
Change transform

↓

No Layout

↓

No Paint (in many cases)

↓

Composite only

↓

Very smooth animation (60 FPS)

```

* * * * *

Easy interview answer
---------------------

> **Reflow (Layout) occurs when a change affects an element's size or position, so the browser must recalculate the layout. Repaint occurs when only an element's visual appearance changes, such as its color or background, without affecting its size or position. Every reflow leads to a repaint because the updated layout must be drawn, but a repaint does not necessarily require a reflow. Modern browsers can often optimize changes to `transform` and `opacity` by handling them during compositing, avoiding both reflow and repaint.**
