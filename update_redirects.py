#!/usr/bin/env python3
"""
Autonomous Redirect Link Remediation Script
Processes linkcheck output to update redirected URLs in Markdown files
Uses only standard Python libraries
"""

import re
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set


class RedirectUpdater:
    """Handles parsing linkcheck output and updating redirected URLs in Markdown files"""
    
    def __init__(self, docs_dir: str = "docs"):
        self.docs_dir = Path(docs_dir)
        self.broken_urls: Set[str] = set()
        self.redirects: List[Dict[str, str]] = []
        self.updates_by_file: Dict[str, List[Tuple[str, str]]] = {}
        self.successful_updates: List[Dict[str, str]] = []
        self.skipped_updates: List[Dict[str, str]] = []
        
    def parse_linkcheck_output(self, linkcheck_file: str) -> None:
        """
        Parse the linkcheck output file to extract broken URLs and redirects
        
        Args:
            linkcheck_file: Path to the linkcheck output file
        """
        print(f"Parsing {linkcheck_file}...")
        
        with open(linkcheck_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # First pass: collect all broken URLs
        broken_pattern = r'\[broken\]\s+([^\s:]+)'
        for match in re.finditer(broken_pattern, content):
            broken_url = match.group(1)
            self.broken_urls.add(broken_url)
        
        print(f"Found {len(self.broken_urls)} broken URLs")
        
        # Second pass: collect redirects from _build/output.txt
        output_file = self.docs_dir / "_build" / "output.txt"
        if output_file.exists():
            with open(output_file, 'r', encoding='utf-8', errors='ignore') as f:
                output_content = f.read()
            
            # Pattern: filename.md:LINE: [redirected ...] FROM_URL to TO_URL
            redirect_pattern = r'([^\s:]+\.md):\d+:\s+\[redirected[^\]]*\]\s+([^\s]+)\s+to\s+([^\s]+)'
            
            for match in re.finditer(redirect_pattern, output_content):
                file_path = match.group(1)
                from_url = match.group(2)
                to_url = match.group(3)
                
                # Safety check: skip if target URL is broken
                if to_url in self.broken_urls:
                    self.skipped_updates.append({
                        'file': file_path,
                        'from_url': from_url,
                        'to_url': to_url,
                        'reason': 'Target URL is broken'
                    })
                    continue
                
                # Store the redirect
                self.redirects.append({
                    'file': file_path,
                    'from_url': from_url,
                    'to_url': to_url
                })
                
                # Organize by file
                if file_path not in self.updates_by_file:
                    self.updates_by_file[file_path] = []
                self.updates_by_file[file_path].append((from_url, to_url))
        
        print(f"Found {len(self.redirects)} valid redirects to process")
        print(f"Skipped {len(self.skipped_updates)} redirects (target URL is broken)")
    
    def update_markdown_files(self) -> None:
        """
        Update all Markdown files with redirect URL replacements
        """
        print("\nUpdating Markdown files...")
        
        for file_path, updates in self.updates_by_file.items():
            full_path = self.docs_dir / file_path
            
            if not full_path.exists():
                print(f"  Warning: File not found: {full_path}")
                continue
            
            # Read the file
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                changes_made = []
                
                # Apply all updates for this file
                for from_url, to_url in updates:
                    if from_url in content:
                        # Count occurrences
                        count = content.count(from_url)
                        content = content.replace(from_url, to_url)
                        changes_made.append({
                            'from_url': from_url,
                            'to_url': to_url,
                            'occurrences': count
                        })
                        print(f"  {file_path}: {from_url} -> {to_url} ({count} occurrence(s))")
                
                # Write back if changes were made
                if content != original_content:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    # Record successful updates
                    for change in changes_made:
                        self.successful_updates.append({
                            'file': file_path,
                            'from_url': change['from_url'],
                            'to_url': change['to_url'],
                            'occurrences': change['occurrences']
                        })
            
            except Exception as e:
                print(f"  Error processing {full_path}: {e}")
        
        print(f"\nSuccessfully updated {len(self.successful_updates)} redirects across {len(self.updates_by_file)} files")
    
    def save_summary(self, output_file: str = "redirect_changes_summary.json") -> None:
        """
        Save a summary of all changes to a JSON file
        
        Args:
            output_file: Path to the output JSON file
        """
        summary = {
            'total_redirects_found': len(self.redirects),
            'successful_updates': self.successful_updates,
            'skipped_updates': self.skipped_updates,
            'broken_urls_count': len(self.broken_urls)
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\nSummary saved to {output_file}")
    
    def verify_updates(self, validation_file: str) -> Tuple[bool, List[str]]:
        """
        Verify that updated URLs are not broken in the validation linkcheck
        
        Args:
            validation_file: Path to the validation linkcheck output file
            
        Returns:
            Tuple of (success, list of new broken URLs)
        """
        print(f"\nVerifying updates using {validation_file}...")
        
        new_broken_urls = []
        
        # Check if validation file exists
        if not os.path.exists(validation_file):
            print(f"  Warning: Validation file not found: {validation_file}")
            return False, []
        
        # Read validation output
        output_file = self.docs_dir / "_build" / "output.txt"
        if output_file.exists():
            with open(output_file, 'r', encoding='utf-8', errors='ignore') as f:
                validation_content = f.read()
            
            # Check if any of our updated target URLs are now broken
            broken_pattern = r'\[broken\]\s+([^\s:]+)'
            validation_broken = set()
            for match in re.finditer(broken_pattern, validation_content):
                validation_broken.add(match.group(1))
            
            # Check if any of our to_urls are now broken
            for update in self.successful_updates:
                if update['to_url'] in validation_broken:
                    new_broken_urls.append(update['to_url'])
        
        if new_broken_urls:
            print(f"  FAILED: {len(new_broken_urls)} updated URLs are now broken!")
            for url in new_broken_urls:
                print(f"    - {url}")
            return False, new_broken_urls
        else:
            print(f"  PASSED: All {len(self.successful_updates)} updated URLs are valid!")
            return True, []


def main():
    """Main execution function"""
    print("=" * 80)
    print("Autonomous Redirect Link Remediation")
    print("=" * 80)
    
    # Initialize updater
    updater = RedirectUpdater(docs_dir="docs")
    
    # Step 1: Parse the initial linkcheck output
    linkcheck_file = "docs/linkcheck.txt"
    if not os.path.exists(linkcheck_file):
        print(f"Error: {linkcheck_file} not found!")
        print("Please run: make linkcheck > linkcheck.txt")
        return 1
    
    updater.parse_linkcheck_output(linkcheck_file)
    
    if not updater.redirects:
        print("\nNo redirects found to process.")
        return 0
    
    # Step 2: Update Markdown files
    updater.update_markdown_files()
    
    # Step 3: Save summary
    updater.save_summary("redirect_changes_summary.json")
    
    # Step 4: Run validation linkcheck
    print("\n" + "=" * 80)
    print("Running validation linkcheck...")
    print("=" * 80)
    os.system("cd docs && make linkcheck > linkcheck_validation.txt 2>&1")
    
    # Step 5: Verify updates
    validation_passed, new_broken = updater.verify_updates("docs/linkcheck_validation.txt")
    
    # Step 6: Generate final report
    print("\n" + "=" * 80)
    print("Generating final report...")
    print("=" * 80)
    
    with open("redirect_update_report.md", 'w', encoding='utf-8') as f:
        f.write("# Redirect Update Report\n\n")
        f.write(f"**Date:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Summary\n\n")
        f.write(f"- **Total redirects found:** {len(updater.redirects)}\n")
        f.write(f"- **Redirects successfully updated:** {len(updater.successful_updates)}\n")
        f.write(f"- **Redirects skipped (target was broken):** {len(updater.skipped_updates)}\n")
        f.write(f"- **Validation status:** {'✅ PASSED' if validation_passed else '❌ FAILED'}\n\n")
        
        if new_broken:
            f.write("## Validation Issues\n\n")
            f.write("The following updated URLs are now broken:\n\n")
            for url in new_broken:
                f.write(f"- {url}\n")
            f.write("\n")
        
        f.write("## Detailed Changes\n\n")
        f.write("```json\n")
        with open("redirect_changes_summary.json", 'r') as summary_file:
            f.write(summary_file.read())
        f.write("\n```\n")
    
    print(f"\nFinal report saved to redirect_update_report.md")
    
    # Step 7: Cleanup temporary files
    print("\nCleaning up temporary files...")
    try:
        if os.path.exists("docs/linkcheck.txt"):
            os.remove("docs/linkcheck.txt")
            print("  Removed docs/linkcheck.txt")
        if os.path.exists("docs/linkcheck_validation.txt"):
            os.remove("docs/linkcheck_validation.txt")
            print("  Removed docs/linkcheck_validation.txt")
    except Exception as e:
        print(f"  Warning: Could not remove temporary files: {e}")
    
    print("\n" + "=" * 80)
    print(f"Process completed: {'SUCCESS' if validation_passed else 'FAILED'}")
    print("=" * 80)
    
    return 0 if validation_passed else 1


if __name__ == "__main__":
    exit(main())
