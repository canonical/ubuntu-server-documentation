# SEO & AEO Audit Analysis - Reusable AI Agent Prompt

Use this prompt template to have an AI agent analyze audit results and generate actionable recommendations.

---

## Prompt Template

```
I need you to analyze the results of an SEO and AEO audit of documentation pages. 

I have a CSV file at `[PATH_TO_CSV]` that contains detailed scoring for each documentation page across 14 metrics:

**SEO Metrics (1-5 scale):**
1. Title Tag Quality - Meta description presence and quality
2. Content Depth - Word count and comprehensiveness  
3. Heading Structure - Proper H1-H6 hierarchy
4. Internal Links - Cross-references to other pages
5. Meta Description - Description for search results
6. URL Quality - Descriptive, keyword-rich filenames
7. Freshness - Version information and currency

**AEO Metrics (1-5 scale):**
1. Direct Answer Quality - First paragraph clarity
2. Structured Content - Lists, code blocks, clear sections
3. Semantic Clarity - Term markup, acronym expansions
4. Code Examples - Presence of practical code
5. Prerequisites - Clear requirements stated upfront
6. Step Format - Numbered procedural steps
7. Version Specificity - Ubuntu version mentions

Please analyze this audit data and provide:

## 1. Executive Summary
- Total pages analyzed
- Average scores (SEO, AEO, Overall)
- Overall health assessment (Excellent/Good/Needs Work/Critical)

## 2. Critical Issues Analysis
Identify and rank issues by impact:
- What percentage of pages have critical issues (score < 2) in each metric?
- Which metrics have the lowest average scores?
- Which issues affect the most pages?

## 3. Top Performing Pages
- List the top 10 pages by overall score
- Identify what makes them successful
- Extract patterns/best practices

## 4. Pages Needing Immediate Attention
- List bottom 10 pages by overall score
- Identify specific issues for each
- Suggest concrete fixes

## 5. Category Analysis
Break down scores by documentation category:
- tutorial/
- how-to/
- explanation/
- reference/

Which categories perform best/worst? Why?

## 6. Actionable Recommendations

Provide recommendations in three tiers:

### Immediate (Next 30 days) - High Impact, Low Effort
- List 3-5 specific actions
- Estimate impact (% improvement expected)
- Estimate effort (hours)
- Prioritize by ROI

### Short-term (1-3 months) - High Impact, Medium Effort
- List 5-8 specific actions
- Include implementation approach

### Long-term (3-6 months) - Sustained Improvement
- Strategic initiatives
- Process improvements
- Automation opportunities

## 7. Metrics to Track
- Which metrics should be monitored most closely?
- What are realistic targets for improvement?
- Suggest a dashboard or tracking approach

## 8. Quick Win Opportunities
- Identify pages that are close to high scores (4.0-4.4) 
- Suggest minimal changes to push them over 4.5
- Estimate impact of these quick fixes

Please make your analysis specific, data-driven, and actionable. Reference actual page names and provide concrete examples where possible.
```

---

## Usage Examples

### Example 1: Initial Audit Analysis

```
I need you to analyze the results of an SEO and AEO audit of documentation pages.

I have a CSV file at `seo-aeo-audit.csv` that contains detailed scoring for each documentation page across 14 metrics:

[... rest of prompt template ...]

Additionally, compare your findings to these benchmarks:
- Industry standard for technical documentation: 4.0/5.0 overall
- Our target: 4.3/5.0 overall within 6 months
- Critical threshold: Any page below 3.0/5.0 needs immediate attention
```

### Example 2: Follow-up Analysis After Improvements

```
I need you to analyze the results of an SEO and AEO audit of documentation pages.

I have TWO CSV files:
- Baseline audit: `audits/baseline-2025-12-10.csv` 
- Current audit: `audits/audit-2025-12-17.csv`

[... rest of prompt template ...]

Additionally:
1. Compare the two audits to identify improvements and regressions
2. Assess whether our improvement efforts are working
3. Recommend whether to continue current strategies or pivot
4. Identify which pages improved the most and why
```

### Example 3: Category-Specific Deep Dive

```
I need you to analyze the results of an SEO and AEO audit of documentation pages.

I have a CSV file at `seo-aeo-audit.csv`.

[... include metric definitions ...]

Focus your analysis specifically on the "how-to" category pages:
1. What's the average score for how-to guides?
2. What are the most common issues in how-to pages?
3. Which how-to guides are exemplary? What makes them good?
4. Create a checklist for writers creating new how-to guides
5. Suggest a template for how-to pages that would score 4.5+
```

### Example 4: Quick Triage Analysis

```
I need a quick triage analysis of an SEO/AEO audit.

CSV file: `seo-aeo-audit.csv`

Provide a condensed analysis focused on:
1. What are the top 3 most critical issues affecting the most pages?
2. What are the top 5 pages that need immediate attention?
3. What's the single highest-impact action we could take this week?
4. Quick win: What pages are closest to 4.5+ and just need minor tweaks?

Keep the response concise and action-oriented - I need to present this in a 10-minute standup.
```

---

## Prompt Customization Tips

### Add Context About Your Team
```
Additional context:
- Team size: 2 technical writers, 3 developers contributing docs
- Time available: 10 hours/week for doc improvements  
- Primary goal: Improve search traffic from Google by 50%
- Secondary goal: Better LLM extraction for AI assistants
```

### Add Specific Constraints
```
Constraints:
- Cannot restructure URLs (would break existing links)
- Cannot add more than 2 hours of work per writer per week
- Must maintain existing Diátaxis structure
- All improvements must be backward compatible
```

### Add Business Context
```
Business context:
- Documentation supports Ubuntu Server 22.04 LTS and 24.04 LTS
- Primary audience: System administrators, DevOps engineers
- Top search queries: [list if known]
- Competitor documentation: [link to compare against]
```

### Request Specific Outputs
```
Output format requested:
1. Executive summary (max 300 words)
2. Top 10 action items in GitHub issue format
3. CSV file with prioritized page fixes
4. Draft email to team explaining findings
```

---

## Integration with Tools

### After Running Analyzer
```bash
# Run audit
python tools/seo_aeo_analyzer.py --output audit.csv

# Then use this prompt with the AI agent:
"I have an audit CSV at audit.csv. [insert prompt template]"
```

### After Running Comparison
```bash
# Compare audits
python tools/compare_audits.py baseline.csv current.csv --output report.md

# Then use this follow-up prompt:
"I have a comparison report at report.md and two CSVs (baseline.csv and current.csv). 
Analyze the changes and recommend whether our strategy is working. [insert relevant 
sections of prompt template]"
```

### For Continuous Monitoring
```bash
# Set up weekly analysis
# In crontab or CI/CD:
0 9 * * 1 python tools/seo_aeo_analyzer.py --output audits/audit-$(date +%Y-%m-%d).csv && \
  [trigger AI agent with prompt template]
```

---

## Expected AI Agent Capabilities

For best results, use an AI agent that can:
- Read and parse CSV files
- Perform statistical analysis
- Compare datasets
- Generate markdown reports
- Access context about documentation best practices
- Suggest specific code/content changes

Recommended models:
- Claude 3.5 Sonnet or newer (excellent for technical analysis)
- GPT-4 or GPT-4 Turbo (good general analysis)
- Any model with large context window (100k+ tokens ideal)

---

## Sample Output Structure

The AI agent following this prompt should generate:

```markdown
# SEO & AEO Audit Analysis Report

## Executive Summary
[3-4 paragraphs with key findings]

## Critical Issues
### Issue 1: Internal Linking (Impact: Critical)
- Affects: 212 pages (91.4%)
- Current avg score: 1.14/5.0
- Impact: Search rankings, user navigation
- **Action:** [specific recommendation]

[... more issues ...]

## Top Performing Pages
1. page-name.md (4.71/5.0) - Excellent because...
[... more pages ...]

## Immediate Actions (Next 30 Days)
- [ ] **Add internal links to all how-to guides** 
  - Impact: +40% SEO score improvement
  - Effort: 40 hours
  - ROI: High
  - How: [specific steps]

[... more actions ...]

## Tracking & Success Metrics
- Monitor: Internal links per page (target: 3-5)
- Goal: Overall score from 4.03 → 4.30 by [date]
- Review: Weekly comparison reports

[... rest of report ...]
```

---

## Version History

- **v1.0** (2025-12-10): Initial prompt template
- Add your updates here as you refine the prompt

---

## Tips for Success

1. **Be Specific:** The more context you provide, the better the analysis
2. **Iterate:** Start with a broad analysis, then ask follow-up questions
3. **Request Examples:** Ask the AI to show specific before/after examples
4. **Validate Recommendations:** Not all AI suggestions will be applicable - use judgment
5. **Track Changes:** Document which recommendations you implement
6. **Compare Results:** Re-run audits after changes to measure impact

---

## Related Files

- `seo_aeo_analyzer.py` - Generates the CSV data
- `compare_audits.py` - Compares two audits over time
- `README.md` - Full documentation for the audit tools
