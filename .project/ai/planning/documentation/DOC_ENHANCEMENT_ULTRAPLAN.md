# Documentation Enhancement Ultra-Plan
## Full-Text Search + Breadcrumbs + Interactive Notebooks

**Plan ID**: DOC-ENH-2025-001
**Created**: 2025-11-08
**Total Effort**: 16-21 hours
**Impact**: HIGH - Transforms already-excellent docs into world-class
**Status**: PLANNING

---

## Executive Summary

This plan implements 3 high-ROI enhancements to an already-mature documentation system (821 files, 11 navigation systems). The enhancements address the #1 missing capability (search), improve deep-navigation UX (breadcrumbs), and revolutionize interactive learning (Jupyter notebooks).

**Enhancement Stack:**
1. **Full-Text Search** (Priority 1) - 4-6 hours - Lunr.js client-side search
2. **Breadcrumbs** (Priority 2) - 2-3 hours - Context-aware navigation trail
3. **Interactive Notebooks** (Priority 3) - 10-12 hours - JupyterLite embedding

**Success Criteria:**
- Search: <200ms latency, 821 files indexed, keyboard shortcut (Ctrl+K)
- Breadcrumbs: Auto-generated from Sphinx toctree, visible on all pages
- Notebooks: 5 tutorials converted, execute Python in-browser, zero-install

---

## Phase 1: Full-Text Search Implementation (4-6 hours)

### 1.1 Technology Decision Matrix

**Candidates Evaluated:**

| Solution | Pros | Cons | Decision |
|----------|------|------|----------|
| **Lunr.js** | Client-side, zero backend, 200ms search | 2MB index for 821 files | **SELECTED** |
| Algolia | Fast, hosted, great UX | $1/mo after trial, vendor lock-in | Rejected |
| Sphinx Search | Built-in | Outdated, poor UX | Rejected |
| Meilisearch | Powerful, open-source | Requires server, overkill | Rejected |

**Selection Rationale:**
- Lunr.js is perfect for static sites (Sphinx generates static HTML)
- Client-side = zero server cost, zero maintenance
- 2MB index is acceptable (modern browsers handle this easily)
- Proven integration with Sphinx via `sphinx-lunr-search` extension

### 1.2 Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SPHINX BUILD PROCESS                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. Sphinx Reads RST/MD Files (821 files)                   │
│            │                                                  │
│            ▼                                                  │
│  2. sphinx-lunr-search Extension Hooks into Build           │
│            │                                                  │
│            ├──> Extracts: title, headings, body text        │
│            │                                                  │
│            ├──> Tokenizes: splits words, removes stopwords  │
│            │                                                  │
│            └──> Generates: searchindex.json (Lunr format)   │
│                       │                                       │
│                       ▼                                       │
│  3. Output: docs/_build/html/searchindex.json (2MB)         │
│                                                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   BROWSER RUNTIME (User)                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. Page Loads → Fetch searchindex.json (once, cached)     │
│            │                                                  │
│            ▼                                                  │
│  2. Lunr.js Initializes Index in Memory (~5MB RAM)          │
│            │                                                  │
│            ▼                                                  │
│  3. User Types "adaptive SMC" → Lunr.query()                │
│            │                                                  │
│            ├──> Tokenize query                               │
│            ├──> TF-IDF scoring                               │
│            ├──> Rank results by relevance                    │
│            └──> Return top 10 matches (<200ms)               │
│                       │                                       │
│                       ▼                                       │
│  4. Display Results in Modal Overlay (see UI mockup)        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Implementation Steps (Detailed)

#### Step 1.3.1: Install Dependencies (15 minutes)

```bash
# Add to requirements.txt (docs section)
echo "sphinx-lunr-search==0.6.2  # Full-text search via Lunr.js" >> requirements.txt

# Install
pip install sphinx-lunr-search
```

**Verification:**
```bash
python -c "import sphinx_lunr; print(f'sphinx-lunr {sphinx_lunr.__version__}')"
# Expected: sphinx-lunr 0.6.2
```

#### Step 1.3.2: Configure Sphinx Extension (30 minutes)

**File:** `docs/conf.py`

```python
# ============================================================================
# SEARCH CONFIGURATION (lunr.js)
# ============================================================================

extensions = [
    # ... existing extensions ...
    'sphinx_lunr',  # Add to extensions list
]

# Lunr.js search configuration
lunr_search = {
    # Index all text content
    'index_pages': True,

    # Include section headings in search
    'index_headings': True,

    # Boost title matches (appear higher in results)
    'boost_title': 2.0,

    # Include first 200 chars as preview snippet
    'snippet_length': 200,

    # Exclude these pages from indexing
    'exclude_pages': [
        'genindex',
        'search',
        'modindex',
    ],

    # Custom stopwords (words to ignore)
    'stopwords': [
        'a', 'an', 'the', 'is', 'are', 'was', 'were',
        'be', 'been', 'being', 'have', 'has', 'had',
    ],

    # Languages to support (English only for now)
    'languages': ['en'],
}

# Output search index to custom location (optional)
html_static_path = ['_static']
html_extra_path = []  # searchindex.json will auto-generate in _build/html/
```

**Testing:**
```bash
# Rebuild docs
sphinx-build -M html docs docs/_build -W --keep-going

# Verify searchindex.json exists
stat docs/_build/html/searchindex.json
# Expected: File exists, ~2MB size

# Verify index contains expected fields
python -c "
import json
with open('docs/_build/html/searchindex.json') as f:
    index = json.load(f)
    print(f'Documents indexed: {len(index.get(\"docs\", []))}')
    print(f'Index keys: {list(index.keys())}')
"
# Expected: Documents indexed: 821
#           Index keys: ['docs', 'index', 'pipeline']
```

#### Step 1.3.3: Create Search UI Component (2 hours)

**File:** `docs/_static/search.js` (NEW)

```javascript
// ============================================================================
// FULL-TEXT SEARCH UI (Lunr.js)
// ============================================================================
// Purpose: Client-side search over 821 documentation files
// Trigger: Ctrl+K or click search icon
// Performance: <200ms search latency
// ============================================================================

(function() {
  'use strict';

  // -------------------------------------------------------------------------
  // 1. STATE MANAGEMENT
  // -------------------------------------------------------------------------

  let searchIndex = null;          // Lunr.js index object
  let searchDocs = null;            // Document metadata (titles, URLs, snippets)
  let searchModal = null;           // Modal overlay DOM element
  let searchInput = null;           // Input field DOM element
  let searchResults = null;         // Results container DOM element
  let isIndexLoaded = false;        // Prevent double-loading

  // -------------------------------------------------------------------------
  // 2. INITIALIZATION (runs on page load)
  // -------------------------------------------------------------------------

  function init() {
    // Create modal HTML structure
    createSearchModal();

    // Bind keyboard shortcut (Ctrl+K)
    document.addEventListener('keydown', function(e) {
      if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        openSearchModal();
      }

      // ESC to close
      if (e.key === 'Escape' && searchModal.classList.contains('active')) {
        closeSearchModal();
      }
    });

    // Click outside modal to close
    searchModal.addEventListener('click', function(e) {
      if (e.target === searchModal) {
        closeSearchModal();
      }
    });

    // Load search index asynchronously (don't block page render)
    loadSearchIndex();
  }

  // -------------------------------------------------------------------------
  // 3. SEARCH INDEX LOADING
  // -------------------------------------------------------------------------

  function loadSearchIndex() {
    if (isIndexLoaded) return;

    // Show loading indicator
    console.log('[SEARCH] Loading search index...');

    fetch('/searchindex.json')
      .then(response => response.json())
      .then(data => {
        // Initialize Lunr.js with pre-built index
        searchIndex = lunr.Index.load(data.index);
        searchDocs = data.docs;
        isIndexLoaded = true;

        console.log(`[SEARCH] Index loaded: ${Object.keys(searchDocs).length} documents`);
      })
      .catch(error => {
        console.error('[SEARCH] Failed to load index:', error);
        showError('Search index failed to load. Please refresh the page.');
      });
  }

  // -------------------------------------------------------------------------
  // 4. MODAL UI CREATION
  // -------------------------------------------------------------------------

  function createSearchModal() {
    const modalHTML = `
      <div id="search-modal" class="search-modal">
        <div class="search-modal-content">
          <!-- Header -->
          <div class="search-header">
            <input
              type="text"
              id="search-input"
              class="search-input"
              placeholder="Search documentation... (Ctrl+K)"
              autocomplete="off"
            />
            <button class="search-close" onclick="closeSearchModal()">[X]</button>
          </div>

          <!-- Results -->
          <div id="search-results" class="search-results">
            <div class="search-hint">
              Type to search across 821 documentation files
            </div>
          </div>

          <!-- Footer -->
          <div class="search-footer">
            <kbd>ESC</kbd> to close
            <span class="search-stats" id="search-stats"></span>
          </div>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // Cache DOM references
    searchModal = document.getElementById('search-modal');
    searchInput = document.getElementById('search-input');
    searchResults = document.getElementById('search-results');

    // Bind search input event
    searchInput.addEventListener('input', debounce(handleSearch, 300));
  }

  // -------------------------------------------------------------------------
  // 5. SEARCH EXECUTION
  // -------------------------------------------------------------------------

  function handleSearch(e) {
    const query = e.target.value.trim();

    // Clear results if query is empty
    if (query.length === 0) {
      searchResults.innerHTML = '<div class="search-hint">Type to search...</div>';
      return;
    }

    // Require at least 2 characters
    if (query.length < 2) {
      searchResults.innerHTML = '<div class="search-hint">Type at least 2 characters...</div>';
      return;
    }

    // Check if index is loaded
    if (!isIndexLoaded) {
      searchResults.innerHTML = '<div class="search-loading">Loading search index...</div>';
      return;
    }

    // Execute search
    const startTime = performance.now();

    try {
      // Lunr.js query with wildcards for partial matching
      const results = searchIndex.search(`${query}* ${query}~1`);
      // Explanation:
      // - `query*` = prefix matching (e.g., "adapt" matches "adaptive")
      // - `query~1` = fuzzy matching with edit distance 1 (e.g., "adpative" matches "adaptive")

      const endTime = performance.now();
      const searchTime = (endTime - startTime).toFixed(0);

      // Display results
      displayResults(results, query, searchTime);

    } catch (error) {
      console.error('[SEARCH] Query error:', error);
      searchResults.innerHTML = '<div class="search-error">Invalid search query</div>';
    }
  }

  // -------------------------------------------------------------------------
  // 6. RESULTS DISPLAY
  // -------------------------------------------------------------------------

  function displayResults(results, query, searchTime) {
    // Update stats
    const statsEl = document.getElementById('search-stats');
    statsEl.textContent = `${results.length} results in ${searchTime}ms`;

    // No results
    if (results.length === 0) {
      searchResults.innerHTML = `
        <div class="search-no-results">
          No results found for "${escapeHTML(query)}"
        </div>
      `;
      return;
    }

    // Limit to top 50 results
    const topResults = results.slice(0, 50);

    // Render results
    const resultsHTML = topResults.map((result, index) => {
      const doc = searchDocs[result.ref];

      return `
        <a href="${doc.url}" class="search-result-item">
          <div class="search-result-title">
            ${highlightMatch(doc.title, query)}
          </div>
          <div class="search-result-snippet">
            ${highlightMatch(doc.snippet, query)}
          </div>
          <div class="search-result-meta">
            ${doc.breadcrumbs || doc.url}
          </div>
        </a>
      `;
    }).join('');

    searchResults.innerHTML = resultsHTML;
  }

  // -------------------------------------------------------------------------
  // 7. UTILITY FUNCTIONS
  // -------------------------------------------------------------------------

  function openSearchModal() {
    searchModal.classList.add('active');
    searchInput.focus();
  }

  function closeSearchModal() {
    searchModal.classList.remove('active');
    searchInput.value = '';
    searchResults.innerHTML = '<div class="search-hint">Type to search...</div>';
  }

  function escapeHTML(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  function highlightMatch(text, query) {
    if (!text) return '';

    const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
    return escapeHTML(text).replace(regex, '<mark>$1</mark>');
  }

  function escapeRegex(text) {
    return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function debounce(func, wait) {
    let timeout;
    return function(...args) {
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(this, args), wait);
    };
  }

  function showError(message) {
    searchResults.innerHTML = `<div class="search-error">${escapeHTML(message)}</div>`;
  }

  // -------------------------------------------------------------------------
  // 8. AUTO-INITIALIZE
  // -------------------------------------------------------------------------

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Expose closeSearchModal globally for button onclick
  window.closeSearchModal = closeSearchModal;

})();
```

**File:** `docs/_static/search.css` (NEW)

```css
/* ============================================================================
   FULL-TEXT SEARCH UI STYLES
   ============================================================================
   Purpose: Modal overlay for Lunr.js search
   Accessibility: WCAG 2.1 Level AA compliant
   ============================================================================ */

/* Modal Overlay */
.search-modal {
  display: none;
  position: fixed;
  z-index: 10000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
}

.search-modal.active {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 10vh;
}

/* Modal Content */
.search-modal-content {
  background-color: var(--color-background-primary);
  border: 1px solid var(--color-border-primary);
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 700px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Header */
.search-header {
  display: flex;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid var(--color-border-primary);
}

.search-input {
  flex: 1;
  font-size: 18px;
  padding: 12px;
  border: 1px solid var(--color-border-secondary);
  border-radius: 4px;
  background-color: var(--color-background-secondary);
  color: var(--color-text-primary);
}

.search-input:focus {
  outline: 2px solid var(--color-brand-primary);
  border-color: var(--color-brand-primary);
}

.search-close {
  margin-left: 12px;
  padding: 8px 12px;
  background: transparent;
  border: 1px solid var(--color-border-primary);
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  color: var(--color-text-secondary);
}

.search-close:hover {
  background-color: var(--color-background-hover);
}

/* Results Container */
.search-results {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  min-height: 200px;
  max-height: 500px;
}

/* Result Item */
.search-result-item {
  display: block;
  padding: 12px;
  margin-bottom: 8px;
  border: 1px solid var(--color-border-secondary);
  border-radius: 4px;
  text-decoration: none;
  color: inherit;
  transition: all 0.2s ease;
}

.search-result-item:hover {
  background-color: var(--color-background-hover);
  border-color: var(--color-brand-primary);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.search-result-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-brand-primary);
  margin-bottom: 4px;
}

.search-result-snippet {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-bottom: 4px;
  line-height: 1.4;
}

.search-result-meta {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

/* Highlight Matches */
.search-result-item mark {
  background-color: var(--color-warning-bg);
  color: var(--color-warning-text);
  padding: 2px 4px;
  border-radius: 2px;
  font-weight: 600;
}

/* Hints and States */
.search-hint,
.search-loading,
.search-no-results,
.search-error {
  text-align: center;
  padding: 40px 20px;
  color: var(--color-text-secondary);
  font-size: 14px;
}

.search-loading {
  color: var(--color-brand-primary);
}

.search-error {
  color: var(--color-danger-text);
  background-color: var(--color-danger-bg);
  border-radius: 4px;
}

/* Footer */
.search-footer {
  padding: 12px 16px;
  border-top: 1px solid var(--color-border-primary);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.search-footer kbd {
  padding: 2px 6px;
  border: 1px solid var(--color-border-primary);
  border-radius: 3px;
  background-color: var(--color-background-secondary);
  font-family: monospace;
}

.search-stats {
  color: var(--color-text-secondary);
}

/* Responsive Design */
@media (max-width: 768px) {
  .search-modal-content {
    width: 95%;
    max-height: 90vh;
  }

  .search-input {
    font-size: 16px;  /* Prevent zoom on iOS */
  }

  .search-results {
    max-height: 400px;
  }
}
```

#### Step 1.3.4: Add Search Button to Navbar (30 minutes)

**File:** `docs/_templates/layout.html` (may need to create)

```html
{% extends "!layout.html" %}

{% block header %}
  {{ super() }}

  <!-- Search Button in Navbar -->
  <div class="search-button-container">
    <button
      class="search-button"
      onclick="document.dispatchEvent(new KeyboardEvent('keydown', {key: 'k', ctrlKey: true}))"
      title="Search documentation (Ctrl+K)"
    >
      <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
        <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
      </svg>
      Search <kbd>Ctrl+K</kbd>
    </button>
  </div>
{% endblock %}

{% block scripts %}
  {{ super() }}

  <!-- Load Lunr.js -->
  <script src="https://cdn.jsdelivr.net/npm/lunr@2.3.9/lunr.min.js"></script>

  <!-- Load Search UI -->
  <script src="{{ pathto('_static/search.js', 1) }}"></script>
{% endblock %}

{% block css %}
  {{ super() }}
  <link rel="stylesheet" href="{{ pathto('_static/search.css', 1) }}" />
{% endblock %}
```

#### Step 1.3.5: Testing & Validation (1 hour)

**Test Plan:**

1. **Functional Tests**
```bash
# 1. Rebuild docs with search enabled
sphinx-build -M html docs docs/_build -W --keep-going

# 2. Start local server
python -m http.server 9000 --directory docs/_build/html

# 3. Open browser to http://localhost:9000

# 4. Test search functionality:
#    - Press Ctrl+K (modal should open)
#    - Type "adaptive SMC" (should show results in <200ms)
#    - Click result (should navigate to correct page)
#    - Press ESC (modal should close)
```

2. **Performance Tests**
```javascript
// Open browser console at http://localhost:9000
// Paste and run:

(async function testSearchPerformance() {
  const queries = [
    'adaptive SMC',
    'PSO optimization',
    'double inverted pendulum',
    'sliding mode control',
    'Lyapunov stability',
  ];

  for (const query of queries) {
    const start = performance.now();
    const results = searchIndex.search(`${query}* ${query}~1`);
    const end = performance.now();

    console.log(`Query: "${query}"`);
    console.log(`  Results: ${results.length}`);
    console.log(`  Time: ${(end - start).toFixed(2)}ms`);
    console.log('---');
  }
})();

// Expected output:
// Query: "adaptive SMC"
//   Results: 15
//   Time: 120ms
// ---
// Query: "PSO optimization"
//   Results: 23
//   Time: 150ms
// (etc.)
```

3. **Accessibility Tests**
```bash
# Install axe-core for accessibility testing
npm install -g @axe-core/cli

# Run accessibility audit on search modal
axe http://localhost:9000 --include "#search-modal"

# Expected: 0 violations, WCAG 2.1 Level AA compliant
```

4. **Cross-Browser Tests**
- [ ] Chromium (tested)
- [ ] Firefox (deferred per Phase 3 policy)
- [ ] Safari (deferred per Phase 3 policy)

**Success Criteria:**
- ✅ Search latency <200ms for all queries
- ✅ 821 files indexed
- ✅ Keyboard navigation works (Ctrl+K, ESC, Tab)
- ✅ WCAG 2.1 Level AA compliant
- ✅ Mobile responsive (tested on iPhone 12 simulator)

#### Step 1.3.6: Documentation & Handoff (30 minutes)

**Update Navigation Guide:**

```markdown
<!-- Add to docs/NAVIGATION.md -->

## How to Search Documentation

The documentation includes full-text search across all 821 files.

**Quick Access:**
- Press `Ctrl+K` anywhere to open search
- Click the search icon in the top navigation bar
- Type your query and press Enter

**Search Features:**
- Prefix matching: "adapt" matches "adaptive", "adaptation", etc.
- Fuzzy matching: "adpative" matches "adaptive" (1 typo tolerance)
- Context snippets: See matching text before clicking
- Fast results: <200ms search latency

**Tips:**
- Use specific terms: "Lyapunov stability" instead of "stability"
- Combine terms: "adaptive SMC PSO" finds pages with all 3 terms
- Check breadcrumbs: See file location before clicking
```

**Update CHANGELOG.md:**

```markdown
## [Unreleased]

### Added
- Full-text search across 821 documentation files
  - Lunr.js client-side search (<200ms latency)
  - Keyboard shortcut: Ctrl+K
  - Fuzzy matching with 1 typo tolerance
  - Context snippets in results
  - WCAG 2.1 Level AA compliant
```

---

## Phase 2: Breadcrumbs Implementation (2-3 hours)

### 2.1 Technology Decision

**Solution:** Auto-generate breadcrumbs from Sphinx toctree hierarchy

**Benefits:**
- Zero manual maintenance (toctree is already maintained)
- Consistent with Sphinx navigation model
- Leverages existing `sphinx.environment.toctree` API

### 2.2 Technical Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                  SPHINX BUILD PROCESS                         │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  1. Sphinx Parses Toctrees in index.rst                      │
│            │                                                   │
│            ├──> Home                                          │
│            │    └── Guides                                    │
│            │        └── Getting Started                       │
│            │            └── Tutorial 01                       │
│            │                                                   │
│            ▼                                                   │
│  2. For Each Page: Resolve Parent Chain                      │
│            │                                                   │
│            ├──> tutorial_01.md                                │
│            │    ├── parent: getting-started.md               │
│            │    ├── grandparent: guides/INDEX.md             │
│            │    └── root: index.rst                           │
│            │                                                   │
│            ▼                                                   │
│  3. Inject Breadcrumbs into Page Context                     │
│            │                                                   │
│            └──> page.breadcrumbs = [                          │
│                   {'title': 'Home', 'url': '/'},             │
│                   {'title': 'Guides', 'url': '/guides/'},    │
│                   {'title': 'Getting Started', 'url': '...'}, │
│                   {'title': 'Tutorial 01', 'url': None},     │
│                 ]                                              │
│                                                                │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                  HTML RENDERING (Jinja2)                      │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Template: docs/_templates/breadcrumbs.html                   │
│                                                                │
│  Output: Home > Guides > Getting Started > Tutorial 01       │
│          [link] [link]    [link]           [current page]    │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Steps

#### Step 2.3.1: Create Breadcrumb Extension (1 hour)

**File:** `docs/_ext/breadcrumbs.py` (NEW)

```python
"""
============================================================================
BREADCRUMB GENERATOR FOR SPHINX
============================================================================
Purpose: Auto-generate breadcrumbs from toctree hierarchy
Algorithm: Traverse toctree parents up to root
Fallback: Use file path if toctree not found
============================================================================
"""

from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from docutils import nodes

def get_breadcrumbs(app: Sphinx, pagename: str) -> list[dict[str, str]]:
    """
    Generate breadcrumb trail for a page by traversing toctree parents.

    Args:
        app: Sphinx application instance
        pagename: Current page name (e.g., 'guides/tutorial-01')

    Returns:
        List of breadcrumb items: [{'title': str, 'url': str | None}, ...]
        Last item (current page) has url=None

    Example:
        >>> get_breadcrumbs(app, 'guides/getting-started/tutorial-01')
        [
            {'title': 'Home', 'url': '/'},
            {'title': 'Guides', 'url': '/guides/INDEX.html'},
            {'title': 'Getting Started', 'url': '/guides/getting-started.html'},
            {'title': 'Tutorial 01', 'url': None},  # Current page
        ]
    """
    env: BuildEnvironment = app.env
    breadcrumbs = []

    # -------------------------------------------------------------------------
    # 1. Resolve toctree parents
    # -------------------------------------------------------------------------

    current = pagename
    visited = set()  # Prevent infinite loops

    while current:
        # Prevent infinite loops (shouldn't happen, but be defensive)
        if current in visited:
            app.warn(f"Circular toctree reference detected for {current}")
            break
        visited.add(current)

        # Get page title
        try:
            title = env.titles[current].astext()
        except KeyError:
            # Fallback: use filename
            title = current.split('/')[-1].replace('-', ' ').title()

        # Get page URL (None for current page)
        url = None if current == pagename else app.builder.get_relative_uri(pagename, current)

        # Prepend to breadcrumbs (we're traversing bottom-up)
        breadcrumbs.insert(0, {'title': title, 'url': url})

        # Get parent from toctree
        parent = env.toctree_includes.get(current)
        if parent:
            current = parent[0] if isinstance(parent, list) else parent
        else:
            # Reached root or orphan page
            break

    # -------------------------------------------------------------------------
    # 2. Ensure "Home" is always first
    # -------------------------------------------------------------------------

    if not breadcrumbs or breadcrumbs[0]['title'] != 'Home':
        breadcrumbs.insert(0, {
            'title': 'Home',
            'url': app.builder.get_relative_uri(pagename, 'index')
        })

    # -------------------------------------------------------------------------
    # 3. Limit breadcrumb length (prevent UI overflow)
    # -------------------------------------------------------------------------

    MAX_BREADCRUMBS = 5
    if len(breadcrumbs) > MAX_BREADCRUMBS:
        # Keep first 2 (Home, Section) + last 2 (Parent, Current)
        breadcrumbs = [
            breadcrumbs[0],
            breadcrumbs[1],
            {'title': '...', 'url': None},  # Ellipsis
            breadcrumbs[-2],
            breadcrumbs[-1],
        ]

    return breadcrumbs


def html_page_context(app: Sphinx, pagename: str, templatename: str,
                       context: dict, doctree) -> None:
    """
    Inject breadcrumbs into page context (called for every HTML page).

    This hook is called by Sphinx before rendering each page.
    We add `breadcrumbs` to the context so templates can access it.
    """
    context['breadcrumbs'] = get_breadcrumbs(app, pagename)


def setup(app: Sphinx) -> dict:
    """
    Register extension with Sphinx.
    """
    app.connect('html-page-context', html_page_context)

    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
```

#### Step 2.3.2: Enable Extension in Sphinx Config (5 minutes)

**File:** `docs/conf.py`

```python
# ============================================================================
# EXTENSIONS
# ============================================================================

import sys
import os

# Add custom extensions directory to path
sys.path.insert(0, os.path.abspath('_ext'))

extensions = [
    # ... existing extensions ...
    'breadcrumbs',  # Add custom breadcrumb generator
]
```

#### Step 2.3.3: Create Breadcrumb Template (30 minutes)

**File:** `docs/_templates/breadcrumbs.html` (NEW)

```html
{#
============================================================================
BREADCRUMB NAVIGATION TEMPLATE
============================================================================
Purpose: Render breadcrumb trail at top of each page
Accessibility: ARIA landmarks, semantic markup
Responsive: Collapses to dropdown on mobile
============================================================================
#}

{% if breadcrumbs and breadcrumbs|length > 1 %}
<nav class="breadcrumbs" aria-label="Breadcrumb navigation">
  <ol class="breadcrumbs-list">
    {% for crumb in breadcrumbs %}
      <li class="breadcrumbs-item {% if loop.last %}current{% endif %}">
        {% if crumb.url %}
          <a href="{{ crumb.url }}" class="breadcrumbs-link">
            {{ crumb.title }}
          </a>
        {% else %}
          <span class="breadcrumbs-current" aria-current="page">
            {{ crumb.title }}
          </span>
        {% endif %}

        {% if not loop.last %}
          <span class="breadcrumbs-separator" aria-hidden="true">&gt;</span>
        {% endif %}
      </li>
    {% endfor %}
  </ol>
</nav>
{% endif %}
```

#### Step 2.3.4: Style Breadcrumbs (30 minutes)

**File:** `docs/_static/breadcrumbs.css` (NEW)

```css
/* ============================================================================
   BREADCRUMB NAVIGATION STYLES
   ============================================================================
   Purpose: Visual styling for breadcrumb trail
   Accessibility: WCAG 2.1 Level AA contrast ratios
   Responsive: Horizontal scroll on narrow screens
   ============================================================================ */

.breadcrumbs {
  padding: 12px 0;
  margin-bottom: 24px;
  border-bottom: 1px solid var(--color-border-secondary);
}

.breadcrumbs-list {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 8px;
}

.breadcrumbs-item {
  display: inline-flex;
  align-items: center;
  font-size: 14px;
}

.breadcrumbs-link {
  color: var(--color-brand-primary);
  text-decoration: none;
  transition: color 0.2s ease;
}

.breadcrumbs-link:hover {
  color: var(--color-brand-secondary);
  text-decoration: underline;
}

.breadcrumbs-link:focus {
  outline: 2px solid var(--color-brand-primary);
  outline-offset: 2px;
  border-radius: 2px;
}

.breadcrumbs-current {
  color: var(--color-text-primary);
  font-weight: 500;
}

.breadcrumbs-separator {
  margin: 0 4px;
  color: var(--color-text-tertiary);
  user-select: none;
}

/* Truncate long breadcrumb text */
.breadcrumbs-item {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.breadcrumbs-item:hover {
  max-width: none;  /* Expand on hover */
  white-space: normal;
}

/* Responsive: Horizontal scroll on mobile */
@media (max-width: 768px) {
  .breadcrumbs-list {
    flex-wrap: nowrap;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;  /* Smooth scroll on iOS */
  }

  .breadcrumbs-item {
    flex-shrink: 0;
  }
}

/* Dark mode support (if theme uses data-theme attribute) */
[data-theme="dark"] .breadcrumbs {
  border-bottom-color: var(--color-border-dark);
}

[data-theme="dark"] .breadcrumbs-link {
  color: var(--color-brand-light);
}

[data-theme="dark"] .breadcrumbs-current {
  color: var(--color-text-light);
}
```

#### Step 2.3.5: Integrate into Layout (15 minutes)

**File:** `docs/_templates/layout.html` (modify existing or create)

```html
{% extends "!layout.html" %}

{% block content %}
  <!-- Inject breadcrumbs before main content -->
  {% include "breadcrumbs.html" %}

  <!-- Original content -->
  {{ super() }}
{% endblock %}

{% block css %}
  {{ super() }}
  <link rel="stylesheet" href="{{ pathto('_static/breadcrumbs.css', 1) }}" />
{% endblock %}
```

#### Step 2.3.6: Testing & Validation (30 minutes)

**Test Plan:**

1. **Functional Tests**
```bash
# 1. Rebuild docs
sphinx-build -M html docs docs/_build -W --keep-going

# 2. Verify breadcrumbs appear on pages
curl -s http://localhost:9000/guides/getting-started/tutorial-01.html | grep "breadcrumbs"
# Expected: <nav class="breadcrumbs" ...> found

# 3. Check breadcrumb structure
# Open browser, inspect breadcrumbs on tutorial-01.html
# Expected structure: Home > Guides > Getting Started > Tutorial 01
```

2. **Accessibility Tests**
```bash
# Run accessibility audit on breadcrumbs
axe http://localhost:9000/guides/getting-started/tutorial-01.html --include ".breadcrumbs"

# Expected: 0 violations
# - ARIA labels present (aria-label, aria-current)
# - Semantic HTML (<nav>, <ol>, <li>)
# - Keyboard navigable (Tab, Enter)
```

3. **Visual Regression Tests**
```bash
# Take screenshots before/after
# (Manual comparison for now, automated tests in future)
```

**Success Criteria:**
- ✅ Breadcrumbs appear on all pages (except index.rst)
- ✅ Correct hierarchy (matches toctree)
- ✅ Last item is current page (not clickable)
- ✅ WCAG 2.1 Level AA compliant
- ✅ Responsive (tested on mobile)

---

## Phase 3: Interactive Jupyter Notebooks (10-12 hours)

### 3.1 Technology Decision Matrix

**Candidates Evaluated:**

| Solution | Pros | Cons | Decision |
|----------|------|------|----------|
| **JupyterLite** | Zero server, runs in browser, full Jupyter UX | 50MB WASM, complex setup | **SELECTED** |
| Binder | Full Jupyter, GitHub integration | Requires server, slow startup | Rejected |
| Google Colab | Familiar, free hosting | Requires Google account | Rejected |
| Thebe | Lightweight, Sphinx integration | Limited features | Rejected |

**Selection Rationale:**
- JupyterLite is revolutionary: full Jupyter in-browser, zero install
- Perfect for documentation: users can run code WITHOUT server/install
- Trade-off: 50MB WASM payload (acceptable, loads once)
- Active development, official Jupyter project

### 3.2 Technical Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                  JUPYTERLITE ARCHITECTURE                     │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  1. Build Time (Sphinx + JupyterLite)                        │
│            │                                                   │
│            ├──> Convert tutorials/*.md to *.ipynb            │
│            │    (pandoc or myst-nb)                           │
│            │                                                   │
│            ├──> JupyterLite builds WASM kernel                │
│            │    - Python 3.11 WASM (pyodide)                  │
│            │    - NumPy, SciPy, Matplotlib (preinstalled)    │
│            │    - Custom package: dip-smc-pso wheel           │
│            │                                                   │
│            └──> Output: docs/_build/html/jupyter/             │
│                       ├── lab/index.html (full JupyterLab)   │
│                       ├── repl/index.html (minimal REPL)     │
│                       └── files/*.ipynb (tutorial notebooks) │
│                                                                │
│  2. Runtime (Browser)                                         │
│            │                                                   │
│            ├──> User clicks "Run in Browser" button          │
│            │                                                   │
│            ├──> Load JupyterLite (~50MB WASM, once)          │
│            │                                                   │
│            ├──> User edits code in notebook cell             │
│            │                                                   │
│            ├──> Execute cell (Python runs in WASM)           │
│            │    ├── Import numpy, scipy, matplotlib          │
│            │    ├── Import dip_smc_pso                        │
│            │    └── Run simulation                            │
│            │                                                   │
│            └──> Display output (text, plots, animations)     │
│                 ├── Matplotlib plots render to canvas        │
│                 ├── Print statements to stdout               │
│                 └── Errors to stderr                          │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

### 3.3 Implementation Steps

#### Step 3.3.1: Install JupyterLite (30 minutes)

```bash
# Install JupyterLite build tools
pip install jupyterlite-core jupyterlite-pyodide-kernel
pip install jupyterlab>=4.0.0  # Required for building

# Add to requirements.txt (docs section)
cat >> requirements.txt << 'EOF'

# JupyterLite (interactive notebooks in docs)
jupyterlite-core==0.3.0      # Core JupyterLite builder
jupyterlite-pyodide-kernel==0.3.1  # Python WASM kernel
jupyterlab>=4.0.0             # Required for JupyterLite build
EOF

# Verify installation
jupyter lite --version
# Expected: jupyterlite-core 0.3.0
```

#### Step 3.3.2: Create JupyterLite Config (1 hour)

**File:** `docs/jupyter_lite_config.json` (NEW)

```json
{
  "LiteBuildConfig": {
    "output_dir": "_build/html/jupyter",
    "contents": [
      "tutorials/*.ipynb",
      "examples/*.ipynb"
    ],
    "apps": [
      "lab",
      "repl"
    ]
  },

  "PipliteAddon": {
    "piplite_urls": [
      "../_static/wheels/dip_smc_pso-2.1.0-py3-none-any.whl"
    ]
  },

  "LiteStatusApp": {
    "federated_extensions": []
  }
}
```

**Explanation:**
- `output_dir`: Where JupyterLite builds (inside Sphinx output)
- `contents`: Notebooks to include (tutorials + examples)
- `apps`: Which JupyterLite interfaces to build (Lab + REPL)
- `piplite_urls`: Custom packages to preinstall (our package!)

#### Step 3.3.3: Build Package Wheel (1 hour)

**File:** `pyproject.toml` (may need to add build config)

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "dip-smc-pso"
version = "2.1.0"
description = "Double Inverted Pendulum Sliding Mode Control with PSO"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "numpy>=1.21.0",
    "scipy>=1.7.0",
    "matplotlib>=3.4.0",
    # ... other deps from requirements.txt ...
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=3.0.0",
]
```

**Build Script:** `scripts/build_wheel.sh` (NEW)

```bash
#!/bin/bash
# ============================================================================
# BUILD WHEEL FOR JUPYTERLITE
# ============================================================================
# Purpose: Create .whl file for in-browser installation
# Output: dist/dip_smc_pso-2.1.0-py3-none-any.whl
# ============================================================================

set -euo pipefail

echo "[INFO] Building wheel for JupyterLite..."

# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build wheel
python -m build --wheel

# Copy to docs static directory
mkdir -p docs/_static/wheels/
cp dist/*.whl docs/_static/wheels/

# Verify wheel
python -m zipfile -l "docs/_static/wheels/$(ls docs/_static/wheels/)"

echo "[OK] Wheel built and copied to docs/_static/wheels/"
```

**Run:**
```bash
chmod +x scripts/build_wheel.sh
./scripts/build_wheel.sh

# Expected output:
# [INFO] Building wheel for JupyterLite...
# [OK] Wheel built and copied to docs/_static/wheels/
```

#### Step 3.3.4: Convert Tutorials to Notebooks (2 hours)

**Option 1: Manual Conversion (recommended for control)**

**Example:** `docs/tutorials/tutorial-01.ipynb` (NEW)

```json
{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "# Tutorial 01: Your First Simulation\n",
        "\n",
        "In this tutorial, you'll run your first double inverted pendulum simulation.\n",
        "\n",
        "**Learning Objectives:**\n",
        "- Understand the basic simulation workflow\n",
        "- Run a classical SMC controller\n",
        "- Visualize system response\n",
        "\n",
        "**Prerequisites:** None (complete beginner friendly)\n",
        "\n",
        "**Duration:** 10-15 minutes"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## Step 1: Import Required Modules\n",
        "\n",
        "First, let's import the necessary components from the `dip-smc-pso` package."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "\n",
        "# Import DIP simulation components\n",
        "from dip_smc_pso.controllers import ClassicalSMC\n",
        "from dip_smc_pso.dynamics import SimplifiedDynamics\n",
        "from dip_smc_pso.simulation import run_simulation\n",
        "\n",
        "print(\"[OK] Imports successful!\")"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## Step 2: Configure Simulation Parameters\n",
        "\n",
        "Let's set up the basic parameters for our simulation."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Time parameters\n",
        "dt = 0.01  # Time step (10ms)\n",
        "t_final = 5.0  # Simulation duration (5 seconds)\n",
        "\n",
        "# Initial conditions [x, x_dot, theta1, theta1_dot, theta2, theta2_dot]\n",
        "x0 = np.array([0.0, 0.0, 0.1, 0.0, -0.1, 0.0])\n",
        "#                ^    ^     ^     ^      ^     ^\n",
        "#                |    |     |     |      |     +--- Angular velocity of upper pendulum\n",
        "#                |    |     |     |      +--------- Angle of upper pendulum (rad)\n",
        "#                |    |     |     +---------------- Angular velocity of lower pendulum\n",
        "#                |    |     +---------------------- Angle of lower pendulum (rad)\n",
        "#                |    +---------------------------- Cart velocity\n",
        "#                +--------------------------------- Cart position\n",
        "\n",
        "print(f\"Simulation: {t_final}s at {dt}s timestep ({int(t_final/dt)} steps)\")\n",
        "print(f\"Initial state: {x0}\")"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## Step 3: Initialize Controller and Dynamics\n",
        "\n",
        "Now let's create our controller (Classical SMC) and dynamics model."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Create Classical SMC controller with default gains\n",
        "controller = ClassicalSMC(\n",
        "    gains=[10.0, 5.0, 8.0, 3.0, 15.0, 2.0],\n",
        "    boundary_layer=0.1,\n",
        ")\n",
        "\n",
        "# Create simplified dynamics model\n",
        "dynamics = SimplifiedDynamics()\n",
        "\n",
        "print(\"[OK] Controller and dynamics initialized\")"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## Step 4: Run Simulation\n",
        "\n",
        "Execute the simulation and collect results."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Run simulation\n",
        "results = run_simulation(\n",
        "    controller=controller,\n",
        "    dynamics=dynamics,\n",
        "    x0=x0,\n",
        "    dt=dt,\n",
        "    t_final=t_final,\n",
        ")\n",
        "\n",
        "print(f\"[OK] Simulation complete: {len(results['t'])} timesteps\")\n",
        "print(f\"Final state: {results['x'][-1]}\")"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## Step 5: Visualize Results\n",
        "\n",
        "Plot the cart position and pendulum angles over time."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "fig, axes = plt.subplots(3, 1, figsize=(10, 8))\n",
        "\n",
        "# Cart position\n",
        "axes[0].plot(results['t'], results['x'][:, 0], 'b-', linewidth=2)\n",
        "axes[0].set_ylabel('Cart Position (m)')\n",
        "axes[0].grid(True, alpha=0.3)\n",
        "axes[0].set_title('System Response - Classical SMC')\n",
        "\n",
        "# Lower pendulum angle\n",
        "axes[1].plot(results['t'], np.rad2deg(results['x'][:, 2]), 'r-', linewidth=2)\n",
        "axes[1].set_ylabel('Angle 1 (deg)')\n",
        "axes[1].grid(True, alpha=0.3)\n",
        "\n",
        "# Upper pendulum angle\n",
        "axes[2].plot(results['t'], np.rad2deg(results['x'][:, 4]), 'g-', linewidth=2)\n",
        "axes[2].set_ylabel('Angle 2 (deg)')\n",
        "axes[2].set_xlabel('Time (s)')\n",
        "axes[2].grid(True, alpha=0.3)\n",
        "\n",
        "plt.tight_layout()\n",
        "plt.show()\n",
        "\n",
        "print(\"[OK] Plots generated successfully!\")"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## Congratulations!\n",
        "\n",
        "You've successfully run your first double inverted pendulum simulation!\n",
        "\n",
        "**What You Learned:**\n",
        "- How to import and use the DIP simulation framework\n",
        "- How to configure simulation parameters\n",
        "- How to run a simulation with Classical SMC\n",
        "- How to visualize results\n",
        "\n",
        "**Next Steps:**\n",
        "- Try modifying the initial conditions (e.g., larger angles)\n",
        "- Experiment with different controller gains\n",
        "- Move on to Tutorial 02: Controller Comparison\n",
        "\n",
        "**Exercises:**\n",
        "1. Change the initial angle of the lower pendulum to 0.2 rad and re-run\n",
        "2. Increase the simulation duration to 10 seconds\n",
        "3. Plot the control input (force) over time (hint: `results['u']`)"
      ]
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3 (ipykernel)",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "name": "python",
      "version": "3.11.0"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 5
}
```

**Conversion Script:** `scripts/convert_tutorials.py` (NEW)

```python
"""
============================================================================
TUTORIAL TO NOTEBOOK CONVERTER
============================================================================
Purpose: Convert existing markdown tutorials to Jupyter notebooks
Strategy: Parse markdown, split into code/text cells
Output: docs/tutorials/*.ipynb
============================================================================
"""

import re
from pathlib import Path
import nbformat as nbf

def convert_markdown_to_notebook(md_path: Path) -> nbf.NotebookNode:
    """
    Convert a markdown tutorial to a Jupyter notebook.

    Algorithm:
    1. Parse markdown sections (split on ## headings)
    2. Identify code blocks (```python ... ```)
    3. Create notebook cells:
       - Markdown → markdown cell
       - Code block → code cell
    4. Return notebook object
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Create new notebook
    nb = nbf.v4.new_notebook()

    # Split content into sections (by ## headings)
    sections = re.split(r'(^##[^\n]+)', content, flags=re.MULTILINE)

    # First section (before first ##) is intro
    if sections[0].strip():
        nb.cells.append(nbf.v4.new_markdown_cell(sections[0].strip()))

    # Process remaining sections
    for i in range(1, len(sections), 2):
        if i + 1 >= len(sections):
            break

        heading = sections[i]
        body = sections[i + 1]

        # Split body into text and code blocks
        parts = re.split(r'(```python.*?```)', body, flags=re.DOTALL)

        for part in parts:
            part = part.strip()
            if not part:
                continue

            # Code block
            if part.startswith('```python'):
                code = part.replace('```python', '').replace('```', '').strip()
                nb.cells.append(nbf.v4.new_code_cell(code))

            # Text
            else:
                text = heading + '\n\n' + part if part == parts[1] else part
                nb.cells.append(nbf.v4.new_markdown_cell(text.strip()))
                heading = ''  # Only include heading once

    return nb


def main():
    """Convert all tutorials in docs/guides/tutorials/*.md"""
    tutorials_dir = Path('docs/guides/tutorials')
    output_dir = Path('docs/tutorials')  # New directory for notebooks
    output_dir.mkdir(exist_ok=True)

    md_files = list(tutorials_dir.glob('*.md'))
    print(f"[INFO] Found {len(md_files)} tutorial files")

    for md_path in md_files:
        print(f"[INFO] Converting {md_path.name}...")

        nb = convert_markdown_to_notebook(md_path)

        # Save notebook
        output_path = output_dir / md_path.name.replace('.md', '.ipynb')
        with open(output_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)

        print(f"[OK] Saved to {output_path}")

    print(f"\n[OK] Converted {len(md_files)} tutorials to notebooks")


if __name__ == '__main__':
    main()
```

**Run:**
```bash
python scripts/convert_tutorials.py

# Expected output:
# [INFO] Found 5 tutorial files
# [INFO] Converting tutorial-01-basics.md...
# [OK] Saved to docs/tutorials/tutorial-01-basics.ipynb
# (etc.)
```

#### Step 3.3.5: Build JupyterLite Site (2 hours)

**Build Script:** `scripts/build_jupyterlite.sh` (NEW)

```bash
#!/bin/bash
# ============================================================================
# BUILD JUPYTERLITE SITE
# ============================================================================
# Purpose: Generate JupyterLite WASM environment for documentation
# Output: docs/_build/html/jupyter/ (50MB)
# ============================================================================

set -euo pipefail

echo "[INFO] Building JupyterLite site..."

# Step 1: Ensure wheel is built
if [ ! -f "docs/_static/wheels/dip_smc_pso-2.1.0-py3-none-any.whl" ]; then
    echo "[INFO] Wheel not found, building..."
    ./scripts/build_wheel.sh
fi

# Step 2: Build JupyterLite
cd docs
jupyter lite build \
    --config jupyter_lite_config.json \
    --debug

# Step 3: Verify output
if [ -d "_build/html/jupyter/lab" ]; then
    echo "[OK] JupyterLite built successfully"
    echo "[INFO] Lab interface: _build/html/jupyter/lab/index.html"
    echo "[INFO] REPL interface: _build/html/jupyter/repl/index.html"
else
    echo "[ERROR] JupyterLite build failed"
    exit 1
fi

# Step 4: Test that package wheel is accessible
if [ -f "_build/html/jupyter/files/packages/dip_smc_pso-2.1.0-py3-none-any.whl" ]; then
    echo "[OK] Package wheel copied to JupyterLite"
else
    echo "[WARNING] Package wheel not found in JupyterLite output"
fi

cd ..
echo "[OK] JupyterLite build complete"
```

**Run:**
```bash
chmod +x scripts/build_jupyterlite.sh
./scripts/build_jupyterlite.sh

# Expected output (takes 5-10 minutes):
# [INFO] Building JupyterLite site...
# [INFO] Wheel not found, building...
# [OK] Wheel built and copied to docs/_static/wheels/
# [jupyterlite] Building JupyterLite...
# [jupyterlite] Downloading pyodide...
# [jupyterlite] Extracting pyodide...
# [jupyterlite] Copying files...
# [OK] JupyterLite built successfully
```

#### Step 3.3.6: Integrate into Sphinx Build (1 hour)

**File:** `docs/conf.py` (add custom build step)

```python
# ============================================================================
# CUSTOM BUILD STEPS
# ============================================================================

import subprocess
from pathlib import Path

def build_jupyterlite(app, exception):
    """
    Build JupyterLite after Sphinx build completes.

    This ensures JupyterLite is always up-to-date with docs.
    """
    if exception:
        return  # Don't build if Sphinx failed

    if app.builder.name != 'html':
        return  # Only build for HTML output

    print("[INFO] Building JupyterLite...")

    # Run build script
    script_path = Path(__file__).parent.parent / 'scripts' / 'build_jupyterlite.sh'
    result = subprocess.run([str(script_path)], capture_output=True, text=True)

    if result.returncode == 0:
        print("[OK] JupyterLite build complete")
    else:
        print(f"[ERROR] JupyterLite build failed:\n{result.stderr}")


def setup(app):
    """Register custom build hooks."""
    app.connect('build-finished', build_jupyterlite)
```

**Testing:**
```bash
# Rebuild docs (should trigger JupyterLite build)
sphinx-build -M html docs docs/_build -W --keep-going

# Verify JupyterLite exists
ls -lh docs/_build/html/jupyter/lab/index.html
# Expected: File exists, ~1MB

# Test in browser
python -m http.server 9000 --directory docs/_build/html
# Open http://localhost:9000/jupyter/lab/index.html
# Expected: JupyterLab interface loads, notebooks visible
```

#### Step 3.3.7: Add "Run in Browser" Buttons (2 hours)

**File:** `docs/_static/jupyterlite_button.js` (NEW)

```javascript
// ============================================================================
// JUPYTERLITE LAUNCH BUTTONS
// ============================================================================
// Purpose: Add "Run in Browser" buttons to tutorial pages
// Trigger: Auto-detect tutorial pages, inject button
// Target: JupyterLite Lab with pre-loaded notebook
// ============================================================================

(function() {
  'use strict';

  // -------------------------------------------------------------------------
  // 1. DETECT TUTORIAL PAGES
  // -------------------------------------------------------------------------

  // Only run on tutorial pages
  const currentPath = window.location.pathname;
  if (!currentPath.includes('/tutorials/')) {
    return;  // Not a tutorial page
  }

  // Extract notebook name from URL
  // Example: /tutorials/tutorial-01.html → tutorial-01.ipynb
  const pageName = currentPath.split('/').pop().replace('.html', '');
  const notebookPath = `tutorial/${pageName}.ipynb`;

  // -------------------------------------------------------------------------
  // 2. CREATE LAUNCH BUTTON
  // -------------------------------------------------------------------------

  function createLaunchButton() {
    const button = document.createElement('a');
    button.className = 'jupyterlite-button';
    button.textContent = '[▶] Run in Browser';
    button.title = 'Open this tutorial in JupyterLab (runs in browser, no install required)';

    // JupyterLite URL with pre-loaded notebook
    const jupyterliteURL = `/jupyter/lab/index.html?path=${notebookPath}`;
    button.href = jupyterliteURL;
    button.target = '_blank';  // Open in new tab

    return button;
  }

  // -------------------------------------------------------------------------
  // 3. INJECT BUTTON INTO PAGE
  // -------------------------------------------------------------------------

  function injectButton() {
    // Find the first h1 (page title)
    const pageTitle = document.querySelector('article h1');
    if (!pageTitle) {
      console.warn('[JUPYTERLITE] Could not find page title');
      return;
    }

    // Create button
    const button = createLaunchButton();

    // Insert after title
    pageTitle.insertAdjacentElement('afterend', button);

    console.log(`[JUPYTERLITE] Button added for ${notebookPath}`);
  }

  // -------------------------------------------------------------------------
  // 4. INITIALIZE
  // -------------------------------------------------------------------------

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectButton);
  } else {
    injectButton();
  }

})();
```

**File:** `docs/_static/jupyterlite_button.css` (NEW)

```css
/* ============================================================================
   JUPYTERLITE LAUNCH BUTTON STYLES
   ============================================================================ */

.jupyterlite-button {
  display: inline-block;
  margin: 16px 0;
  padding: 12px 24px;
  background: linear-gradient(135deg, var(--color-brand-primary) 0%, var(--color-brand-secondary) 100%);
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 600;
  font-size: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  cursor: pointer;
}

.jupyterlite-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.jupyterlite-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* Play icon (▶) styling */
.jupyterlite-button::before {
  content: '';
  display: inline-block;
  width: 0;
  height: 0;
  border-left: 8px solid white;
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  margin-right: 8px;
  vertical-align: middle;
}
```

**File:** `docs/_templates/layout.html` (add scripts)

```html
{% extends "!layout.html" %}

{% block scripts %}
  {{ super() }}

  <!-- JupyterLite launch button (only on tutorial pages) -->
  <script src="{{ pathto('_static/jupyterlite_button.js', 1) }}"></script>
{% endblock %}

{% block css %}
  {{ super() }}
  <link rel="stylesheet" href="{{ pathto('_static/jupyterlite_button.css', 1) }}" />
{% endblock %}
```

#### Step 3.3.8: Testing & Validation (2 hours)

**Test Plan:**

1. **Functional Tests**
```bash
# 1. Rebuild docs
sphinx-build -M html docs docs/_build -W --keep-going

# 2. Verify button appears on tutorial pages
curl -s http://localhost:9000/tutorials/tutorial-01.html | grep "jupyterlite-button"
# Expected: <a class="jupyterlite-button" ...> found

# 3. Test JupyterLite loading
# Open http://localhost:9000/jupyter/lab/index.html?path=tutorials/tutorial-01.ipynb
# Expected:
#  - JupyterLab interface loads (~10s)
#  - tutorial-01.ipynb opens automatically
#  - Toolbar shows "Run" button
```

2. **Execution Tests**
```python
# In JupyterLab browser interface:

# Test 1: Import package
import dip_smc_pso
print(dip_smc_pso.__version__)
# Expected: 2.1.0

# Test 2: Run cell from tutorial
from dip_smc_pso.controllers import ClassicalSMC
controller = ClassicalSMC(gains=[10.0, 5.0, 8.0, 3.0, 15.0, 2.0])
print(controller)
# Expected: <ClassicalSMC object at 0x...>

# Test 3: Run full simulation (from tutorial-01.ipynb)
# Click "Run All Cells" in JupyterLab
# Expected:
#  - All cells execute without errors
#  - Plots display inline
#  - Total execution time <10s
```

3. **Performance Tests**
```bash
# Measure JupyterLite load time
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:9000/jupyter/lab/index.html

# Expected:
#  - time_total: <5s (first load)
#  - time_total: <1s (cached)
```

4. **Cross-Browser Tests**
- [ ] Chromium (tested)
- [ ] Firefox (deferred per Phase 3 policy)
- [ ] Safari (deferred per Phase 3 policy)

**Success Criteria:**
- ✅ JupyterLite loads in <10s (first visit)
- ✅ Notebooks execute without errors
- ✅ Plots render correctly (matplotlib)
- ✅ Package imports work (`import dip_smc_pso`)
- ✅ "Run in Browser" buttons appear on all tutorial pages
- ✅ Mobile responsive (JupyterLite has responsive UI)

---

## Phase 4: Documentation & Deployment (1-2 hours)

### 4.1 Update Documentation

**File:** `docs/guides/INDEX.md` (update)

```markdown
## New Interactive Features

### Full-Text Search
Search across all 821 documentation files instantly.

- **Keyboard Shortcut**: `Ctrl+K` anywhere
- **Features**: Prefix matching, fuzzy matching, context snippets
- **Performance**: <200ms search latency

### Breadcrumbs
Navigate deep hierarchies easily with breadcrumb trails.

- **Auto-Generated**: From Sphinx toctree structure
- **Always Visible**: Top of every page
- **Click to Navigate**: Jump to parent sections

### Interactive Notebooks
Run Python code directly in your browser, no installation required!

- **Technology**: JupyterLite (WASM-based Jupyter)
- **Launch**: Click "▶ Run in Browser" on any tutorial
- **Features**: Full Jupyter environment, matplotlib plots, zero setup
```

**File:** `docs/NAVIGATION.md` (update)

```markdown
## Interactive Features

The documentation now includes 3 powerful interactive features:

### 1. Full-Text Search
- **Trigger**: Press `Ctrl+K` or click search icon
- **Coverage**: All 821 documentation files
- **Speed**: <200ms search latency
- **Features**: Fuzzy matching, prefix matching, context snippets

### 2. Breadcrumbs
- **Location**: Top of every page
- **Purpose**: Show current location in hierarchy
- **Example**: Home > Guides > Tutorials > Tutorial 01
- **Action**: Click any breadcrumb to navigate up

### 3. Interactive Notebooks (NEW!)
- **What**: Run Python code in-browser (zero install)
- **How**: Click "▶ Run in Browser" on tutorial pages
- **Environment**: Full Jupyter with NumPy, SciPy, Matplotlib
- **Package**: `dip-smc-pso` pre-installed
```

### 4.2 Update CHANGELOG

```markdown
## [2.2.0] - 2025-11-09

### Added - Documentation Enhancements
- **Full-text search** across 821 documentation files
  - Lunr.js client-side search (<200ms latency)
  - Keyboard shortcut: Ctrl+K
  - Fuzzy matching with 1 typo tolerance
  - Context snippets in results
  - WCAG 2.1 Level AA compliant

- **Breadcrumb navigation** for deep hierarchies
  - Auto-generated from Sphinx toctree
  - Always visible at top of page
  - WCAG 2.1 Level AA compliant
  - Responsive mobile design

- **Interactive Jupyter notebooks** via JupyterLite
  - Run Python code in-browser (zero install)
  - Full Jupyter environment (WASM-based)
  - Pre-installed: NumPy, SciPy, Matplotlib, dip-smc-pso
  - 5 tutorials converted to interactive notebooks
  - "Run in Browser" buttons on all tutorial pages

### Technical Details
- Dependencies: `sphinx-lunr-search`, `jupyterlite-core`, `jupyterlite-pyodide-kernel`
- Build time: +30s for search indexing, +60s for JupyterLite (one-time)
- Runtime payload: +2MB (search index), +50MB (JupyterLite, cached)
- Browser compatibility: Chromium tested, Firefox/Safari deferred
```

### 4.3 Deployment Checklist

```markdown
# Documentation Enhancement Deployment Checklist

## Pre-Deployment
- [ ] All tests passing (search, breadcrumbs, notebooks)
- [ ] Accessibility audit passed (WCAG 2.1 Level AA)
- [ ] Performance benchmarks met (<200ms search, <10s JupyterLite load)
- [ ] Cross-browser testing complete (Chromium validated)
- [ ] Documentation updated (NAVIGATION.md, CHANGELOG.md, guides/INDEX.md)

## Build Verification
- [ ] Sphinx build succeeds: `sphinx-build -M html docs docs/_build -W`
- [ ] Search index generated: `docs/_build/html/searchindex.json` exists (2MB)
- [ ] JupyterLite built: `docs/_build/html/jupyter/lab/index.html` exists
- [ ] Package wheel copied: `docs/_build/html/_static/wheels/*.whl` exists
- [ ] All static assets present: CSS, JS, fonts

## Functional Testing
- [ ] Search works: Ctrl+K opens modal, returns results
- [ ] Breadcrumbs appear on all pages (except index)
- [ ] "Run in Browser" buttons visible on tutorial pages
- [ ] JupyterLite loads and executes notebooks
- [ ] Package imports work in JupyterLite: `import dip_smc_pso`

## Performance Testing
- [ ] Search latency <200ms (measured in DevTools)
- [ ] JupyterLite load time <10s (first visit)
- [ ] Page load time <2s (with search/breadcrumbs)
- [ ] No console errors in browser

## Accessibility Testing
- [ ] Keyboard navigation works (Tab, Enter, ESC)
- [ ] Screen reader compatible (tested with NVDA/JAWS)
- [ ] Color contrast ratios meet WCAG 2.1 Level AA
- [ ] Focus indicators visible

## Documentation Verification
- [ ] NAVIGATION.md updated with new features
- [ ] CHANGELOG.md entry added
- [ ] guides/INDEX.md updated
- [ ] Tutorial pages link to JupyterLite correctly

## Post-Deployment
- [ ] Verify live site: https://your-docs-domain.com
- [ ] Test search on live site
- [ ] Test JupyterLite on live site
- [ ] Monitor for errors (check analytics/logs)
- [ ] Announce to users (release notes, email, etc.)

## Rollback Plan
If critical issues found:
1. Revert to previous Sphinx build: `git checkout HEAD~1 docs/_build`
2. Disable JupyterLite: Comment out `build_jupyterlite` in `conf.py`
3. Disable search: Remove `sphinx_lunr` from `extensions` in `conf.py`
4. Rebuild: `sphinx-build -M html docs docs/_build -W`
```

---

## Implementation Timeline

### Immediate Priority (Week 1)

**Day 1-2: Full-Text Search (4-6 hours)**
- Install sphinx-lunr-search
- Configure Sphinx extension
- Create search UI (modal, input, results)
- Add keyboard shortcut (Ctrl+K)
- Testing & validation

**Day 3: Breadcrumbs (2-3 hours)**
- Create breadcrumb extension
- Auto-generate from toctree
- Style breadcrumbs (CSS)
- Integrate into layout
- Testing & validation

**Day 4-5: Buffer & Documentation (2 hours)**
- Update NAVIGATION.md, CHANGELOG.md
- Write user guides
- Deploy to staging
- User acceptance testing

### Short-Term (Week 2-3)

**Days 6-12: Interactive Notebooks (10-12 hours)**
- Install JupyterLite
- Build package wheel
- Convert 5 tutorials to notebooks
- Build JupyterLite site
- Add "Run in Browser" buttons
- Testing & validation

**Days 13-14: Deployment & Handoff (2 hours)**
- Deploy to production
- Monitor for issues
- Create deployment guide
- Announce to users

---

## Risk Assessment & Mitigation

### Risk 1: Search Index Too Large (2MB)
**Probability**: LOW
**Impact**: MEDIUM (slow page loads)
**Mitigation**:
- Use lazy loading (load index only when search opened)
- Enable gzip compression (reduces to ~500KB)
- Consider CDN for static assets

### Risk 2: JupyterLite Doesn't Load on Some Browsers
**Probability**: MEDIUM
**Impact**: HIGH (users can't run notebooks)
**Mitigation**:
- Add browser compatibility check (show warning for unsupported browsers)
- Provide fallback: "Download notebook" button
- Test on multiple browsers BEFORE deployment

### Risk 3: Package Wheel Breaks in JupyterLite
**Probability**: LOW
**Impact**: HIGH (notebooks can't import package)
**Mitigation**:
- Test package import in JupyterLite BEFORE deployment
- Pin exact dependency versions in pyproject.toml
- Add automated test: "import dip_smc_pso" in JupyterLite

### Risk 4: Breadcrumbs Break on Orphan Pages
**Probability**: LOW
**Impact**: LOW (minor UI glitch)
**Mitigation**:
- Add fallback: use file path if toctree not found
- Test on all page types (orphan, nested, index)
- Graceful degradation: hide breadcrumbs if empty

### Risk 5: Accessibility Regressions
**Probability**: LOW
**Impact**: HIGH (blocks users with disabilities)
**Mitigation**:
- Run automated accessibility tests (axe-core)
- Manual testing with screen reader
- Follow WCAG 2.1 Level AA guidelines strictly

---

## Success Metrics

### Quantitative Metrics

**Search:**
- Search latency <200ms (95th percentile)
- 821 files indexed
- Search usage: >10% of page views
- Search satisfaction: >80% (user survey)

**Breadcrumbs:**
- Breadcrumbs visible on >95% of pages
- Breadcrumb clicks: >5% of navigation
- Mobile breadcrumb scroll: <10% of users

**Interactive Notebooks:**
- JupyterLite load time <10s (first visit)
- Notebook execution success rate >90%
- Notebook usage: >20% of tutorial page views
- Tutorial completion rate: +15% (compared to static docs)

### Qualitative Metrics

**User Feedback:**
- "Search is fast and accurate"
- "Breadcrumbs help me navigate deep hierarchies"
- "Love that I can run code without installing anything"

**Developer Experience:**
- Zero maintenance (auto-generated from existing sources)
- Fast build times (<2 min total)
- Easy to extend (add more notebooks, update search config)

---

## Future Enhancements (Post-Implementation)

### Phase 5: Advanced Search Features (4-6 hours)
- Filters: file type, category, date
- Search history (localStorage)
- Popular searches
- "Did you mean..." suggestions

### Phase 6: Enhanced Notebooks (6-8 hours)
- Pre-run notebooks (show outputs without execution)
- Progress indicators (cell execution time)
- Download results as PDF
- Share notebook with pre-filled code

### Phase 7: Analytics & Optimization (3-4 hours)
- Track search queries (identify gaps in docs)
- Track notebook usage (popular tutorials)
- A/B test search UI variants
- Optimize search index (reduce size)

---

## Appendix: Technical References

### A. Lunr.js Documentation
- Official docs: https://lunrjs.com/
- Sphinx integration: https://sphinx-lunr-search.readthedocs.io/
- TF-IDF algorithm: https://en.wikipedia.org/wiki/Tf%E2%80%93idf

### B. JupyterLite Documentation
- Official docs: https://jupyterlite.readthedocs.io/
- Pyodide (Python WASM): https://pyodide.org/
- Build config: https://jupyterlite.readthedocs.io/en/latest/reference/cli.html

### C. Sphinx Extension Development
- Custom extensions: https://www.sphinx-doc.org/en/master/development/tutorials/
- Event hooks: https://www.sphinx-doc.org/en/master/extdev/appapi.html#events
- Jinja2 templates: https://jinja.palletsprojects.com/

### D. WCAG 2.1 Accessibility Guidelines
- Overview: https://www.w3.org/WAI/WCAG21/quickref/
- Level AA checklist: https://www.wuhcag.com/wcag-checklist/
- Testing tools: https://www.deque.com/axe/

---

## Conclusion

This ultra-plan provides a comprehensive roadmap for implementing 3 high-ROI documentation enhancements:

1. **Full-text search** - Solves #1 pain point (finding content in 821 files)
2. **Breadcrumbs** - Improves navigation UX for deep hierarchies
3. **Interactive notebooks** - Revolutionizes learning experience (zero-install code execution)

**Total Effort**: 16-21 hours
**Expected Impact**: Transforms already-excellent docs into world-class
**Risk Level**: LOW (all technologies proven, graceful degradation)

**Recommendation**: Implement in phases (search → breadcrumbs → notebooks) to maximize value delivery and minimize risk.

**Next Step**: User approval to proceed with Phase 1 (Full-Text Search, 4-6 hours).
