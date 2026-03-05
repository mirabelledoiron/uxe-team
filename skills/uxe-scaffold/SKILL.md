---
name: uxe-scaffold
description: Scaffold a new design system component with all required files — component, types, tests, and documentation stub. Adapts to the project's framework and styling approach automatically.
argument-hint: <ComponentName> [framework]
disable-model-invocation: true
---

# Component Scaffold

Generate all files needed to add a new component to the design system.

## Usage

```
/uxe-scaffold Button
/uxe-scaffold CardGroup react
/uxe-scaffold NavigationMenu vue
/uxe-scaffold Badge angular
```

## Detected Project Context

- Framework: !`node -e "try{const p=require('./package.json');const d={...p.dependencies,...p.devDependencies};['react','vue','angular','svelte','lit'].filter(k=>d[k]).forEach(k=>console.log(k))}catch(e){console.log('unknown')}" 2>/dev/null || echo "unknown"`
- TypeScript: !`ls tsconfig.json 2>/dev/null && echo "yes" || echo "no"`
- Storybook: !`ls .storybook 2>/dev/null && echo "yes" || echo "no"`
- Test framework: !`node -e "try{const p=require('./package.json');const d={...p.dependencies,...p.devDependencies};['vitest','jest','@testing-library/react'].filter(k=>d[k]).forEach(k=>console.log(k))}catch(e){}" 2>/dev/null || echo "not detected"`
- Components directory: !`ls -d src/components components lib/components packages/ui/src 2>/dev/null | head -1 || echo "src/components"`
- Token file: !`find . -maxdepth 4 \( -name "tokens.css" -o -name "tokens.json" -o -name "design-tokens.json" \) 2>/dev/null | grep -v node_modules | head -1 || echo "not found"`

## Component Name

$ARGUMENTS

## Instructions

Using the detected context above, generate a complete, production-ready component scaffold for **$ARGUMENTS**.

### Step 1: Confirm the component location

Place new components in the detected components directory. If none was found, use `src/components/$ARGUMENTS/`.

### Step 2: Generate these files

#### `[ComponentName].tsx` (or `.vue`, `.svelte` per framework)

- Props interface with TypeScript types (if TS detected)
- `variant` prop: `'default' | 'primary' | 'secondary' | 'ghost' | 'destructive'` (include only what makes sense for this component)
- `size` prop: `'sm' | 'md' | 'lg'` (if applicable)
- `disabled` prop: boolean
- `className` prop for extension (React) or `class` (Vue/Svelte)
- All tokens referenced as CSS custom properties or Tailwind classes — never hardcoded values
- Accessible by default: correct HTML element, ARIA attributes, keyboard support
- `displayName` set (React) or `name` option (Vue)
- `forwardRef` for React if the component is a DOM wrapper

#### `[ComponentName].test.tsx` (or appropriate extension)

- Renders without crashing
- Renders all variants
- Renders all sizes
- Disabled state behavior
- Keyboard interaction (if interactive)
- Accessibility check (use `@testing-library/jest-dom` or `axe-core`)
- Snapshot test (optional, only if team uses snapshots)

#### `[ComponentName].stories.tsx` (only if Storybook detected)

- Default story showing all props
- Story per variant
- Story per size
- Story for disabled state
- Story for error/loading state (if applicable)
- `argTypes` configured for interactive controls

#### `index.ts`

- Named export of the component
- Named export of the props type
- Re-export from parent `index.ts` at the components root

### Step 3: After generating files

Print a summary:
```
Created:
  src/components/[ComponentName]/
    [ComponentName].tsx           — component
    [ComponentName].test.tsx      — tests
    [ComponentName].stories.tsx   — Storybook (if applicable)
    index.ts                      — exports

Next steps:
  1. Add token values if not already in your token file
  2. Run tests: [appropriate test command]
  3. View in Storybook: [appropriate command]
  4. Use uxe-bridge to generate the full component spec
  5. Use uxe-a11y agent to audit accessibility
```

## Framework-Specific Notes

### React
- Use `React.forwardRef` for all DOM-wrapping components
- Props type named `[ComponentName]Props`, exported
- Default export the component, named export the type

### Vue 3
- Use Composition API with `<script setup lang="ts">`
- `defineProps` with types, `defineEmits` for events
- `defineExpose` only for public imperative APIs

### Angular
- `@Component` decorator with `standalone: true`
- `Input()` for props, `Output()` and `EventEmitter` for events
- Use `ChangeDetectionStrategy.OnPush`

### Svelte
- TypeScript via `<script lang="ts">`
- Props via `export let` syntax
- Forward events with `on:click` and rest props with `{...$$restProps}`

### Web Components (Lit)
- Extend `LitElement`
- `@property` decorator for observed attributes
- Shadow DOM for style encapsulation
