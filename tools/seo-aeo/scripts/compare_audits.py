#!/usr/bin/env python3
"""
SEO & AEO Audit Comparison Tool
Compare two audit CSV files to track improvements or regressions over time.

Usage:
    python compare_audits.py baseline.csv current.csv [--output report.md]

Author: Ubuntu Server Documentation Team
Date: December 2025
"""

import csv
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class AuditComparison:
    """Compare two audit results and generate improvement report."""
    
    def __init__(self, baseline_file: str, current_file: str):
        self.baseline_file = baseline_file
        self.current_file = current_file
        self.baseline_data = {}
        self.current_data = {}
        
    def load_audit(self, filepath: str) -> Dict[str, Dict]:
        """Load audit CSV into dictionary keyed by file path."""
        data = {}
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                file_path = row['file_path']
                # Convert numeric fields
                for key in row:
                    if key not in ['file_path', 'category', 'notes']:
                        try:
                            row[key] = float(row[key])
                        except (ValueError, KeyError):
                            pass
                data[file_path] = row
        return data
    
    def compare(self) -> Dict:
        """Compare baseline and current audits."""
        self.baseline_data = self.load_audit(self.baseline_file)
        self.current_data = self.load_audit(self.current_file)
        
        # Find common pages
        baseline_pages = set(self.baseline_data.keys())
        current_pages = set(self.current_data.keys())
        
        common_pages = baseline_pages & current_pages
        new_pages = current_pages - baseline_pages
        removed_pages = baseline_pages - current_pages
        
        # Calculate changes for common pages
        improvements = []
        regressions = []
        unchanged = []
        
        for page in common_pages:
            baseline = self.baseline_data[page]
            current = self.current_data[page]
            
            baseline_score = baseline['overall_score']
            current_score = current['overall_score']
            change = current_score - baseline_score
            
            if change > 0.1:
                improvements.append((page, baseline_score, current_score, change))
            elif change < -0.1:
                regressions.append((page, baseline_score, current_score, change))
            else:
                unchanged.append((page, baseline_score, current_score, change))
        
        # Sort by magnitude of change
        improvements.sort(key=lambda x: x[3], reverse=True)
        regressions.sort(key=lambda x: x[3])
        
        # Calculate aggregate statistics
        baseline_avg = sum(self.baseline_data[p]['overall_score'] for p in common_pages) / len(common_pages)
        current_avg = sum(self.current_data[p]['overall_score'] for p in common_pages) / len(common_pages)
        
        # Metric-specific changes
        metric_changes = {}
        metrics = ['title_tag', 'content_depth', 'heading_structure', 'internal_links',
                   'meta_description', 'url_quality', 'freshness', 'direct_answer',
                   'structure', 'semantic_clarity', 'code_examples', 'prerequisites',
                   'step_format', 'version_info']
        
        for metric in metrics:
            baseline_vals = [self.baseline_data[p][metric] for p in common_pages]
            current_vals = [self.current_data[p][metric] for p in common_pages]
            baseline_metric_avg = sum(baseline_vals) / len(baseline_vals)
            current_metric_avg = sum(current_vals) / len(current_vals)
            change = current_metric_avg - baseline_metric_avg
            metric_changes[metric] = {
                'baseline': baseline_metric_avg,
                'current': current_metric_avg,
                'change': change,
                'change_pct': (change / baseline_metric_avg * 100) if baseline_metric_avg > 0 else 0
            }
        
        return {
            'common_pages': len(common_pages),
            'new_pages': len(new_pages),
            'removed_pages': len(removed_pages),
            'baseline_avg': baseline_avg,
            'current_avg': current_avg,
            'overall_change': current_avg - baseline_avg,
            'improvements': improvements,
            'regressions': regressions,
            'unchanged': unchanged,
            'metric_changes': metric_changes,
            'new_page_list': sorted(new_pages),
            'removed_page_list': sorted(removed_pages)
        }
    
    def generate_report(self, comparison: Dict, output_file: str = None):
        """Generate markdown comparison report."""
        lines = []
        
        lines.append("# SEO & AEO Audit Comparison Report")
        lines.append("")
        lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"**Baseline:** {self.baseline_file}")
        lines.append(f"**Current:** {self.current_file}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Executive Summary
        lines.append("## Executive Summary")
        lines.append("")
        lines.append(f"- **Total pages compared:** {comparison['common_pages']}")
        lines.append(f"- **New pages added:** {comparison['new_pages']}")
        lines.append(f"- **Pages removed:** {comparison['removed_pages']}")
        lines.append(f"- **Baseline average score:** {comparison['baseline_avg']:.2f}/5.0")
        lines.append(f"- **Current average score:** {comparison['current_avg']:.2f}/5.0")
        
        change = comparison['overall_change']
        change_pct = (change / comparison['baseline_avg'] * 100) if comparison['baseline_avg'] > 0 else 0
        
        if change > 0:
            emoji = "📈"
            direction = "improved"
        elif change < 0:
            emoji = "📉"
            direction = "decreased"
        else:
            emoji = "➡️"
            direction = "unchanged"
        
        lines.append(f"- **Overall change:** {emoji} {change:+.2f} ({change_pct:+.1f}%) - {direction}")
        lines.append("")
        
        # Improvements
        if comparison['improvements']:
            lines.append("## 🎉 Top Improvements")
            lines.append("")
            lines.append("| Page | Baseline | Current | Change |")
            lines.append("|------|----------|---------|--------|")
            for page, baseline, current, change in comparison['improvements'][:20]:
                lines.append(f"| `{page}` | {baseline:.2f} | {current:.2f} | +{change:.2f} |")
            lines.append("")
        
        # Regressions
        if comparison['regressions']:
            lines.append("## ⚠️ Regressions")
            lines.append("")
            lines.append("| Page | Baseline | Current | Change |")
            lines.append("|------|----------|---------|--------|")
            for page, baseline, current, change in comparison['regressions'][:20]:
                lines.append(f"| `{page}` | {baseline:.2f} | {current:.2f} | {change:.2f} |")
            lines.append("")
        
        # Metric changes
        lines.append("## 📊 Metric-by-Metric Changes")
        lines.append("")
        lines.append("| Metric | Baseline | Current | Change | % Change |")
        lines.append("|--------|----------|---------|--------|----------|")
        
        metric_names = {
            'title_tag': 'Title Tag',
            'content_depth': 'Content Depth',
            'heading_structure': 'Heading Structure',
            'internal_links': 'Internal Links',
            'meta_description': 'Meta Description',
            'url_quality': 'URL Quality',
            'freshness': 'Freshness',
            'direct_answer': 'Direct Answer',
            'structure': 'Structure',
            'semantic_clarity': 'Semantic Clarity',
            'code_examples': 'Code Examples',
            'prerequisites': 'Prerequisites',
            'step_format': 'Step Format',
            'version_info': 'Version Info'
        }
        
        for metric, data in sorted(comparison['metric_changes'].items(), 
                                   key=lambda x: abs(x[1]['change']), reverse=True):
            name = metric_names.get(metric, metric)
            baseline = data['baseline']
            current = data['current']
            change = data['change']
            change_pct = data['change_pct']
            
            if change > 0:
                emoji = "✅"
            elif change < 0:
                emoji = "❌"
            else:
                emoji = "➡️"
            
            lines.append(f"| {emoji} {name} | {baseline:.2f} | {current:.2f} | {change:+.2f} | {change_pct:+.1f}% |")
        
        lines.append("")
        
        # New pages
        if comparison['new_page_list']:
            lines.append("## ✨ New Pages Added")
            lines.append("")
            for page in comparison['new_page_list']:
                score = self.current_data[page]['overall_score']
                lines.append(f"- `{page}` (score: {score:.2f}/5.0)")
            lines.append("")
        
        # Removed pages
        if comparison['removed_page_list']:
            lines.append("## 🗑️ Pages Removed")
            lines.append("")
            for page in comparison['removed_page_list']:
                lines.append(f"- `{page}`")
            lines.append("")
        
        # Recommendations
        lines.append("## 💡 Recommendations")
        lines.append("")
        
        # Find biggest opportunities
        worst_metrics = sorted(comparison['metric_changes'].items(), 
                              key=lambda x: x[1]['current'])[:3]
        
        lines.append("Based on this comparison, focus on:")
        lines.append("")
        for metric, data in worst_metrics:
            name = metric_names.get(metric, metric)
            score = data['current']
            lines.append(f"- **{name}** (current avg: {score:.2f}/5.0)")
        
        lines.append("")
        
        if comparison['regressions']:
            lines.append(f"Also investigate the {len(comparison['regressions'])} pages that regressed since the baseline audit.")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("*Report generated by `compare_audits.py`*")
        
        report = "\n".join(lines)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Comparison report written to {output_file}")
        else:
            print(report)
        
        return report


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Compare two SEO/AEO audit results'
    )
    parser.add_argument(
        'baseline',
        help='Baseline audit CSV file'
    )
    parser.add_argument(
        'current',
        help='Current audit CSV file'
    )
    parser.add_argument(
        '--output',
        help='Output markdown report file (prints to stdout if not specified)'
    )
    
    args = parser.parse_args()
    
    # Create comparison
    comparator = AuditComparison(args.baseline, args.current)
    
    # Run comparison
    print("Loading audit files...")
    comparison = comparator.compare()
    
    print(f"Comparing {comparison['common_pages']} common pages...")
    print()
    
    # Generate report
    comparator.generate_report(comparison, args.output)


if __name__ == '__main__':
    main()
