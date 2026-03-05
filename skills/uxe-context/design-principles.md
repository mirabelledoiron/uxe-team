# UXE Design Principles

This is the knowledge base for UX Engineering work. It captures the *reasoning* behind design decisions — not just the rules, but the *why*. A UXE who understands the why can make good judgment calls when the spec is incomplete.

---

## The UXE Role

A UX Engineer is a front-end engineer with working knowledge of UX design principles. They are not:
- A full UX designer (no user research, no information architecture)
- A backend engineer (no middleware, no APIs)
- A pixel-perfect implementer (they understand *why*, not just *what*)

They are:
- The person who can read a Figma file and ask the right engineering questions
- The person who can explain to a designer why a CSS animation needs to be GPU-accelerated
- The person who builds the design system that everyone else uses
- The translator between two different professional languages

**Primary domain:** The UI component layer — the boundary between raw data and visual presentation.

---

## The Three Pillars of a Design System

### 1. Design Language

The visual foundation — assets and guidelines that define brand identity:

- **Color palette** — primary, secondary, neutral, semantic (success/warning/error/info), surface
- **Typography scale** — font families, sizes, weights, line heights, letter spacing
- **Spacing system** — usually 4pt or 8pt grid (4, 8, 12, 16, 24, 32, 48, 64...)
- **Motion library** — duration tokens, easing curves, keyframe animations
- **Accessibility guidelines** — contrast requirements, touch target sizes, focus indicators

### 2. Component Library

The design language in code. Components are built in the project's framework (React, Vue, Angular, Svelte, Web Components) and consume design language exclusively through tokens — never hardcoded values.

Component anatomy:
- **Atoms** — Button, Input, Icon, Badge, Label (cannot be broken down further)
- **Molecules** — FormField, SearchBar, Card, ListItem (atoms combined)
- **Organisms** — Header, DataTable, Modal, Navigation (molecules combined)
- **Templates** — full page layouts using organisms

### 3. Style Guide

The documentation website that lives between design and engineering. It must serve both audiences simultaneously:
- Designers: visual reference, usage guidelines, do/don't examples
- Engineers: props API, code examples, token reference, installation instructions

Gold standard reference: IBM Carbon Design System

---

## Visual Design Principles: The Reasoning

These are the principles a UXE must understand at the *reasoning* level, not just as rules.

### Typography

**Left-align body text (in LTR languages)**
The eye returns to the same left margin at the start of each line. Centered text creates a jagged left edge — the eye has to search for where the next line starts. This causes fatigue on anything longer than 3 lines. Right-to-left languages (Arabic, Hebrew) justify to the right for the same reason.

**50–70 characters per line maximum**
Beyond 70 characters, the eye struggles to track back to the start of the next line. Below 45 characters, the eye has to move so frequently it breaks reading rhythm. This is why readable prose has optimal column widths.

**Type scale ratios (1.25x Major Third is most common)**
A scale ratio ensures visual harmony between heading sizes. Arbitrary sizes feel disconnected. The ratio creates a predictable visual hierarchy. Common ratios: 1.25 (Major Third), 1.333 (Perfect Fourth), 1.5 (Perfect Fifth — more dramatic).

**Line height 1.4–1.6 for body text**
Tight line height (1.0–1.2) makes long-form text claustrophobic. Too loose (2.0+) makes it feel disconnected. 1.5 is the web standard for readability.

**Font weight for hierarchy, not just size**
Weight changes are more visually efficient than size changes at small scales. A 16px Bold heading reads as more important than a 20px Regular one.

### Color

**Dark text on light backgrounds (not vice versa)**
The human eye processes dark-on-light more efficiently than light-on-dark. Light text on dark backgrounds creates a "bloom" effect — the white pixels bleed into the surrounding dark area. Dark mode works because it reduces eye strain in low-light environments, not because light-on-dark is inherently more readable.

**Never place text on background images without treatment**
A white image has light areas. White text on a light area = invisible. The image changes — the text doesn't adapt. Always use one of: background overlay (semi-transparent layer), drop shadow (on the text itself), reduced image contrast/opacity, or a solid text area. The same applies for dark text.

**WCAG contrast ratios**
- AA (minimum): 4.5:1 for normal text, 3:1 for large text (18pt+ or 14pt+ bold)
- AAA (enhanced): 7:1 for normal text, 4.5:1 for large text
- UI components and graphical objects: 3:1 minimum

The ratio is calculated as (lighter color + 0.05) / (darker color + 0.05).

**Color scales (50–900)**
A complete color scale gives engineers range to work with. The 500 step is typically the base/brand color. Steps below 500 are lighter (backgrounds, subtle UI). Steps above 500 are darker (hover states, text on light backgrounds). Having the full scale prevents engineers from inventing arbitrary shades.

**Semantic color tokens**
Never expose raw color tokens to component code. Map them to semantic intent:
- `color-brand-500` (primitive) → `color-action-primary` (semantic) → `button-background-default` (component)
This way, a brand refresh changes one primitive token and the entire system updates.

### Spacing

**8pt grid system**
Spacing values that are multiples of 8 (8, 16, 24, 32, 48, 64) create visual rhythm. 4pt grid adds half-steps (4, 8, 12, 16, 20, 24...) for finer control. Arbitrary spacing (13px, 22px) creates visual noise that users feel even if they can't name it.

**Consistent internal vs external spacing**
Internal spacing (padding within a component) should feel tighter than external spacing (margin between components). A card with 16px internal padding should have 24–32px margin from adjacent cards.

**Touch targets: 44x44px minimum**
WCAG 2.5.8 and Apple HIG both specify 44x44px as the minimum interactive target size on touch screens. A visually small button (24px icon) needs invisible padding to meet this. Designers frequently specify visual size — engineers must account for touch target separately.

### Layout

**Responsive design is not just "make it smaller"**
Each breakpoint is a different context. Mobile is not a shrunken desktop. Navigation patterns change (hamburger vs sidebar vs tabs). Content priority changes. Touch vs mouse interaction changes. A component spec must address each breakpoint as a distinct layout, not just scaled dimensions.

**Standard breakpoints**
- xs: 0–479px (small phones)
- sm: 480–639px (large phones)
- md: 640–767px (tablets portrait)
- lg: 768–1023px (tablets landscape / small laptops)
- xl: 1024–1279px (desktops)
- 2xl: 1280px+ (large screens)

**Z-index system**
Without a defined z-index scale, engineers invent values (z-index: 9999). Define a semantic scale: base (0), raised (1), dropdown (100), sticky (200), overlay (300), modal (400), toast (500), tooltip (600).

---

## Token Architecture

### The Three-Level Hierarchy

```
Primitive tokens      →   Semantic tokens       →   Component tokens
(the raw values)          (the meaning)              (the usage)

color-blue-500        →   color-action-primary  →   button-bg-default
color-blue-700        →   color-action-hover    →   button-bg-hover
color-neutral-900     →   color-text-primary    →   button-label-color
spacing-4             →   spacing-component-sm  →   button-padding-y
```

**Why this matters:** When your brand color changes, you update `color-blue-500`. Every semantic and component token that references it updates automatically. Without this hierarchy, a color change requires finding and updating hundreds of hardcoded values.

### Token Naming Conventions

Consistent naming pattern: `[category]-[property]-[variant]-[state]`

Examples:
- `color-text-primary` — color category, text property, primary variant
- `color-text-primary-disabled` — same, disabled state
- `spacing-4` — spacing category, scale step 4
- `shadow-md` — shadow category, medium variant
- `font-size-lg` — typography category, large size

### Output Formats

The same token set can be consumed in multiple formats:
- **CSS custom properties** — `:root { --color-action-primary: #0066CC; }`
- **SCSS variables** — `$color-action-primary: #0066CC;`
- **JavaScript/TypeScript** — `export const colorActionPrimary = '#0066CC'`
- **Tailwind config** — `theme.extend.colors.action.primary`
- **Style Dictionary** — platform-agnostic source, transforms to any format
- **Figma Tokens / Token Studio** — JSON format synced with Figma

---

## Accessibility Fundamentals

### Semantic HTML First

The single most impactful accessibility decision is using the right HTML element. A `<button>` gets keyboard focus, Enter/Space activation, and the `button` ARIA role for free. A `<div onClick>` gets none of these.

Common semantic HTML patterns for components:
- Interactive → `<button>` (not div/span)
- Navigation → `<nav>` with `<ul>/<li>/<a>`
- Form fields → `<label>` associated with `<input>` via `for`/`id`
- Headings → `<h1>`–`<h6>` in hierarchical order (never skip levels)
- Main content → `<main>` (one per page)
- Sectioning → `<section>`, `<article>`, `<aside>`, `<header>`, `<footer>`

### ARIA: Use Sparingly

ARIA should supplement semantic HTML, not replace it. The first rule of ARIA: don't use ARIA if a native HTML element does the job.

Essential ARIA patterns:
- `aria-label` — accessible name for elements without visible text (icon buttons)
- `aria-labelledby` — connects a label to a complex component
- `aria-describedby` — connects descriptive text (error messages, hints)
- `aria-expanded` — toggle state for accordions, dropdowns, menus
- `aria-selected` — selection state for tabs, listboxes
- `aria-disabled` — communicates disabled state to screen readers
- `aria-live` — announces dynamic content changes (toast, form validation)
- `role="dialog"` + `aria-modal="true"` — modal dialogs
- `role="status"` — non-urgent announcements
- `role="alert"` — urgent announcements (errors)

### Focus Management

- All interactive elements must be reachable via Tab key
- Focus order must follow visual reading order
- Focus indicator must be visible (never `outline: none` without a custom replacement)
- Modal dialogs must trap focus inside when open and restore focus on close
- Skip navigation links at page top for keyboard users

### Keyboard Interaction Patterns

| Component | Keys |
|-----------|------|
| Button | Enter, Space to activate |
| Link | Enter to follow |
| Checkbox | Space to toggle |
| Radio group | Arrow keys to move between options |
| Select/Dropdown | Enter to open, Arrow keys to navigate, Enter/Escape to close |
| Tabs | Arrow keys between tabs, Enter to activate |
| Modal | Escape to close, Tab trapped inside |
| Accordion | Enter/Space to toggle |
| Combobox | Arrow keys to navigate list, Enter to select, Escape to close |

---

## Component States Checklist

Every interactive component must specify behavior for all applicable states. Designers most commonly forget states below the fold.

**Visual states (always required):**
- Default
- Hover (mouse over)
- Active (mouse down / being pressed)
- Focus (keyboard focused)
- Focus-visible (keyboard focus specifically, distinct from :focus)
- Disabled

**Conditional states (as applicable):**
- Loading (async operation in progress)
- Error (validation failed, operation failed)
- Success (operation completed)
- Empty (no data, no content)
- Selected / checked
- Indeterminate (partial selection)
- Read-only

---

## The Designer-Engineer Translation Map

These are the questions a UXE asks at handoff. If a design spec doesn't answer these, the implementation will drift.

| Design says | Engineering needs to know |
|-------------|--------------------------|
| "Use the brand color" | Which token? `color-action-primary`? Or `color-brand-500`? |
| "Small version" | What are the exact dimensions? Is it a `size` prop or a separate component? |
| "Rounded corners" | `border-radius-sm` (4px) or `border-radius-md` (8px)? Token name? |
| "Subtle shadow" | Which shadow token? `shadow-sm`? What are the exact values? |
| "It should animate" | Duration? Easing? Which properties? Reduce-motion fallback? |
| "Same as [X] but [Y]" | Is this a variant of X (same component, different props) or a new component? |
| "Responsive" | What changes at each breakpoint? Layout? Content? Behavior? |
| "Accessible" | Which ARIA roles? Keyboard behavior? Focus management? |
| "Error state" | What triggers it? What's the error message? Where does it appear? |
| "Loading state" | What triggers it? Duration estimate? Skeleton or spinner? |
