# Deep Performance Analysis Prompt (For Puppeteer + Chrome DevTools Protocol)

**Context:** LCP improved from 7.6s to 5.5s (27%) after removing heavyweight JS, but expected 89% improvement. Need to identify remaining bottlenecks preventing <2.5s target.

**Tools Available:**
- Puppeteer MCP server (mcp__puppeteer__)
- Chrome DevTools Protocol (CDP) via puppeteer
- Chrome Coverage API
- Performance trace capture

---

## Comprehensive Analysis Prompt

```
I need you to perform a deep performance analysis of http://localhost:9000 using Puppeteer and Chrome DevTools Protocol to identify why LCP is 5.5s instead of the expected <1.0s.

Context:
- Removed 1.7 MB of JavaScript (Pyodide, Plotly, Three.js)
- Expected 89% LCP improvement (7.6s → 0.8s)
- Actual: 27% improvement (7.6s → 5.5s)
- Hypothesis: CSS blocking is now primary bottleneck

Please use the mcp__puppeteer__ tools to:

## Phase 1: Coverage Analysis (Identify Unused Code)

1. Navigate to http://localhost:9000
2. Start CSS coverage tracking
3. Start JavaScript coverage tracking
4. Wait for page load (networkidle0)
5. Stop coverage and report:
   - Total CSS bytes loaded vs used
   - Total JS bytes loaded vs used
   - Specific files with >50% unused code
   - Line-by-line breakdown for custom.css

Example approach:
```javascript
// Use mcp__puppeteer__puppeteer_evaluate with this script:
const [jsCoverage, cssCoverage] = await Promise.all([
  page.coverage.startJSCoverage(),
  page.coverage.startCSSCoverage()
]);

await page.goto('http://localhost:9000', { waitUntil: 'networkidle0' });

const [jsReport, cssReport] = await Promise.all([
  page.coverage.stopJSCoverage(),
  page.coverage.stopCSSCoverage()
]);

// Calculate unused CSS
let totalCSSBytes = 0;
let usedCSSBytes = 0;
for (const entry of cssReport) {
  totalCSSBytes += entry.text.length;
  for (const range of entry.ranges) {
    usedCSSBytes += range.end - range.start;
  }
}

console.log('CSS Usage:');
console.log(`Total: ${(totalCSSBytes/1024).toFixed(1)} KB`);
console.log(`Used: ${(usedCSSBytes/1024).toFixed(1)} KB`);
console.log(`Unused: ${((totalCSSBytes-usedCSSBytes)/1024).toFixed(1)} KB (${((1-usedCSSBytes/totalCSSBytes)*100).toFixed(1)}%)`);

// Same for JS...
```

## Phase 2: Performance Trace Analysis (Identify Blocking)

1. Start performance trace with categories: 'devtools.timeline', 'disabled-by-default-devtools.timeline'
2. Navigate to http://localhost:9000
3. Stop trace and analyze:
   - Time to First Paint (when first pixel rendered)
   - Time to First Contentful Paint (when first content rendered)
   - Largest Contentful Paint element and timing
   - Main thread blocking time breakdown:
     * JavaScript parsing/execution: X ms
     * CSS parsing/style calculation: X ms
     * Layout: X ms
     * Paint: X ms
   - Network waterfall showing blocking relationships

Example approach:
```javascript
// Use CDP via puppeteer evaluate:
const client = await page.target().createCDPSession();
await client.send('Tracing.start', {
  categories: 'devtools.timeline,disabled-by-default-devtools.timeline',
  options: 'sampling-frequency=10000'
});

await page.goto('http://localhost:9000', { waitUntil: 'networkidle0' });

const traceData = await client.send('Tracing.end');
// Analyze traceData events...

// Find LCP element timing
const lcpEvents = traceData.filter(e => e.name === 'largestContentfulPaint::Candidate');
const lcpTime = lcpEvents[lcpEvents.length - 1]?.args?.data?.candidateIndex;

console.log(`LCP occurred at: ${lcpTime}ms`);
console.log(`LCP element:`, lcpEvents[lcpEvents.length - 1]?.args?.data?.nodeId);
```

## Phase 3: Resource Timing Analysis

1. Capture detailed resource timing for all resources
2. Identify render-blocking resources (CSS, sync JS)
3. Calculate impact of each blocking resource:
   - Download time
   - Parse time
   - Blocking duration

Example approach:
```javascript
const resourceTiming = await page.evaluate(() => {
  return performance.getEntriesByType('resource').map(entry => ({
    name: entry.name,
    type: entry.initiatorType,
    startTime: entry.startTime,
    duration: entry.duration,
    transferSize: entry.transferSize,
    renderBlockingStatus: entry.renderBlockingStatus || 'unknown'
  }));
});

// Sort by blocking impact
const blockingResources = resourceTiming
  .filter(r => r.renderBlockingStatus === 'blocking')
  .sort((a, b) => b.duration - a.duration);

console.log('Top 5 Render-Blocking Resources:');
blockingResources.slice(0, 5).forEach(r => {
  console.log(`${r.duration.toFixed(0)}ms - ${r.name.split('/').pop()} (${(r.transferSize/1024).toFixed(1)} KB)`);
});
```

## Phase 4: Critical Rendering Path Analysis

1. Identify what's preventing first paint
2. Calculate critical path length
3. Determine which resources MUST load before render

Example questions to answer:
- How many CSS files block rendering?
- What's the total blocking time from CSS?
- Are fonts blocking render?
- Is document parsing blocked by scripts?

## Phase 5: Main Thread Analysis

1. Capture main thread activity breakdown
2. Identify long tasks (>50ms)
3. Report JavaScript execution time by script

Example approach:
```javascript
const metrics = await page.evaluate(() => {
  return {
    navigationTiming: performance.getEntriesByType('navigation')[0],
    paintTiming: performance.getEntriesByType('paint'),
    longTasks: performance.getEntriesByType('longtask')
  };
});

console.log('Main Thread Analysis:');
console.log(`DOM Content Loaded: ${metrics.navigationTiming.domContentLoadedEventEnd - metrics.navigationTiming.domContentLoadedEventStart}ms`);
console.log(`Load Event: ${metrics.navigationTiming.loadEventEnd - metrics.navigationTiming.loadEventStart}ms`);
console.log(`First Paint: ${metrics.paintTiming.find(p => p.name === 'first-paint')?.startTime}ms`);
console.log(`First Contentful Paint: ${metrics.paintTiming.find(p => p.name === 'first-contentful-paint')?.startTime}ms`);
console.log(`Number of Long Tasks: ${metrics.longTasks.length}`);
```

## Phase 6: CSS Analysis (Detailed)

1. List all CSS files loaded
2. For each CSS file:
   - Size (transfer vs uncompressed)
   - Parse time
   - Used vs unused rules
   - Blocking duration
3. Identify opportunities:
   - Unused CSS to remove
   - CSS to defer
   - CSS to inline (critical path)

## Expected Output Format

Please provide a structured report with:

### 1. Coverage Summary
```
CSS Usage:
- custom.css: 140 KB total, 25 KB used (82% unused)
- furo.css: 85 KB total, 60 KB used (29% unused)
- TOTAL: 225 KB total, 85 KB used (62% UNUSED)

JavaScript Usage:
- lazy-load.js: 12 KB total, 8 KB used (33% unused)
- MathJax: 251 KB total, 180 KB used (28% unused)
- TOTAL: 280 KB total, 200 KB used (29% UNUSED)
```

### 2. Render-Blocking Resources
```
Blocking the critical rendering path:
1. custom.css: 850ms download + 120ms parse = 970ms BLOCKING
2. furo.css: 620ms download + 80ms parse = 700ms BLOCKING
3. _static/pygments.css: 180ms download + 30ms parse = 210ms BLOCKING
TOTAL BLOCKING TIME: 1,880ms (this is why LCP > 2s)
```

### 3. LCP Element Analysis
```
Largest Contentful Paint Element:
- Element: <div class="content-block"> with text "Double Inverted Pendulum Control"
- Rendered at: 5,500ms
- Blocked by:
  - CSS parsing: 1,880ms (38% of LCP time)
  - Font loading: 800ms (15% of LCP time)
  - JavaScript parsing: 1,200ms (22% of LCP time)
  - Other: 1,620ms (29% of LCP time)
```

### 4. Main Thread Activity Breakdown
```
Main Thread Busy Time: 3,200ms
- JavaScript execution: 1,400ms (44%)
- Style calculation: 850ms (27%)
- Layout: 520ms (16%)
- Paint: 280ms (9%)
- Other: 150ms (5%)
```

### 5. Actionable Recommendations (Priority Order)
```
1. CRITICAL: Remove unused CSS (62% of 225 KB = 140 KB savings)
   - Run PurgeCSS on custom.css
   - Expected LCP improvement: -1.2s

2. HIGH: Inline critical CSS (above-the-fold styles)
   - Inline ~15 KB of critical CSS in <head>
   - Defer non-critical CSS loading
   - Expected LCP improvement: -1.5s

3. MEDIUM: Defer non-critical JavaScript
   - Add defer attribute to utility scripts
   - Lazy load MathJax
   - Expected LCP improvement: -0.5s

4. LOW: Font optimization
   - Use font-display: swap
   - Preload critical fonts
   - Expected LCP improvement: -0.3s

TOTAL EXPECTED IMPROVEMENT: ~3.5s (5.5s → 2.0s)
```

## Execution Instructions

To run this analysis, use the mcp__puppeteer__ tools available:

1. mcp__puppeteer__puppeteer_navigate - Navigate to page
2. mcp__puppeteer__puppeteer_evaluate - Execute CDP/coverage scripts
3. mcp__puppeteer__puppeteer_screenshot - Capture visual progression

Combine these to build the complete analysis pipeline.
```

---

## Alternative: Use Existing CLI Tools

If puppeteer approach is too complex, you can use these standard CLI tools:

### Option 1: Chrome DevTools Performance Profiler
```bash
# Capture performance trace
google-chrome --headless --disable-gpu \
  --enable-logging --v=1 \
  --trace-startup-file=trace.json \
  --trace-startup-duration=10 \
  http://localhost:9000

# Analyze trace (requires trace analysis tool)
python analyze_trace.py trace.json
```

### Option 2: WebPageTest CLI
```bash
# Requires webpagetest CLI tool
webpagetest test http://localhost:9000 \
  --location Local \
  --connectivity 3G \
  --runs 3 \
  --output json
```

### Option 3: Chrome Coverage via Puppeteer Script
```bash
# Create standalone script: analyze_coverage.js
node analyze_coverage.js http://localhost:9000
```

### Option 4: Critical CSS Extraction
```bash
# Using critical package
npm install -g critical

critical http://localhost:9000 \
  --base=docs/_build/html \
  --inline \
  --minify \
  --width 1300 \
  --height 900
```

---

## Expected Outcome

This analysis should reveal:

1. **Exact unused CSS percentage** (currently suspected 62% = 140 KB)
2. **Exact CSS blocking time** (currently unknown, suspected ~2s)
3. **Exact JavaScript blocking time** (currently known: reduced from 18s to ~1.5s)
4. **LCP element and what's blocking it** (CSS? Fonts? JS?)
5. **Prioritized optimization roadmap** with expected LCP improvements

With this data, we can make informed decisions on next optimization steps to reach the <2.5s target.

---

**Next Steps After Analysis:**

1. If CSS blocking is >50% of LCP time → Proceed with CSS optimization
2. If fonts blocking is >30% of LCP time → Optimize font loading
3. If JavaScript still blocking → Further defer/async optimizations
4. If none of the above → Investigate server response time, document size, etc.

This systematic approach should identify the precise bottleneck preventing us from reaching <2.5s LCP.