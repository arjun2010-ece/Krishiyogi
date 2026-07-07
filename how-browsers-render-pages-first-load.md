This is one of the most important concepts for a React/Frontend interview. Once you understand this sequence, you'll understand why CSS blocks rendering, why `defer` is useful, why React updates are fast, and much more.

Let's imagine the browser opens:

```
https://myapp.com

```

and receives this HTML:

```
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <h1>Hello</h1>
  <button>Click Me</button>

  <script src="app.js"></script>
</body>
</html>

```

Now let's go through **everything** that happens.

* * * * *

Step 1. Browser requests the HTML
=================================

```
Browser

↓

GET /

↓

Server

↓

HTML arrives

```

At this point, the browser only has plain text.

It hasn't displayed anything yet.

* * * * *

Step 2. HTML Parser starts reading HTML
=======================================

The browser starts from the top.

```
<html>

```

↓

```
<head>

```

↓

```
<link ...>

```

↓

```
<body>

```

↓

```
<h1>

```

...and so on.

It reads **line by line**.

* * * * *

Step 3. DOM Tree is created
===========================

As the HTML parser reads tags, it creates **DOM Nodes**.

For

```
<body>
    <h1>Hello</h1>
    <button>Click</button>
</body>

```

it builds

```
Document
    │
   html
    │
 ┌──┴─────┐
head     body
            │
      ┌─────┴──────┐
      h1        button

```

This is the **DOM Tree**.

Notice:

The browser is **not drawing anything yet**.

It is only building objects in memory.

* * * * *

Step 4. CSS is downloaded
=========================

The parser encounters

```
<link rel="stylesheet" href="style.css">

```

Now it sends another request.

```
HTML

↓

Found CSS

↓

Download CSS

```

While downloading CSS, the browser **can continue building the DOM**, but it **cannot render the page yet**, because it doesn't yet know how elements should look.

* * * * *

Step 5. CSS Parser creates the CSSOM
====================================

Suppose

```
h1 {
    color: red;
}

button {
    background: blue;
}

```

The browser parses CSS into another tree called the **CSSOM**.

```
CSSOM

h1
 │
color:red

button
 │
background:blue

```

Now the browser has

```
DOM Tree ✅

CSSOM ✅

```

* * * * *

Step 6. Style Calculation
=========================

Now the browser combines

```
DOM Tree

+

CSSOM

```

to determine the final computed styles for every element.

For example,

```
<h1>Hello</h1>

```

becomes

```
h1

font-size:32px
font-weight:bold
color:red
margin:21px
display:block
...

```

This is called the **Computed Style**.

The browser now knows exactly how every element should look.

* * * * *

Step 7. Render Tree is created
==============================

Now the browser builds something called the **Render Tree**.

This is **not** the DOM Tree.

The Render Tree contains **only visible elements**.

Example:

```
<body>

<h1>Hello</h1>

<div style="display:none">
   Hidden
</div>

<button>Click</button>

</body>

```

DOM Tree

```
body
 ├── h1
 ├── div
 └── button

```

Render Tree

```
body
 ├── h1
 └── button

```

The hidden `div` is **excluded**, because it won't be rendered.

So:

-   DOM = everything in the document

-   Render Tree = only what will actually be displayed

* * * * *

Step 8. Layout (Reflow)
=======================

Now the browser asks:

> **"Where should every visible element go?"**

It calculates:

-   x-coordinate

-   y-coordinate

-   width

-   height

Example:

```
h1

x = 20

y = 30

width = 300

height = 50

```

Every visible element gets a rectangle.

This step is called **Layout** (or **Reflow**).

* * * * *

Step 9. Paint
=============

Now the browser knows:

-   what everything looks like

-   where everything goes

Finally it draws pixels.

For example,

```
Draw white background

↓

Draw black text

↓

Draw blue button

↓

Draw button text

↓

Draw border

↓

Draw shadow

```

This converts the render tree into actual colored pixels.

* * * * *

Step 10. Composite
==================

Modern browsers separate content into **layers**.

For example:

```
Background layer

Button layer

Video layer

Fixed navbar

```

The GPU combines these layers into one final image.

That image appears on your screen.

* * * * *

Complete Initial Page Load
==========================

```
1\. Browser requests HTML
          │
          ▼
2. HTML Parser
          │
          ▼
3. DOM Tree
          │
          ▼
4. Download CSS
          │
          ▼
5. CSS Parser
          │
          ▼
6. CSSOM
          │
          ▼
7. Style Calculation
(DOM + CSSOM)
          │
          ▼
8. Render Tree
(only visible elements)
          │
          ▼
9. Layout (Reflow)
(size & position)
          │
          ▼
10. Paint
(draw pixels)
          │
          ▼
11. Composite
(GPU combines layers)
          │
          ▼
🎉 Page appears on screen

```

Where does JavaScript fit?
--------------------------

Suppose your HTML contains:

```
<body>
    <h1>Hello</h1>

    <script src="app.js"></script>

    <button>Click</button>
</body>

```

When the HTML parser reaches the `<script>` tag:

1.  It **pauses parsing the HTML**.

2.  Downloads `app.js` (if needed).

3.  Executes the JavaScript.

4.  The JavaScript may modify the DOM.

5.  Only then does the parser continue reading the rest of the HTML.

That's why placing scripts at the end of the `<body>` or using the `defer` attribute often improves page loading.

* * * * *

### Interview summary (30-second answer)

> When a page loads, the browser downloads the HTML and parses it to create the DOM tree. It downloads and parses the CSS to build the CSSOM. The DOM and CSSOM are combined during style calculation to produce computed styles. The browser then creates the Render Tree, which contains only visible elements. Next, it performs Layout to calculate each element's size and position, Paint to draw the pixels, and finally Compositing, where the GPU combines layers and displays the page on the screen.

This is the complete rendering pipeline that React and other frontend frameworks ultimately rely on---they don't draw directly to the screen; they update the DOM, and the browser performs these rendering steps as needed.
