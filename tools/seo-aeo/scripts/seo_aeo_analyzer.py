#!/usr/bin/env python3
"""
SEO & AEO Documentation Analyzer
Analyzes Markdown documentation files for SEO and AEO compliance metrics.

Usage:
    python seo_aeo_analyzer.py [--output OUTPUT.csv] [--docs-dir DOCS_DIR]

Author: Ubuntu Server Documentation Team
Date: December 2025
"""

import os
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import csv
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class PageMetrics:
    """Data class to store all metrics for a documentation page."""
    file_path: str
    category: str
    title_tag: int
    content_depth: int
    heading_structure: int
    internal_links: int
    meta_description: int
    url_quality: int
    freshness: int
    direct_answer: int
    structure: int
    semantic_clarity: int
    code_examples: int
    prerequisites: int
    step_format: int
    version_info: int
    seo_score: float
    aeo_score: float
    overall_score: float
    notes: str


class DocumentationAnalyzer:
    """Analyzes documentation files for SEO and AEO metrics."""
    
    def __init__(self, docs_dir: str = "docs"):
        self.docs_dir = Path(docs_dir)
        self.ubuntu_versions = [
            "24.04", "24.10", "22.04", "20.04", 
            "Noble", "Jammy", "Focal"
        ]
        
    def find_content_files(self) -> List[Path]:
        """Find all Markdown content files, excluding index and contributing."""
        content_files = []
        
        # Target directories
        target_dirs = ["tutorial", "how-to", "explanation", "reference"]
        
        for target_dir in target_dirs:
            dir_path = self.docs_dir / target_dir
            if dir_path.exists():
                # Find all .md files recursively
                for md_file in dir_path.rglob("*.md"):
                    # Skip index files and contributing
                    if md_file.name != "index.md":
                        content_files.append(md_file)
        
        return sorted(content_files)
    
    def read_file_content(self, file_path: Path) -> str:
        """Read file content, handling encoding issues."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
    
    def get_category(self, file_path: Path) -> str:
        """Determine the category of the documentation page."""
        parts = file_path.relative_to(self.docs_dir).parts
        if len(parts) > 0:
            return parts[0]
        return "unknown"
    
    def extract_frontmatter(self, content: str) -> Dict[str, any]:
        """Extract YAML frontmatter from Markdown content."""
        frontmatter = {}
        
        # Match YAML frontmatter
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if fm_match:
            fm_content = fm_match.group(1)
            
            # Extract meta description
            desc_match = re.search(r'description:\s*["\']?([^"\n]+)["\']?', fm_content)
            if desc_match:
                frontmatter['description'] = desc_match.group(1).strip('"\'')
        
        return frontmatter
    
    def count_words(self, content: str) -> int:
        """Count words in content, excluding frontmatter and code blocks."""
        # Remove frontmatter
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
        
        # Remove code blocks
        content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        content = re.sub(r'`[^`]+`', '', content)
        
        # Remove markdown links but keep text
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
        
        # Count words
        words = re.findall(r'\b\w+\b', content)
        return len(words)
    
    def analyze_headings(self, content: str) -> Tuple[int, int]:
        """Analyze heading structure. Returns (h1_count, structure_score)."""
        # Remove frontmatter
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
        
        # Count H1 headings
        h1_matches = re.findall(r'^# [^\n]+', content, re.MULTILINE)
        h1_count = len(h1_matches)
        
        # Extract all headings with their levels
        headings = re.findall(r'^(#{1,6}) (.+)$', content, re.MULTILINE)
        
        if not headings:
            return h1_count, 2  # No headings is bad
        
        # Check for proper hierarchy
        levels = [len(h[0]) for h in headings]
        
        # Score based on structure quality
        score = 5
        
        # Penalize multiple H1s
        if h1_count > 1:
            score -= 1
        elif h1_count == 0:
            score -= 2
        
        # Check for skipped levels (e.g., H2 -> H4)
        for i in range(1, len(levels)):
            if levels[i] - levels[i-1] > 1:
                score -= 0.5
        
        # Check if headings are descriptive (more than 2 words)
        short_headings = sum(1 for h in headings if len(h[1].split()) < 3)
        if short_headings > len(headings) * 0.3:
            score -= 0.5
        
        return h1_count, max(1, min(5, int(score)))
    
    def count_internal_links(self, content: str) -> int:
        """Count internal cross-references (MyST refs and relative links)."""
        # MyST reference links: {ref}`label`
        myst_refs = len(re.findall(r'\{ref\}`[^`]+`', content))
        
        # Markdown relative links: [text](relative/path.md)
        relative_links = len(re.findall(r'\]\((?!http)[^\)]+\.md[^\)]*\)', content))
        
        # MyST term references: {term}`term`
        term_refs = len(re.findall(r'\{term\}`[^`]+`', content))
        
        return myst_refs + relative_links + term_refs
    
    def score_internal_links(self, link_count: int) -> int:
        """Score internal links (1-5 scale)."""
        if link_count == 0:
            return 1
        elif link_count <= 2:
            return 2
        elif link_count <= 5:
            return 3
        elif link_count <= 8:
            return 4
        else:
            return 5
    
    def has_version_info(self, content: str) -> bool:
        """Check if content mentions Ubuntu versions."""
        for version in self.ubuntu_versions:
            if version in content:
                return True
        return False
    
    def count_code_blocks(self, content: str) -> int:
        """Count code blocks in the content."""
        return len(re.findall(r'```', content)) // 2
    
    def has_prerequisites_section(self, content: str) -> bool:
        """Check if document has a prerequisites section."""
        return bool(re.search(r'^##+ Prerequisites?', content, re.MULTILINE | re.IGNORECASE))
    
    def count_numbered_steps(self, content: str) -> int:
        """Count numbered list items (procedural steps)."""
        # Match numbered lists: "1. ", "2. ", etc.
        return len(re.findall(r'^\d+\.\s', content, re.MULTILINE))
    
    def analyze_first_paragraph(self, content: str) -> str:
        """Extract first paragraph after frontmatter and heading."""
        # Remove frontmatter
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
        
        # Remove first heading
        content = re.sub(r'^#{1,6}[^\n]+\n+', '', content, flags=re.MULTILINE)
        
        # Get first paragraph
        paragraphs = re.split(r'\n\s*\n', content.strip())
        if paragraphs:
            return paragraphs[0][:200]  # First 200 chars
        return ""
    
    def count_list_items(self, content: str) -> int:
        """Count bullet and numbered list items."""
        bullets = len(re.findall(r'^\s*[-*+]\s', content, re.MULTILINE))
        numbered = len(re.findall(r'^\s*\d+\.\s', content, re.MULTILINE))
        return bullets + numbered
    
    def count_semantic_markup(self, content: str) -> int:
        """Count MyST semantic markup usage."""
        # {term}, {manpage}, {kbd}, etc.
        markup = len(re.findall(r'\{(term|manpage|kbd|command|guilabel)\}`[^`]+`', content))
        
        # Acronym expansions: "Word (ACRONYM)"
        acronyms = len(re.findall(r'\([A-Z]{2,}\)', content))
        
        return markup + acronyms
    
    def analyze_page(self, file_path: Path) -> PageMetrics:
        """Analyze a single documentation page for all metrics."""
        content = self.read_file_content(file_path)
        frontmatter = self.extract_frontmatter(content)
        category = self.get_category(file_path)
        
        # Calculate individual metrics
        word_count = self.count_words(content)
        h1_count, heading_score = self.analyze_headings(content)
        internal_link_count = self.count_internal_links(content)
        code_block_count = self.count_code_blocks(content)
        has_prereqs = self.has_prerequisites_section(content)
        numbered_steps = self.count_numbered_steps(content)
        has_version = self.has_version_info(content)
        first_para = self.analyze_first_paragraph(content)
        list_count = self.count_list_items(content)
        semantic_count = self.count_semantic_markup(content)
        
        # Score each metric (1-5 scale)
        
        # SEO Metrics
        # 1. Title Tag Quality (meta description)
        meta_desc = frontmatter.get('description', '')
        if meta_desc and 50 <= len(meta_desc) <= 160:
            title_score = 5
        elif meta_desc:
            title_score = 4
        else:
            title_score = 2
        
        # 2. Content Depth (word count)
        if word_count >= 800:
            depth_score = 5
        elif word_count >= 500:
            depth_score = 4
        elif word_count >= 300:
            depth_score = 3
        elif word_count >= 150:
            depth_score = 2
        else:
            depth_score = 1
        
        # 3. Heading Structure
        structure_score = heading_score
        
        # 4. Internal Links
        link_score = self.score_internal_links(internal_link_count)
        
        # 5. Meta Description
        meta_score = title_score  # Same as title tag
        
        # 6. URL Quality
        filename = file_path.stem
        # Good: descriptive, hyphenated, not too long
        if len(filename) <= 60 and '-' in filename and len(filename.split('-')) >= 2:
            url_score = 5
        elif len(filename) <= 80 and '-' in filename:
            url_score = 4
        elif len(filename) <= 100:
            url_score = 3
        else:
            url_score = 2
        
        # 7. Freshness (version info)
        if has_version and any(v in content for v in ["24.04", "24.10", "Noble"]):
            fresh_score = 4
        elif has_version:
            fresh_score = 3
        else:
            fresh_score = 2
        
        # AEO Metrics
        # 1. Direct Answer Quality
        if first_para and len(first_para) >= 100 and any(word in first_para.lower() for word in ['is', 'provides', 'allows', 'enables', 'describes']):
            answer_score = 5
        elif first_para and len(first_para) >= 50:
            answer_score = 4
        elif first_para:
            answer_score = 3
        else:
            answer_score = 2
        
        # 2. Structured Content (lists, code blocks)
        structure_elements = code_block_count + (list_count / 5)
        if structure_elements >= 10:
            struct_score = 5
        elif structure_elements >= 7:
            struct_score = 5
        elif structure_elements >= 5:
            struct_score = 4
        elif structure_elements >= 3:
            struct_score = 4
        elif structure_elements >= 1:
            struct_score = 3
        else:
            struct_score = 2
        
        # 3. Semantic Clarity
        semantic_density = semantic_count / max(1, word_count / 100)
        if semantic_density >= 3:
            semantic_score = 5
        elif semantic_density >= 2:
            semantic_score = 5
        elif semantic_density >= 1:
            semantic_score = 4
        elif semantic_density >= 0.5:
            semantic_score = 4
        else:
            semantic_score = 3
        
        # 4. Code Examples
        if code_block_count >= 5:
            code_score = 5
        elif code_block_count >= 3:
            code_score = 4
        elif code_block_count >= 2:
            code_score = 3
        elif code_block_count >= 1:
            code_score = 2
        else:
            code_score = 1
        
        # 5. Prerequisites
        if has_prereqs:
            if word_count >= 500:
                prereq_score = 5
            else:
                prereq_score = 4
        else:
            if category == "explanation":
                prereq_score = 3  # Not always needed
            else:
                prereq_score = 2
        
        # 6. Step Format (for how-to guides)
        if category == "how-to":
            if numbered_steps >= 10:
                step_score = 5
            elif numbered_steps >= 5:
                step_score = 4
            elif numbered_steps >= 3:
                step_score = 3
            else:
                step_score = 2
        else:
            # Not applicable for other types
            if numbered_steps >= 3:
                step_score = 4
            else:
                step_score = 3
        
        # 7. Version Specificity
        version_mentions = sum(1 for v in self.ubuntu_versions if v in content)
        if version_mentions >= 3 and "24.04" in content:
            version_score = 4
        elif version_mentions >= 2:
            version_score = 3
        elif version_mentions >= 1:
            version_score = 3
        else:
            version_score = 2
        
        # Calculate aggregate scores
        seo_metrics = [title_score, depth_score, structure_score, link_score, 
                       meta_score, url_score, fresh_score]
        aeo_metrics = [answer_score, struct_score, semantic_score, code_score,
                       prereq_score, step_score, version_score]
        
        seo_score = sum(seo_metrics) / len(seo_metrics)
        aeo_score = sum(aeo_metrics) / len(aeo_metrics)
        overall_score = (seo_score + aeo_score) / 2
        
        # Generate notes
        notes = []
        if h1_count > 1:
            notes.append(f"Multiple H1s ({h1_count})")
        if word_count < 300:
            notes.append(f"Short content ({word_count} words)")
        if internal_link_count == 0:
            notes.append("No internal links")
        if not has_prereqs and category == "how-to":
            notes.append("Missing prerequisites")
        if not has_version:
            notes.append("No version info")
        if code_block_count == 0 and category == "how-to":
            notes.append("No code examples")
        if code_block_count >= 5:
            notes.append("Excellent code examples")
        if word_count >= 1000:
            notes.append("Comprehensive content")
        if overall_score >= 4.5:
            notes.append("High quality page")
        
        notes_str = "; ".join(notes) if notes else "Good overall quality"
        
        # Build relative path
        rel_path = str(file_path.relative_to(self.docs_dir))
        
        return PageMetrics(
            file_path=rel_path,
            category=category,
            title_tag=title_score,
            content_depth=depth_score,
            heading_structure=structure_score,
            internal_links=link_score,
            meta_description=meta_score,
            url_quality=url_score,
            freshness=fresh_score,
            direct_answer=answer_score,
            structure=struct_score,
            semantic_clarity=semantic_score,
            code_examples=code_score,
            prerequisites=prereq_score,
            step_format=step_score,
            version_info=version_score,
            seo_score=round(seo_score, 2),
            aeo_score=round(aeo_score, 2),
            overall_score=round(overall_score, 2),
            notes=notes_str
        )
    
    def analyze_all(self) -> List[PageMetrics]:
        """Analyze all documentation files."""
        files = self.find_content_files()
        results = []
        
        print(f"Found {len(files)} content files to analyze...")
        
        for i, file_path in enumerate(files, 1):
            if i % 10 == 0:
                print(f"Analyzed {i}/{len(files)} files...")
            
            try:
                metrics = self.analyze_page(file_path)
                results.append(metrics)
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")
        
        print(f"Analysis complete! Analyzed {len(results)} files.")
        return results
    
    def write_csv(self, results: List[PageMetrics], output_file: str):
        """Write results to CSV file."""
        if not results:
            print("No results to write!")
            return
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            # Get field names from dataclass
            fieldnames = list(asdict(results[0]).keys())
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in results:
                writer.writerow(asdict(result))
        
        print(f"Results written to {output_file}")
    
    def print_summary(self, results: List[PageMetrics]):
        """Print summary statistics."""
        if not results:
            return
        
        print("\n" + "="*60)
        print("SEO & AEO AUDIT SUMMARY")
        print("="*60)
        print(f"Total pages analyzed: {len(results)}")
        print(f"Analysis date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Calculate averages
        avg_seo = sum(r.seo_score for r in results) / len(results)
        avg_aeo = sum(r.aeo_score for r in results) / len(results)
        avg_overall = sum(r.overall_score for r in results) / len(results)
        
        print(f"\nAverage SEO Score: {avg_seo:.2f}/5.0")
        print(f"Average AEO Score: {avg_aeo:.2f}/5.0")
        print(f"Average Overall Score: {avg_overall:.2f}/5.0")
        
        # Category breakdown
        print("\n" + "-"*60)
        print("SCORES BY CATEGORY")
        print("-"*60)
        categories = {}
        for result in results:
            if result.category not in categories:
                categories[result.category] = []
            categories[result.category].append(result.overall_score)
        
        for category, scores in sorted(categories.items()):
            avg_cat = sum(scores) / len(scores)
            print(f"{category:20s}: {avg_cat:.2f}/5.0 ({len(scores)} pages)")
        
        # Metric breakdown
        print("\n" + "-"*60)
        print("AVERAGE SCORES BY METRIC")
        print("-"*60)
        
        metrics = {
            'Title Tag': 'title_tag',
            'Content Depth': 'content_depth',
            'Heading Structure': 'heading_structure',
            'Internal Links': 'internal_links',
            'Meta Description': 'meta_description',
            'URL Quality': 'url_quality',
            'Freshness': 'freshness',
            'Direct Answer': 'direct_answer',
            'Structure': 'structure',
            'Semantic Clarity': 'semantic_clarity',
            'Code Examples': 'code_examples',
            'Prerequisites': 'prerequisites',
            'Step Format': 'step_format',
            'Version Info': 'version_info',
        }
        
        for name, attr in metrics.items():
            values = [getattr(r, attr) for r in results]
            avg = sum(values) / len(values)
            print(f"{name:20s}: {avg:.2f}/5.0")
        
        # Top and bottom performers
        print("\n" + "-"*60)
        print("TOP 5 PERFORMING PAGES")
        print("-"*60)
        top_5 = sorted(results, key=lambda x: x.overall_score, reverse=True)[:5]
        for result in top_5:
            print(f"{result.overall_score:.2f} - {result.file_path}")
        
        print("\n" + "-"*60)
        print("BOTTOM 5 PERFORMING PAGES")
        print("-"*60)
        bottom_5 = sorted(results, key=lambda x: x.overall_score)[:5]
        for result in bottom_5:
            print(f"{result.overall_score:.2f} - {result.file_path}")
        
        # Critical issues
        print("\n" + "-"*60)
        print("CRITICAL ISSUES FOUND")
        print("-"*60)
        
        no_links = sum(1 for r in results if r.internal_links == 1)
        print(f"Pages with no internal links: {no_links} ({no_links/len(results)*100:.1f}%)")
        
        short_pages = sum(1 for r in results if r.content_depth <= 2)
        print(f"Pages under 300 words: {short_pages} ({short_pages/len(results)*100:.1f}%)")
        
        no_prereqs = sum(1 for r in results if r.prerequisites <= 2 and r.category == "how-to")
        how_to_count = sum(1 for r in results if r.category == "how-to")
        if how_to_count > 0:
            print(f"How-to pages without prerequisites: {no_prereqs} ({no_prereqs/how_to_count*100:.1f}%)")
        
        no_version = sum(1 for r in results if r.version_info <= 2)
        print(f"Pages without version info: {no_version} ({no_version/len(results)*100:.1f}%)")
        
        print("\n" + "="*60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Analyze documentation for SEO and AEO compliance'
    )
    parser.add_argument(
        '--docs-dir',
        default='docs',
        help='Path to documentation directory (default: docs)'
    )
    parser.add_argument(
        '--output',
        default='seo-aeo-audit.csv',
        help='Output CSV file path (default: seo-aeo-audit.csv)'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress summary output'
    )
    
    args = parser.parse_args()
    
    # Create analyzer
    analyzer = DocumentationAnalyzer(args.docs_dir)
    
    # Run analysis
    results = analyzer.analyze_all()
    
    # Write results
    analyzer.write_csv(results, args.output)
    
    # Print summary
    if not args.quiet:
        analyzer.print_summary(results)


if __name__ == '__main__':
    main()
