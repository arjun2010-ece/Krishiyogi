# How frontend dev works with UX design team

You do not need to memorise 58 separate answers. Most of them are really testing a few habits: clarify early, think about users and edge cases, build reusable UI, include accessibility, and verify the result.

A simple pattern to remember is:

**Understand → Clarify → Build → Check → Improve**

Below are the questions grouped into 10 easy interview answers. Learn the idea behind each answer, then adapt it naturally.

---

## 1. How do you work with UX/UI designers?

**Covers:** 1, 2, 7, 8, 9, 10

**Interview answer:**

> I like to involve myself early, ideally when a feature is being discussed rather than only after the final design is ready. First, I try to understand the user’s goal: what problem are we solving and what should the user be able to do?
>
> Then I review the design with the designer and product manager. I ask questions, point out technical constraints early, and suggest alternatives if something may be slow, difficult to maintain, or confusing for users.
>
> During development, I keep communication open instead of making assumptions. Before release, I compare the implementation with the design and check that it works properly on different screens and in real user situations.

**Easy memory:** *Work early, communicate openly, check before release.*

---

## 2. What do you check when you receive a Figma design?

**Covers:** 3, 5, 13, 15, 18, 19

**Interview answer:**

> I do not only look at the happy path in Figma. I check what happens when data is loading, empty, missing, too long, or when an API request fails.
>
> I also check interactive states: hover, focus, disabled, selected, validation errors, success messages, and mobile behaviour. If only a desktop design is available, I ask how the layout should behave on tablet and mobile rather than guessing.
>
> After that, I break the work into smaller pieces: reusable components, API integration, states, testing, and responsive behaviour. That helps me estimate the task more accurately.

**Good questions to ask a designer:**

* What should happen while data is loading?
* What does the empty state look like?
* What happens if the API fails?
* What happens with very long text or many items?
* How should it work on mobile?
* What should keyboard focus and validation look like?

**Easy memory:** *Don’t just check how it looks—check what happens.*

---

## 3. What if a design is unclear, missing something, or hard to build?

**Covers:** 4, 5, 9, 17, 18

**Interview answer:**

> I avoid silently making big assumptions. If something is unclear, I explain the specific question to the designer or product manager and suggest one or two practical options.
>
> If a design is expensive or risky to implement, I do not simply say “no.” I explain the trade-off in plain language. For example: “We can build this animation, but it may affect performance on lower-end mobile devices. Could we use a simpler version that still gives the same feeling?”
>
> If the design changes during development, I first understand the reason and impact. Small changes are normal. But if it affects shared components, accessibility, or the timeline, I discuss it early so the team can make a sensible decision.

**Easy memory:** *Do not complain; explain the trade-off and offer options.*

---

## 4. How do you convert a design into React components?

**Covers:** 11, 12, 16, 20

**Interview answer:**

> I first look for repeated patterns in the design: buttons, inputs, cards, modals, page sections, and layouts. Repeated patterns usually become reusable components.
>
> I keep components reusable when the same structure is likely to appear in multiple places. But I do not over-engineer everything. If something is truly unique and simple, a page-specific component can be clearer.
>
> I use shared styles, tokens, and component variants so spacing, colours, typography, and behaviour stay consistent. This also makes future design changes safer because we can update one shared component instead of many separate copies.

**Example:**

* `Button` with variants: primary, secondary, danger
* `Input` with states: default, focus, error, disabled
* `Card` with variants: basic, selectable, highlighted

**Easy memory:** *Find repetition, make it reusable, but do not over-abstract.*

---

## 5. What is a design system, and how do you use it?

**Covers:** 21, 22, 23, 24, 25, 26, 27, 28, 29, 30

**Interview answer:**

> A design system is a shared language between design and engineering. It includes things such as colours, spacing, typography, icons, and reusable UI components like buttons, forms, modals, and tables.
>
> Its main benefit is consistency. Users get a familiar experience, designers do not need to redesign the same patterns repeatedly, and developers do not create five different versions of the same button.
>
> I prefer using design tokens for values such as colours, spacing, font sizes, border radius, and shadows. For example, instead of hardcoding a blue colour everywhere, we use a named token such as `color-primary`.
>
> Storybook is also useful because it lets designers, developers, and QA see components and their states in one place without needing to open a full application page.

**Easy memory:** *One shared language, fewer inconsistent components.*

---

## 6. How do you handle responsive design?

**Covers:** 14, 15, 16, 58

**Interview answer:**

> I see responsive design as more than making a desktop page smaller. On mobile, the layout, navigation, content order, touch targets, and amount of information may need to change.
>
> I usually build mobile-first where possible, then enhance the layout for larger screens. I test at practical breakpoints and also test in between them, because layouts can break at unusual widths too.
>
> If responsive behaviour is not defined in the design, I clarify the important decisions early—for example, whether a table should scroll, collapse into cards, or show fewer columns on mobile.

**Easy memory:** *Mobile is not a smaller desktop; it is a different context.*

---

## 7. How do you think about UX as a frontend developer?

**Covers:** 31, 32, 33, 34, 35, 36, 37, 38, 39, 40

**Interview answer:**

> UX is about how easy and clear the product feels to use. UI is the visual part—buttons, colours, layouts. UX is the whole experience: whether users understand what to do, whether they get useful feedback, and whether they can recover from mistakes.
>
> As a frontend developer, I think beyond the happy path. For every screen, I consider loading, empty, error, and success states. For forms, I make validation clear and helpful. For slow actions, I show progress so users know the application is working.
>
> For risky actions like deleting something, I make the consequence clear and use confirmation where needed. For long flows such as onboarding or checkout, I keep each step focused and show users where they are in the process.

**Useful example:**

> Instead of showing “Invalid input,” I would show something specific like “Please enter a valid email address.” The user should understand what went wrong and how to fix it.

**Easy memory:** *A good UX answers: What is happening? What should I do? What happens next?*

---

## 8. How do you make sure a design is accessible?

**Covers:** 41–50

**Interview answer:**

> I treat accessibility as part of normal frontend quality, not as a final extra task. I use semantic HTML first—for example, real buttons for actions, labels for inputs, headings in the right order, and proper links for navigation.
>
> I make sure users can use the interface with a keyboard, can see where focus is, and can understand errors. I also check colour contrast and make sure information is not communicated by colour alone.
>
> For more complex components such as modals and dropdowns, I test keyboard navigation and screen-reader behaviour. I use ARIA only when semantic HTML is not enough, because incorrect ARIA can make accessibility worse.

**Easy memory:** *Semantic HTML, keyboard, focus, contrast, clear feedback.*

---

## 9. How do you ensure the implementation matches the design?

**Covers:** 8, 51, 52, 53, 58

**Interview answer:**

> I check both visual quality and real behaviour. I compare the screen with Figma, but I also test different screen sizes, long content, loading states, errors, keyboard use, and browser behaviour.
>
> For important shared UI, visual regression testing can help us catch accidental style changes. For example, if someone changes a shared button or modal, a visual test can show that another page was affected unexpectedly.
>
> I do not aim for pixel perfection at the cost of usability or performance. The goal is a consistent interface that looks right and works well for real users.

**Easy memory:** *Check appearance, behaviour, and edge cases.*

---

## 10. How do you know whether a UX change actually helped users?

**Covers:** 54, 55, 56, 57

**Interview answer:**

> I would first agree on what success means. For example, if we simplify a signup form, success could mean more users complete it, fewer users abandon it, or fewer support requests are raised.
>
> We can use analytics, user feedback, support tickets, usability testing, or A/B testing, depending on the product and the size of the change.
>
> If the feature matches the Figma design but users still find it confusing, I would not defend the design just because it was implemented correctly. I would bring the evidence back to product and design, understand the problem, and improve the experience.

**Easy memory:** *The design is not the final truth; user behaviour is.*

---

## One short senior-level answer you can reuse

If the interviewer asks a broad question such as, “How do you work with UX designers?”, you can say:

> I work with designers early, not only after receiving Figma files. I first understand the user goal, then review the design for responsive behaviour, accessibility, loading, empty, error, and edge cases. I raise technical constraints early and suggest practical alternatives when needed. During implementation, I build reusable components using our design system, and before release I validate the UI against the design and test it in real scenarios. After release, I use feedback and data to improve it if needed.

That one answer covers a large number of UX collaboration questions naturally.


---

# Common questions in different format normally asked

Here are popular senior frontend interview questions around working with UX/design teams, grouped by theme.

### 1. Working with designers

1. How do you collaborate with UX/UI designers during a feature’s lifecycle?
2. When do you involve yourself in the design process?
3. What do you look for when reviewing a Figma design before development?
4. How do you handle a design that is difficult or expensive to implement?
5. What do you do when a design is unclear or missing states?
6. How do you give constructive feedback to a designer?
7. How do you handle disagreements between design, product, and engineering?
8. How do you make sure the final implementation matches the design?
9. How do you communicate technical constraints without blocking creativity?
10. How do you work with designers in an Agile/Scrum team?

### 2. Turning designs into frontend work

11. How do you convert a Figma design into reusable React components?
12. How do you decide what should be a reusable component versus a one-off component?
13. How do you identify variants and states from a design?
14. How do you handle responsive behaviour when only desktop designs are provided?
15. What questions do you ask if mobile/tablet designs are missing?
16. How do you implement spacing, typography, colours, and layout consistently?
17. How do you handle design changes after development has started?
18. How do you estimate a UI task when the design is incomplete?
19. How do you break a design into development tickets or user stories?
20. How do you manage visual regressions when changing shared UI components?

### 3. Design systems and consistency

21. What is a design system, and why is it useful?
22. How have you worked with a component library or design system?
23. How do design tokens help frontend development?
24. What are examples of design tokens?
25. How do you keep Figma components and frontend components aligned?
26. How would you introduce a design system into an existing product?
27. How do you avoid creating many slightly different versions of the same button, modal, or input?
28. How do you document components for both developers and designers?
29. What role can Storybook play when working with UX/design teams?
30. How do you version and safely change shared design-system components?

### 4. UX thinking as a frontend engineer

31. How do you balance pixel-perfect implementation with usability?
32. How do you think about loading, empty, error, and success states?
33. What makes a form experience good or frustrating for users?
34. How do you design helpful validation and error messages?
35. How do you reduce user frustration during slow API calls?
36. How do you make destructive actions, such as deletion, safe and clear?
37. How do you handle long or complex user journeys, such as checkout or onboarding?
38. How do you use progressive disclosure to reduce complexity?
39. What is the difference between UI and UX?
40. How can frontend performance affect UX?

### 5. Accessibility and inclusive design

41. How do you make sure a design is accessible before and during implementation?
42. What accessibility issues do you commonly find in Figma designs?
43. How do you check colour contrast?
44. How do you support keyboard-only users?
45. How do you make modals, dropdowns, and menus accessible?
46. When should you use semantic HTML instead of ARIA?
47. How do you work with designers on focus states?
48. How do you support screen-reader users?
49. How do you handle responsive text sizing and zoom?
50. How do you test accessibility in your frontend work?

### 6. Validation, testing, and improvement

51. How do you perform a UI/UX quality check before release?
52. How do you compare an implementation against Figma?
53. What is visual regression testing, and when would you use it?
54. How do you use user feedback, analytics, or session recordings to improve a UI?
55. What is A/B testing, and what is the frontend engineer’s role in it?
56. How do you measure whether a UX change actually improved the product?
57. How do you handle a feature that matches the design but users still find confusing?
58. How do you ensure UX quality across browsers, devices, and screen sizes?

For senior frontend interviews, the most important areas are usually:

* Handling unclear designs and asking the right questions
* Responsive behaviour and all UI states
* Reusable components and design systems
* Accessibility
* Balancing design quality, performance, and technical constraints
* Collaborating constructively instead of blindly implementing Figma

A strong senior-level answer usually follows this pattern: “I clarify the user goal, review states and edge cases with design, implement reusable accessible components, test against the design across breakpoints, and feed technical or usability issues back early.”

