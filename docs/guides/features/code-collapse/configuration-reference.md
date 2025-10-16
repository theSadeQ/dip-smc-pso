# Configuration Reference

**Last Updated:** 2025-10-12

---

## CONFIG Object (JavaScript)

Located in `code-collapse.js` (lines 21-28)

### storageKey

```javascript
storageKey: 'code-block-states'
```

- **Type:** `string`
- **Default:** `'code-block-states'`
- **Description:** LocalStorage key for persisting collapse states
- **Change if:** You have multiple docs sites on same domain (avoid key collision)

### animationDuration

```javascript
animationDuration: 350
```

- **Type:** `number` (milliseconds)
- **Default:** `350`
- **Valid Range:** 100-1000ms
- **Description:** Duration of collapse/expand animation
- **Recommended:** 300-500ms (too fast = jarring, too slow = sluggish)

### easing

```javascript
easing: 'cubic-bezier(0.4, 0.0, 0.2, 1)'
```

- **Type:** `string` (CSS timing function)
- **Default:** `'cubic-bezier(0.4, 0.0, 0.2, 1)'` (Material Design standard easing)
- **Alternatives:**
  - `'linear'` - constant speed
  - `'ease-in-out'` - slow start/end
  - `'cubic-bezier(0.68, -0.55, 0.265, 1.55)'` - bounce effect
- **Tool:** https://cubic-bezier.com

### expandedIcon

```javascript
expandedIcon: '▼'
```

- **Type:** `string` (Unicode character or emoji)
- **Default:** `'▼'` (down triangle)
- **Examples:** `'➖'`, `'[-]'`, `'🔽'`
- **Note:** Use single character for best visual alignment

### collapsedIcon

```javascript
collapsedIcon: '▲'
```

- **Type:** `string` (Unicode character or emoji)
- **Default:** `'▲'` (up triangle)
- **Examples:** `'➕'`, `'[+]'`, `'🔼'`

### buttonTitle

```javascript
buttonTitle: 'Toggle code block'
```

- **Type:** `string`
- **Default:** `'Toggle code block'`
- **Description:** Tooltip text shown on button hover
- **Change for:** Localization or custom messaging

---

## Selectors Array (JavaScript)

Located in `code-collapse.js` (lines 43-50)

### Default Selectors

```javascript
const selectors = [
    'div.notranslate[class*="highlight-"]',      // Primary language blocks
    'div[class*="highlight-"]:not(.nohighlight)', // Catch-all edge cases
    'div.doctest',                                // Python doctest blocks
    'div.literal-block',                          // reST literal blocks
    'div.code-block',                             // code-block directive
    'pre.literal-block'                           // Pre-formatted blocks
];
```

### Adding Custom Selector

```javascript
const selectors = [
    // ... existing selectors ...
    'div.my-custom-code-class',  // Your custom selector
];
```

**Test after adding:** Check console for 100% coverage message.

---

## CSS Customization

### Button Appearance

**File:** `code-collapse.css` (lines 65-80)

```css
.code-collapse-btn {
    position: absolute;
    top: 8px;           /* Distance from top */
    right: 8px;         /* Distance from right */
    padding: 4px 8px;   /* Button padding */
    opacity: 0.3;       /* Default opacity (subtle) */
    /* ... */
}

.code-collapse-btn:hover {
    opacity: 1.0;       /* Hover opacity (visible) */
    /* ... */
}
```

### Button Gap (Sibling Spacing)

**File:** `code-collapse.css` (lines 104-106)

```css
.copybtn + .code-collapse-btn {
    margin-left: 8px;   /* Gap between copy and collapse buttons */
}
```

- **Desktop:** 8px (default)
- **Mobile (< 768px):** 5px (line 250)

### Master Controls Styling

**File:** `code-collapse.css` (lines 10-21)

```css
.code-controls-master {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(99, 102, 241, 0.05));
    border: 2px solid rgba(59, 130, 246, 0.3);
    padding: 12px 16px;
    margin: 1.5rem 0;
    /* ... */
}
```

**Customize colors:**
- Background gradient: Change `rgba()` values
- Border color: Change `border` property
- Button colors: Lines 31-45 (`.code-control-btn`)

### Dark Mode Customization

**File:** `code-collapse.css` (lines 181-203)

```css
[data-theme="dark"] .code-controls-master {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(99, 102, 241, 0.1));
    border-color: rgba(59, 130, 246, 0.4);
}

[data-theme="dark"] .code-collapse-btn {
    background: transparent;
    color: inherit;
    opacity: 0.3;
}
```

**Note:** Adjust for your theme's dark mode colors.

---

## Exclusion Rules (JavaScript)

Located in `shouldSkipBlock()` function (lines 113-128)

### Default Exclusions

```javascript
function shouldSkipBlock(element) {
    // Skip math blocks
    if (element.classList.contains('nohighlight')) return true;
    if (element.classList.contains('amsmath')) return true;
    if (element.classList.contains('math')) return true;

    // Skip if no code content
    const preElement = element.querySelector('pre');
    if (!preElement) return true;

    // Skip very short blocks (<10 characters)
    const content = preElement.textContent.trim();
    if (content.length < 10) return true;

    return false;
}
```

### Adding Custom Exclusion

```javascript
function shouldSkipBlock(element) {
    // ... existing exclusions ...

    // Add custom exclusion
    if (element.classList.contains('no-collapse')) return true;

    return false;
}
```

---

## Performance Settings

### GPU Acceleration (CSS)

**File:** `code-collapse.css` (lines 114-131)

```css
div[class*="highlight"] {
    contain: layout;  /* Prevent layout shifts - can disable if issues */
}

div.highlight {
    transform: translateZ(0);           /* Force GPU layer - disable if GPU issues */
    backface-visibility: hidden;        /* Smooth rendering - can disable */
}

div[class*="highlight"] pre {
    will-change: max-height, opacity;   /* Performance hint - can disable */
}
```

**Disable if:** GPU acceleration causes issues on low-end devices.

### Animation Optimization

**Disable will-change if memory constrained:**
```css
div[class*="highlight"] pre {
    /* will-change: max-height, opacity; */ /* Commented out */
}
```

**Disable GPU acceleration if glitchy:**
```css
div.highlight {
    /* transform: translateZ(0); */
    /* backface-visibility: hidden; */
}
```

---

## Browser Compatibility Matrix

| Feature | Chrome 90+ | Firefox 88+ | Edge 90+ | Safari 14+ |
|---------|-----------|-------------|----------|-----------|
| Core functionality | ✅ | ✅ | ✅ | ✅ |
| `requestAnimationFrame` | ✅ | ✅ | ✅ | ✅ |
| `cubic-bezier()` | ✅ | ✅ | ✅ | ✅ |
| `localStorage` | ✅ | ✅ | ✅ | ✅ |
| `contain: layout` | ✅ Full | ⚠️ Partial | ✅ Full | ⚠️ Limited |
| `will-change` | ✅ | ✅ | ✅ | ✅ |
| `backface-visibility` | ✅ | ✅ | ✅ | ✅ |

**Legend:**
- ✅ Full support
- ⚠️ Partial/limited support (feature still works)
- ❌ Not supported

---

## Recommended Settings by Use Case

### Minimal Animation (Accessibility-Focused)

```javascript
// CONFIG
animationDuration: 200  // Faster
easing: 'linear'        // Simple

// CSS - Disable GPU features
// Comment out: contain, transform, will-change
```

### Maximum Performance (Modern Browsers)

```javascript
// CONFIG
animationDuration: 350  // Default
easing: 'cubic-bezier(0.4, 0.0, 0.2, 1)'  // Material Design

// CSS - Keep all GPU features enabled (default)
```

### Legacy Browser Support (Older Devices)

```javascript
// CONFIG
animationDuration: 400  // Slightly slower
easing: 'ease-in-out'   // Standard CSS

// CSS - Disable advanced features
// Comment out: contain, transform, backface-visibility, will-change
```

---

**For full technical details, see:** [technical-reference.md](technical-reference.md)
