#!/usr/bin/env python3
"""
Verify DOIs for Batch 08 citations.

Checks that all DOIs resolve correctly and reports any issues.
"""

import requests
from typing import Dict, List
import time

# All 19 unique citations with their DOIs
citations = [
    {
        "name": "Stone (1978)",
        "bibtex_key": "stone1978cross",
        "doi": "10.1080/02331887808801414",
        "type": "journal"
    },
    {
        "name": "Barnett & Lewis (1994)",
        "bibtex_key": "barnett1994outliers",
        "doi": "10.1002/bimj.4710370219",
        "type": "book"
    },
    {
        "name": "Efron & Tibshirani (1993)",
        "bibtex_key": "efron1993bootstrap",
        "doi": "10.1007/978-1-4899-4541-9",
        "type": "book"
    },
    {
        "name": "Demsar (2006)",
        "bibtex_key": "demsar2006statistical",
        "doi": "N/A",
        "type": "journal"
    },
    {
        "name": "Wilcoxon (1945)",
        "bibtex_key": "wilcoxon1945individual",
        "doi": "10.2307/3001968",
        "type": "journal"
    },
    {
        "name": "Shapiro & Wilk (1965)",
        "bibtex_key": "shapiro1965analysis",
        "doi": "10.1093/biomet/52.3-4.591",
        "type": "journal"
    },
    {
        "name": "Pearson (1895)",
        "bibtex_key": "pearson1895note",
        "doi": "10.1098/rspl.1895.0041",
        "type": "journal"
    },
    {
        "name": "Cohen (1988)",
        "bibtex_key": "cohen1988statistical",
        "doi": "10.4324/9780203771587",
        "type": "book"
    },
    {
        "name": "Utkin (1977)",
        "bibtex_key": "utkin1977variable",
        "doi": "10.1109/TAC.1977.1101446",
        "type": "journal"
    },
    {
        "name": "Levant (2003)",
        "bibtex_key": "levant2003higher",
        "doi": "10.1080/0020717031000099029",
        "type": "journal"
    },
    {
        "name": "Clerc & Kennedy (2002)",
        "bibtex_key": "clerc2002particle",
        "doi": "10.1109/4235.985692",
        "type": "journal"
    },
    {
        "name": "Storn & Price (1997)",
        "bibtex_key": "storn1997differential",
        "doi": "10.1023/A:1008202821328",
        "type": "journal"
    },
    {
        "name": "Nelder & Mead (1965)",
        "bibtex_key": "nelder1965simplex",
        "doi": "10.1093/comjnl/7.4.308",
        "type": "journal"
    },
    {
        "name": "Nocedal & Wright (2006)",
        "bibtex_key": "nocedal2006numerical",
        "doi": "10.1007/978-0-387-30303-1",
        "type": "book"
    },
    {
        "name": "Goldberg (1989)",
        "bibtex_key": "goldberg1989genetic",
        "doi": "N/A",
        "type": "book"
    },
    {
        "name": "Deb (2001)",
        "bibtex_key": "deb2001multiobjective",
        "doi": "N/A",
        "type": "book"
    },
    {
        "name": "Camacho & Bordons (2013)",
        "bibtex_key": "camacho2013model",
        "doi": "10.1007/978-0-85729-398-5",
        "type": "book"
    },
    {
        "name": "Hairer, Norsett & Wanner (1993)",
        "bibtex_key": "hairer1993solving",
        "doi": "10.1007/978-3-540-78862-1",
        "type": "book"
    },
    {
        "name": "Ogata (2010)",
        "bibtex_key": "ogata2010modern",
        "doi": "N/A",
        "type": "book"
    }
]

def check_doi(doi: str) -> tuple[bool, int, str]:
    """
    Check if a DOI resolves correctly.

    Returns:
        (success, status_code, redirect_url)
    """
    if doi == "N/A":
        return (True, 0, "N/A - Book without DOI")

    url = f"https://doi.org/{doi}"
    try:
        # Use HEAD request to avoid downloading full content
        response = requests.head(url, allow_redirects=True, timeout=10)

        if response.status_code == 200:
            return (True, response.status_code, response.url)
        elif response.status_code in [301, 302, 303, 307, 308]:
            # Redirects are normal for DOIs
            return (True, response.status_code, response.url)
        else:
            return (False, response.status_code, url)
    except requests.exceptions.RequestException as e:
        return (False, 0, str(e))

print("=" * 100)
print("DOI VERIFICATION - BATCH 08")
print("=" * 100)
print()

results = {
    "success": [],
    "na_books": [],
    "failed": []
}

for i, citation in enumerate(citations, 1):
    print(f"[{i}/19] Checking: {citation['name']}")
    print(f"  BibTeX: {citation['bibtex_key']}")
    print(f"  DOI: {citation['doi']}")

    success, status, url = check_doi(citation['doi'])

    if citation['doi'] == "N/A":
        results['na_books'].append(citation)
        print(f"  [SKIP] Book without DOI (acceptable)")
    elif success:
        results['success'].append(citation)
        print(f"  [OK] Resolves to: {url[:80]}...")
    else:
        results['failed'].append((citation, status, url))
        print(f"  [FAIL] Status: {status}, Error: {url}")

    print()
    time.sleep(0.5)  # Be polite to DOI servers

print("=" * 100)
print("SUMMARY")
print("=" * 100)
print(f"Total citations: {len(citations)}")
print(f"Successful DOIs: {len(results['success'])}")
print(f"Books without DOI (N/A): {len(results['na_books'])}")
print(f"Failed DOIs: {len(results['failed'])}")
print()

if results['failed']:
    print("[!] FAILED DOIS:")
    for citation, status, error in results['failed']:
        print(f"  - {citation['name']} ({citation['doi']})")
        print(f"    Status: {status}, Error: {error}")
    print()
else:
    print("[OK] All DOIs verified successfully!")
    print()

print("Books without DOI (acceptable):")
for citation in results['na_books']:
    print(f"  - {citation['name']} ({citation['bibtex_key']})")

print()
print("=" * 100)
