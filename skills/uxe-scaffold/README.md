# uxe-scaffold

Scaffold a new component for any framework. Auto-detects your project setup.

## Usage

```
/uxe-scaffold NotificationBanner
/uxe-scaffold StatusBadge
/uxe-scaffold UserAvatarGroup
```

**Syntax:** `/uxe-scaffold <ComponentName>`

## What it generates

Four files, matched to your project's framework and tooling:

| File | Description |
|------|-------------|
| `ComponentName.tsx` (or `.vue`, `.svelte`, etc.) | Component implementation |
| `ComponentName.test.ts` | Unit tests for your detected test runner |
| `ComponentName.stories.ts` | Storybook stories (if Storybook detected) |
| `index.ts` | Barrel export |

## What it auto-detects

Before generating, the skill inspects your project for:

- **Framework** — React, Vue 3, Angular, Svelte, Web Components
- **TypeScript** — adds types if detected
- **Storybook** — generates stories file if detected
- **Test runner** — Vitest, Jest, or Testing Library
- **Components directory** — where to put the new files

## Framework-specific output

**React** — `forwardRef`, exported `ComponentNameProps` interface, `displayName`

**Vue 3** — `<script setup>` with `defineProps` and `defineEmits`, TypeScript interface

**Angular** — standalone component with `@Component` decorator

**Svelte** — `<script lang="ts">` with exported props

**Web Components** — `HTMLElement` extension with `observedAttributes`

## Installation

```bash
cp -r skills/uxe-scaffold ~/.claude/skills/
```

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill file with YAML frontmatter and framework instructions |
| `README.md` | This file |
