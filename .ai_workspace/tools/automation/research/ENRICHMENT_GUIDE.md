# Citation Enrichment Guide

## Problem: Missing Supplemental Data

Your citations currently have:
- ✅ **DOI** (permanent identifier)
- ✅ **Title, Authors, Year, Venue**
- ✅ **URL**

But missing:
- ❌ **Citation counts** (how many times cited)
- ❌ **Abstracts** (paper summaries)
- ❌ **Influence metrics** (academic impact)

## Solution: Post-Process Enrichment

I've created `enrich_citations.py` which adds this missing data using alternative APIs.

---

## 📊 Data Sources Comparison

| Source | Citation Counts | Abstracts | Influence | Rate Limit | Cost |
|--------|----------------|-----------|-----------|------------|------|
| **OpenAlex** | ✅ Excellent | ✅ Good | ❌ No | 10/sec (100 with email) | Free |
| **Semantic Scholar (DOI)** | ✅ Good | ✅ Good | ✅ Yes | 100 per 5 min | Free |
| **CrossRef** | ✅ Limited | ❌ Rare | ❌ No | 50/sec | Free |

**Recommendation**: Use OpenAlex as primary source (faster, more reliable)

---

## 🚀 Quick Start

### Option 1: Enrich All Completed Batches (Recommended)

```bash
# Enrich all 7 completed batches at once
python .dev_tools/research/enrich_citations.py --all

# With email for better rate limits
python .dev_tools/research/enrich_citations.py --all --email your@email.com
```

**Output**: Creates `*_enriched.json` files with added data

**Time**: ~5-10 minutes for all completed batches (~350 citations)

---

### Option 2: Enrich Specific Batch

```bash
# Enrich just one batch
python .dev_tools/research/enrich_citations.py academic/batch_03_analysis_high.json

# With Semantic Scholar API key (optional, for higher limits)
python .dev_tools/research/enrich_citations.py \
  academic/batch_03_analysis_high.json \
  --email your@email.com \
  --semantic-key YOUR_API_KEY
```

---

### Option 3: Wait for Running Batches, Then Enrich

```bash
# Check progress
python .dev_tools/research/check_all_batches.py

# When complete, enrich everything
python .dev_tools/research/enrich_citations.py --all --email your@email.com
```

---

## 📝 What Gets Added

### Before Enrichment:
```json
{
  "title": "Sliding Mode Control: Theory and Applications",
  "authors": ["Christopher Edwards", "Sarah Spurgeon"],
  "year": 1998,
  "doi": "10.1201/9781498701822",
  "url": "https://doi.org/10.1201/9781498701822",
  "venue": "CRC Press",
  "source": "crossref"
}
```

### After Enrichment:
```json
{
  "title": "Sliding Mode Control: Theory and Applications",
  "authors": ["Christopher Edwards", "Sarah Spurgeon"],
  "year": 1998,
  "doi": "10.1201/9781498701822",
  "url": "https://doi.org/10.1201/9781498701822",
  "venue": "CRC Press",
  "source": "crossref",
  "citation_count": 3847,
  "abstract": "This book presents the theory and applications...",
  "open_access_url": "https://arxiv.org/pdf/...",
  "enrichment_source": "openalex"
}
```

---

## 🔧 How It Works

1. **Reads your existing citation JSON files**
2. **For each citation with a DOI:**
   - First tries OpenAlex API (fast, reliable)
   - Falls back to Semantic Scholar DOI lookup if needed
3. **Adds supplemental data:**
   - Citation counts (how influential)
   - Abstracts (for context)
   - Open access links (free PDF access)
   - Influence scores (Semantic Scholar)
4. **Saves enriched version** (`*_enriched.json`)
5. **Original files remain unchanged**

### Why DOI Lookup Works (vs Query Search)

- **Query search**: `?query=` → Empty query bug → 400 error
- **DOI lookup**: `/paper/DOI:10.xxx` → Direct access → Works perfectly!

---

## 📈 Expected Results

Based on 7 completed batches (~350 citations):

| Metric | Expected |
|--------|----------|
| Total citations | ~350 |
| Successfully enriched | ~320 (91%) |
| Already had data | ~0 (first run) |
| Failed (no DOI/not found) | ~30 (9%) |
| Time required | 5-10 minutes |

---

## 🎯 Benefits

### Academic Quality:
- **Citation counts** → Shows impact of your references
- **Abstracts** → Provides context for readers
- **Influence metrics** → Highlights seminal papers

### Documentation Value:
- Makes your bibliography more informative
- Helps readers assess source credibility
- Shows you used high-impact references

### Future Use:
- Can sort citations by impact
- Generate "most influential papers" lists
- Create citation network visualizations

---

## 🔮 Next Steps After Enrichment

### 1. Generate Enhanced Bibliography
```bash
python .dev_tools/research/bibtex_generator.py \
  --input batch_03_analysis_high_enriched.json \
  --output enhanced_bibliography.bib \
  --include-citation-counts
```

### 2. Create Citation Report
```python
# Analyze enriched citations
import json

with open('academic/batch_03_analysis_high_enriched.json') as f:
    data = json.load(f)

# Find most influential papers
influential = []
for claim in data['claims']:
    for cite in claim.get('citations', []):
        if cite.get('citation_count', 0) > 100:
            influential.append(cite)

# Sort by citation count
influential.sort(key=lambda x: x.get('citation_count', 0), reverse=True)

print("Top 10 Most Cited References:")
for cite in influential[:10]:
    print(f"  {cite.get('citation_count'):5d} - {cite['title'][:60]}")
```

### 3. Fix Empty Query Bug (Prevent Future Issues)
```bash
# After batches complete, fix the root cause
# See: .dev_tools/research/BUGFIX_EMPTY_QUERY.md
```

---

## 🆘 Troubleshooting

### Rate Limit Errors
```bash
# Solution: Add email for polite pool (10x faster)
--email your@email.com
```

### DOI Not Found
- Normal for ~10% of citations
- Some papers not in OpenAlex/Semantic Scholar
- Original citation data still valid

### Slow Performance
- Expected: ~1-2 seconds per citation
- Total time: ~5-10 minutes for 350 citations
- Can run overnight if needed

---

## 🎉 Summary

**You can compensate for missing supplemental data by:**

1. ✅ Running `enrich_citations.py --all` (5-10 minutes)
2. ✅ Using OpenAlex API (free, excellent coverage)
3. ✅ DOI lookup bypasses the empty query bug
4. ✅ Adds citation counts, abstracts, influence metrics
5. ✅ Original data quality remains excellent (CrossRef)

**Your references are already academically valid** - this just makes them even better!
