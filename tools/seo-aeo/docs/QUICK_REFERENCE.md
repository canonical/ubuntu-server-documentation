# SEO/AEO Audit Quick Reference

## Quick Commands

### Run your first audit
```bash
python tools/seo_aeo_analyzer.py
```

### Run audit with custom output
```bash
python tools/seo_aeo_analyzer.py --output audits/audit-2025-12-10.csv
```

### Compare two audits
```bash
python tools/compare_audits.py audits/baseline.csv audits/audit-2025-12-17.csv
```

### Generate comparison report
```bash
python tools/compare_audits.py \
  audits/baseline.csv \
  audits/current.csv \
  --output audits/report.md
```

### Quick start script
```bash
chmod +x tools/run-audit.sh
./tools/run-audit.sh
```

## Metric Reference Card

| Metric | Score 5 | Score 4 | Score 3 | Score 2 | Score 1 |
|--------|---------|---------|---------|---------|---------|
| **Content Depth** | 800+ words | 500-799 | 300-499 | 150-299 | <150 |
| **Internal Links** | 9+ links | 6-8 | 3-5 | 1-2 | 0 |
| **Code Examples** | 5+ blocks | 3-4 | 2 | 1 | 0 |
| **Meta Description** | 50-160 chars | Present | - | Missing | - |
| **Heading Structure** | Perfect H1-H6 | Good | Adequate | Issues | No structure |

## Common Issues & Quick Fixes

### Issue: No Internal Links (Score: 1)
**Fix:** Add 3-5 cross-references
```markdown
See {ref}`related-guide` for more details.
Check out the {term}`glossary-term` definition.
```
**Time:** 5-10 minutes per page
**Impact:** High

### Issue: Short Content (Score: 1-2)
**Fix:** Expand to 300+ words
- Add "Why this matters" section
- Include troubleshooting
- Add examples
**Time:** 30-60 minutes per page
**Impact:** Medium

### Issue: No Prerequisites (Score: 2)
**Fix:** Add prerequisites section
```markdown
## Prerequisites

- Ubuntu 24.04 LTS or later
- Root or sudo access
- Package X installed
```
**Time:** 5 minutes per page
**Impact:** High for how-tos

### Issue: No Version Info (Score: 2)
**Fix:** Add version callout
```markdown
:::{note}
This guide applies to Ubuntu 22.04 LTS and later.
:::
```
**Time:** 2 minutes per page
**Impact:** Medium

### Issue: Multiple H1s (Score: -1)
**Fix:** Convert secondary H1s to H2s
```markdown
# Main Title        ← Only H1
## Section Title    ← H2, not H1
```
**Time:** 1 minute per page
**Impact:** Medium

## Score Interpretation

| Overall Score | Health | Action |
|---------------|--------|--------|
| 4.5 - 5.0 | 🟢 Excellent | Maintain quality |
| 4.0 - 4.4 | 🟢 Good | Minor improvements |
| 3.5 - 3.9 | 🟡 Fair | Moderate improvements needed |
| 3.0 - 3.4 | 🟠 Needs Work | Significant improvements needed |
| < 3.0 | 🔴 Critical | Urgent attention required |

## Prioritization Matrix

| Impact | Effort | Priority | Example |
|--------|--------|----------|---------|
| High | Low | 🔥 DO NOW | Add internal links |
| High | Medium | ⚡ DO NEXT | Add prerequisites |
| High | High | 📅 PLAN | Expand thin content |
| Medium | Low | ✅ QUICK WIN | Fix multiple H1s |
| Low | High | 🤔 RECONSIDER | Complete rewrites |

## Typical Workflow

```
Week 1: Baseline
├─ Run initial audit
├─ Review summary
└─ Identify top 10 priority pages

Week 2-3: Quick Wins
├─ Fix all multiple H1 issues
├─ Add internal links to top 20 pages
└─ Add prerequisites to how-to guides

Week 4: Measure
├─ Run new audit
├─ Compare with baseline
└─ Assess impact

Week 5+: Iterate
├─ Expand thin content
├─ Add code examples
└─ Continue improvements
```

## File Organization

```
ubuntu-server-documentation/
├── tools/
│   ├── seo_aeo_analyzer.py      # Main analyzer
│   ├── compare_audits.py        # Comparison tool
│   ├── run-audit.sh             # Quick start script
│   └── README.md                # Full documentation
├── audits/
│   ├── baseline.csv             # Initial baseline
│   ├── audit-2025-12-10.csv     # Regular audits
│   ├── audit-2025-12-17.csv
│   └── report-2025-12-17.md     # Comparison reports
└── docs/                        # Your documentation
```

## Automation Options

### Cron (Linux/Mac)
```bash
# Run every Monday at 9 AM
0 9 * * 1 cd ~/ubuntu-server-documentation && python tools/seo_aeo_analyzer.py --output audits/audit-$(date +\%Y-\%m-\%d).csv
```

### Task Scheduler (Windows)
```powershell
# Create scheduled task
schtasks /create /tn "Doc Audit" /tr "python C:\path\to\tools\seo_aeo_analyzer.py" /sc weekly /d MON /st 09:00
```

### GitHub Actions
See `.github/workflows/seo-aeo-audit.yml`

## Getting Help

### Check tool status
```bash
python tools/seo_aeo_analyzer.py --help
```

### Verify Python version (requires 3.7+)
```bash
python3 --version
```

### Test on small set
```bash
# Temporarily modify to analyze just one directory
python tools/seo_aeo_analyzer.py --docs-dir docs/tutorial
```

## Best Practices

✅ **DO:**
- Run audits regularly (weekly or monthly)
- Keep baseline for comparison
- Focus on high-impact, low-effort fixes first
- Track trends, not just absolute scores
- Automate where possible

❌ **DON'T:**
- Obsess over perfect 5.0 scores
- Change everything at once
- Ignore context (some pages are naturally shorter)
- Compare across different doc sets
- Forget to commit audit results

## Success Metrics

Track these over time:
- Average overall score (target: 4.3+)
- Pages with internal links (target: 90%+)
- Pages under 300 words (target: <10%)
- Pages with prerequisites (target: 100% of how-tos)
- Pages with version info (target: 80%+)

## Emergency Triage

If you need to quickly identify problems:

```bash
# Find pages with score < 3.0
awk -F',' '$19 < 3.0 {print $19, $1}' audit.csv | sort -n

# Count pages with no internal links
awk -F',' '$4 == 1 {count++} END {print count}' audit.csv

# Find pages with multiple H1s
grep "Multiple H1s" audit.csv

# List shortest pages
awk -F',' '$2 == 1 {print $1}' audit.csv
```

---

**Last Updated:** 2025-12-10  
**Version:** 1.0
