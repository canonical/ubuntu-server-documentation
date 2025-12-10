# SEO & AEO Audit Tools

Automated tools for analyzing and tracking documentation quality metrics for search engine optimization (SEO) and answer engine optimization (AEO).

## Tools Overview

### 1. `seo_aeo_analyzer.py`
Main analysis tool that scans documentation files and scores them against SEO and AEO metrics.

**Features:**
- Analyzes all Markdown files in tutorial/, how-to/, explanation/, and reference/ directories
- Scores 14 different metrics on a 1-5 scale
- Generates detailed CSV output with per-page scores
- Provides summary statistics and identifies critical issues

**Usage:**
```bash
# Basic usage (analyzes docs/ directory)
python tools/seo_aeo_analyzer.py

# Specify custom docs directory and output file
python tools/seo_aeo_analyzer.py --docs-dir ../other-docs --output audit-2025-12-10.csv

# Suppress summary output
python tools/seo_aeo_analyzer.py --quiet
```

**Output:**
- CSV file with detailed metrics per page
- Console summary with averages, top/bottom performers, and critical issues

### 2. `compare_audits.py`
Comparison tool for tracking changes between two audit runs over time.

**Features:**
- Compares two audit CSV files
- Identifies improvements and regressions
- Tracks metric-by-metric changes
- Generates markdown comparison report

**Usage:**
```bash
# Compare two audits and print to console
python tools/compare_audits.py baseline.csv current.csv

# Generate markdown report file
python tools/compare_audits.py audit-2025-12-10.csv audit-2025-12-17.csv --output weekly-report.md
```

**Output:**
- Markdown report showing:
  - Overall score changes
  - Top improvements and regressions
  - Metric-by-metric comparison
  - New/removed pages
  - Recommendations

## Metrics Explained

### SEO Metrics (Search Engine Optimization)

1. **Title Tag Quality** (1-5)
   - Checks for meta description presence and length (50-160 chars)
   - Evaluates keyword inclusion

2. **Content Depth** (1-5)
   - Based on word count
   - 5: 800+ words
   - 4: 500-799 words
   - 3: 300-499 words
   - 2: 150-299 words
   - 1: <150 words

3. **Heading Structure** (1-5)
   - Proper H1-H6 hierarchy
   - Single H1 per page
   - Descriptive headings

4. **Internal Links** (1-5)
   - Counts MyST refs, term references, and relative links
   - 5: 9+ links
   - 4: 6-8 links
   - 3: 3-5 links
   - 2: 1-2 links
   - 1: 0 links

5. **Meta Description** (1-5)
   - Same as Title Tag Quality
   - Compelling description for search results

6. **URL Quality** (1-5)
   - Descriptive filename
   - Hyphenated words
   - Reasonable length (<60 chars ideal)

7. **Freshness** (1-5)
   - Mentions Ubuntu versions
   - Specifically mentions recent releases (24.04, Noble)

### AEO Metrics (Answer Engine Optimization)

1. **Direct Answer Quality** (1-5)
   - First paragraph clarity
   - Direct answer to implied question
   - Length and completeness

2. **Structured Content** (1-5)
   - Use of lists (bullet, numbered)
   - Code blocks
   - Clear sections

3. **Semantic Clarity** (1-5)
   - MyST semantic markup ({term}, {manpage}, etc.)
   - Acronym expansions
   - Clear definitions

4. **Code Examples** (1-5)
   - Number of code blocks
   - 5: 5+ examples
   - 4: 3-4 examples
   - 3: 2 examples
   - 2: 1 example
   - 1: 0 examples

5. **Prerequisites** (1-5)
   - Presence of prerequisites section
   - Clarity of requirements
   - More important for how-to guides

6. **Step Format** (1-5)
   - Numbered procedural steps
   - Most relevant for how-to guides
   - Clear sequence

7. **Version Specificity** (1-5)
   - Ubuntu version mentions
   - Version-specific callouts
   - Currency (24.04 LTS references)

## Workflow for Periodic Audits

### Initial Baseline Audit
```bash
# Run initial audit
cd /path/to/ubuntu-server-documentation
python tools/seo_aeo_analyzer.py --output audits/baseline-2025-12-10.csv

# Store baseline for future comparisons
mkdir -p audits
cp seo-aeo-audit.csv audits/baseline-2025-12-10.csv
```

### Regular Re-audits (Weekly/Monthly)
```bash
# Run new audit
python tools/seo_aeo_analyzer.py --output audits/audit-$(date +%Y-%m-%d).csv

# Compare with baseline
python tools/compare_audits.py \
    audits/baseline-2025-12-10.csv \
    audits/audit-$(date +%Y-%m-%d).csv \
    --output audits/report-$(date +%Y-%m-%d).md

# Review the report
cat audits/report-$(date +%Y-%m-%d).md
```

### Automated Scheduled Audits
Add to cron or CI/CD pipeline:

```bash
# Example cron entry (every Monday at 9 AM)
0 9 * * 1 cd /path/to/ubuntu-server-documentation && python tools/seo_aeo_analyzer.py --output audits/audit-$(date +%Y-%m-%d).csv
```

**GitHub Actions Example:**
```yaml
name: Weekly SEO/AEO Audit
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
  workflow_dispatch:

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Run SEO/AEO Audit
        run: |
          python tools/seo_aeo_analyzer.py --output audit-$(date +%Y-%m-%d).csv
      
      - name: Upload Audit Results
        uses: actions/upload-artifact@v4
        with:
          name: seo-aeo-audit
          path: audit-*.csv
```

## Integration with AI Agents

These tools generate structured CSV data that can be easily consumed by AI agents for deeper analysis. See `agent-prompt-template.md` for a reusable prompt that guides AI analysis of the audit results.

## Customization

### Adding New Metrics

To add a new metric to `seo_aeo_analyzer.py`:

1. Add scoring logic in the `analyze_page()` method
2. Add the score to either `seo_metrics` or `aeo_metrics` list
3. Update the `PageMetrics` dataclass with the new field
4. Update the `metrics` dict in `print_summary()` for reporting

### Adjusting Scoring Thresholds

Edit the scoring functions in `seo_aeo_analyzer.py`. For example, to make word count requirements stricter:

```python
# Original
if word_count >= 800:
    depth_score = 5

# Stricter
if word_count >= 1200:
    depth_score = 5
```

### Filtering Analyzed Files

Modify the `find_content_files()` method to change which files are analyzed:

```python
def find_content_files(self) -> List[Path]:
    # Add more directories
    target_dirs = ["tutorial", "how-to", "explanation", "reference", "guides"]
    
    # Skip certain patterns
    for md_file in dir_path.rglob("*.md"):
        if md_file.name != "index.md" and "deprecated" not in str(md_file):
            content_files.append(md_file)
```

## Troubleshooting

### "No files found"
- Check that `--docs-dir` points to the correct documentation directory
- Ensure target directories (tutorial/, how-to/, etc.) exist

### "Error analyzing file"
- Check file encoding (should be UTF-8)
- Verify Markdown syntax is valid
- Check for unusual characters in frontmatter

### "Module not found"
- Ensure you're running Python 3.7+
- All required modules are in Python standard library (no pip install needed)

## Best Practices

1. **Regular Audits:** Run audits at least monthly to track progress
2. **Baseline Comparison:** Always compare against baseline to see trends
3. **Focus on Trends:** Individual page scores matter less than overall trends
4. **Prioritize Issues:** Address high-impact, low-effort issues first (like internal linking)
5. **Document Changes:** Keep audit reports in version control to track improvements
6. **Automate:** Use CI/CD to run audits automatically on pull requests

## File Locations

```
ubuntu-server-documentation/
├── tools/
│   ├── seo_aeo_analyzer.py      # Main analysis script
│   ├── compare_audits.py        # Comparison tool
│   ├── README.md                # This file
│   └── agent-prompt-template.md # AI agent prompt
├── audits/                      # Store audit results here
│   ├── baseline-2025-12-10.csv
│   ├── audit-2025-12-17.csv
│   └── report-2025-12-17.md
└── docs/                        # Documentation to analyze
    ├── tutorial/
    ├── how-to/
    ├── explanation/
    └── reference/
```

## Contributing

To contribute improvements to these tools:

1. Test changes on a subset of files first
2. Ensure backward compatibility with existing CSV format
3. Update this README with any new features
4. Add examples for new functionality

## License

These tools are part of the Ubuntu Server Documentation project and follow the same license.
