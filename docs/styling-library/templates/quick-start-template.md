# React Bits - Quick Start Guide

Get started with React Bits components in 3 minutes! 

##  What You Have

**115+ animated React components** organized in 4 categories:
-  **25 Animations** - Interactive effects
-  **24 Text Animations** - Typography effects
-  **36 UI Components** - Interface elements
-  **30 Backgrounds** - Animated backgrounds

##  3 Ways to Use Components

### Method 1: Browse & Copy (Recommended)

1. Open the index: [`COMPONENTS_INDEX.md`](./COMPONENTS_INDEX.md)
2. Find a component you like (e.g., "ShinyText")
3. Navigate to: `src/content/TextAnimations/ShinyText/`
4. Copy the component files to your project

### Method 2: Just Ask Claude

Simply say:
> "Add the **MagicBento** component from React Bits"

Claude will automatically find and integrate it!

### Method 3: Install the Package

```bash
npm install react-bits
```

##  Popular Components for Your Dashboard

### Best for Hero Sections

```
 Aurora - Aurora borealis background
 GradientText - Animated gradient text
 ShinyText - Shiny text effect
 LiquidChrome - Liquid chrome background
```

### Best for Cards & Lists

```
 BounceCards - Bouncing card effects
 MagicBento - Bento grid layout
 TiltedCard - 3D tilt effect
 AnimatedList - List with transitions
```

### Best for Navigation

```
 Dock - macOS-style dock
 PillNav - Pill navigation
 BubbleMenu - Bubble menu
 FlowingMenu - Flowing menu animation
```

### Best for Text Effects

```
 GlitchText - Glitch animation
 ScrambledText - Scramble effect
 TextType - Typewriter effect
 GradientText - Gradient animation
```

### Best for Backgrounds

```
 Galaxy - Space effect
 Lightning - Electric effects
 Waves - Wave patterns
 Particles - Particle system
```

##  Component Structure

Each component folder contains:
```
ComponentName/
 component.tsx    # Main component code
 demo.tsx        # Usage example
 README.md       # Documentation
```

##  Quick Examples

### Example 1: Add ShinyText to Dashboard

```tsx
// 1. Copy from: src/content/TextAnimations/ShinyText/component.tsx
// 2. Paste to: your-project/components/ShinyText.tsx
// 3. Use it:

import ShinyText from '@/components/ShinyText'

export default function Dashboard() {
  return (
    <div>
      <ShinyText text="I'm OK - You're OK" />
    </div>
  )
}
```

### Example 2: Add Aurora Background

```tsx
// 1. Copy from: src/content/Backgrounds/Aurora/component.tsx
// 2. Paste to: your-project/components/Aurora.tsx
// 3. Use it:

import Aurora from '@/components/Aurora'

export default function Page() {
  return (
    <div className="relative">
      <Aurora className="absolute inset-0 -z-10" />
      <div className="relative z-10">
        {/* Your content */}
      </div>
    </div>
  )
}
```

### Example 3: Add MagicBento Grid

```tsx
// 1. Copy from: src/content/Components/MagicBento/component.tsx
// 2. Paste to: your-project/components/MagicBento.tsx
// 3. Use it:

import MagicBento from '@/components/MagicBento'

export default function Dashboard() {
  const items = [
    { title: "Progress", content: "Your stats here" },
    { title: "Charts", content: "Your charts here" }
  ]

  return <MagicBento items={items} />
}
```

##  Dependencies

Most components work with minimal dependencies. Common requirements:

### Framer Motion Components

```bash
npm install framer-motion
```

### GSAP Components

```bash
npm install gsap
```

### React Spring Components

```bash
npm install @react-spring/web
```

### Three.js Components (3D effects)

```bash
npm install three @react-three/fiber @react-three/drei
```

> **Pro Tip**: Check the component's `README.md` for specific dependencies!

##  Styling

Components support both:
-  **Tailwind CSS** (default)
-  **Vanilla CSS** (alternative)

Your dashboard already uses Tailwind, so you're good to go!

##  Finding Components

### By Name

Use the alphabetical index in `COMPONENTS_INDEX.md`

### By Category

Browse directories:
- `src/content/Animations/`
- `src/content/TextAnimations/`
- `src/content/Components/`
- `src/content/Backgrounds/`

### By Use Case

Check the "By Use Case" section in the index

##  Integration Checklist

When adding a component to your dashboard:

- [ ] Find component in `COMPONENTS_INDEX.md`
- [ ] Navigate to `src/content/[Category]/[ComponentName]/`
- [ ] Read the `README.md` for requirements
- [ ] Copy `component.tsx` to your project
- [ ] Install any required dependencies
- [ ] Import and use in your page
- [ ] Customize props and styling

##  Pro Tips

1. **Start Small**: Begin with text animations (easiest)
2. **Check Demos**: Look at `demo.tsx` for usage examples
3. **Mix & Match**: Combine multiple components
4. **Customize**: All components accept className props
5. **Performance**: Use lazy loading for heavy components

##  Next Steps

1. Browse the full index → [`COMPONENTS_INDEX.md`](./COMPONENTS_INDEX.md)
2. Check integration guide → [`INTEGRATION_GUIDE.md`](./INTEGRATION_GUIDE.md)
3. Explore component files → `src/content/`
4. Visit official docs → [reactbits.dev](https://reactbits.dev)

##  Example: Enhanced Dashboard Header

```tsx
import ShinyText from '@/components/ShinyText'
import Aurora from '@/components/Aurora'

export default function Dashboard() {
  return (
    <div className="relative min-h-screen">
      {/* Aurora background */}
      <Aurora className="absolute inset-0 -z-10" />

      {/* Header with ShinyText */}
      <div className="relative z-10 text-center py-20">
        <ShinyText
          text="I'm OK - You're OK"
          className="text-6xl font-bold"
        />
      </div>

      {/* Rest of your dashboard */}
    </div>
  )
}
```



**Ready to build stunning UIs!** 

Just say: "Add [ComponentName] from React Bits" and Claude will handle the rest!
