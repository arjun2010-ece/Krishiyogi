This is one of the most misunderstood parts of browser rendering. Here's the simplest explanation.

What is Paint?
--------------

**Paint means drawing pixels on the screen.**

After the browser knows:

-   **what** an element looks like (Style Recalculation)

-   **where** it should be (Layout)

it still has to **draw it**.

Think of it like this:

```
Style = Decide the color

↓

Layout = Decide where to place it

↓

Paint = Actually color the pixels

```

* * * * *

Example 1: Change text color
----------------------------

Initially:

```
<p>Hello</p>

```

```
color: black;

```

The browser has already painted black pixels.

Now JavaScript runs:

```
p.style.color = "red";

```

The browser now says:

> "The position hasn't changed, but the pixels must become red instead of black."

So it **paints** the text again.

```
Before Paint

BLACK BLACK BLACK

↓

Paint

RED RED RED

```

No layout is needed because the text stays in the same place.

* * * * *

Example 2: Change background
----------------------------

```
div.style.background = "blue";

```

Nothing moved.

The browser simply paints blue pixels inside the box.

```
Old pixels

□□□□□

↓

Paint

🟦🟦🟦🟦🟦

```

* * * * *

Example 3: Change width
-----------------------

```
div.style.width = "300px";

```

Now:

1.  Style changes

2.  Layout recalculates the new width

3.  Paint draws the newly sized box

```
Old

████

↓

Layout

████████

↓

Paint

████████

```

* * * * *

What are "pixels"?
------------------

Your monitor is made of **millions of tiny dots**, called **pixels**.

For a Full HD monitor:

```
1920 × 1080

= about 2 million pixels

```

Every pixel has a color.

Paint means changing those colors.

* * * * *

Why "only if pixels changed"?
-----------------------------

Sometimes nothing actually needs to be redrawn.

Example:

```
div.style.transform = "translateX(100px)";

```

The browser already painted the box earlier.

It simply moves the already-painted layer.

```
Old

🟥

↓

Composite

         🟥

```

Notice:

-   no new pixels were drawn

-   the browser just moved the existing painted image

That's why `transform` animations are very fast.

* * * * *

A simple analogy
----------------

Imagine drawing on paper.

### Style Recalculation

You decide:

> "The box should be blue."

You haven't drawn anything yet.

* * * * *

### Layout

You decide:

> "The box should be in the top-right corner."

Still nothing is drawn.

* * * * *

### Paint

Now you actually take a blue marker and draw the box.

This is **Paint**.

* * * * *

Easy way to remember
--------------------

```
Style
"What should it look like?"

↓

Layout
"Where should it go?"

↓

Paint
"Draw the pixels."

↓

Composite
"Show everything on the screen."

```

The key idea is:

-   **Style recalculation** decides the appearance.

-   **Layout** decides the position and size.

-   **Paint** converts that information into actual colored pixels.

-   **Composite** assembles the painted layers into the final image displayed on your screen.
