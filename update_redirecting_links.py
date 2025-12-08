#!/usr/bin/env python3
"""
Update redirecting links in documentation.

This script:
1. Runs `make linkcheck` to identify redirecting links
2. Parses the linkcheck output to extract redirect information
3. Updates the source files to use the final target URLs
4. Validates changes by running linkcheck again
5. Generates a report of changes made

Usage:
    python3 update_redirecting_links.py [--dry-run] [--verbose]
"""

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple


@dataclass
class Redirect:
    """Information about a redirecting link."""
    source_file: str
    line_number: int
    old_url: str
    new_url: str
    redirect_type: str  # 'permanently' or 'with Found'
    
    def __str__(self):
        return f"{self.source_file}:{self.line_number}: {self.old_url} -> {self.new_url}"


class LinkUpdater:
    """Update redirecting links in documentation files."""
    
    def __init__(self, docs_dir: Path, verbose: bool = False):
        self.docs_dir = docs_dir
        self.verbose = verbose
        self.redirects: List[Redirect] = []
        self.changes_made: List[Dict] = []
        self.skipped: List[Dict] = []
        
    def log(self, message: str, force: bool = False):
        """Log a message if verbose mode is enabled or force is True."""
        if self.verbose or force:
            print(message)
    
    def run_linkcheck(self) -> Tuple[int, str]:
        """
        Run make linkcheck and return the exit code and output.
        
        Returns:
            Tuple of (exit_code, output_text)
        """
        self.log("Running make linkcheck...", force=True)
        try:
            result = subprocess.run(
                ["make", "linkcheck"],
                cwd=self.docs_dir.parent,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            output = result.stdout + result.stderr
            return result.returncode, output
        except subprocess.TimeoutExpired:
            self.log("ERROR: linkcheck timed out after 10 minutes", force=True)
            return 1, ""
        except Exception as e:
            self.log(f"ERROR: Failed to run linkcheck: {e}", force=True)
            return 1, ""
    
    def parse_linkcheck_output(self, output: str) -> List[Redirect]:
        """
        Parse linkcheck output to extract redirect information.
        
        Expected format:
        (source_file: line XXX) redirect  old_url - permanently to new_url
        (source_file: line XXX) redirect  old_url - with Found to new_url
        
        Args:
            output: The linkcheck output text
            
        Returns:
            List of Redirect objects
        """
        redirects = []
        
        # Regex to match redirect lines
        # Format: (file: line NUM) redirect  URL - TYPE to TARGET_URL
        pattern = re.compile(
            r'\(([^:]+):\s+line\s+(\d+)\)\s+redirect\s+'  # File and line
            r'(https?://[^\s]+)\s+-\s+'  # Old URL
            r'(permanently|with Found)\s+to\s+'  # Redirect type
            r'(https?://[^\s]+)'  # New URL
        )
        
        for line in output.split('\n'):
            match = pattern.search(line)
            if match:
                source_file, line_num, old_url, redirect_type, new_url = match.groups()
                
                # Clean up the source file path
                # Remove 'docs/' prefix if present as we'll be working from docs/
                source_file = source_file.strip()
                if not source_file.endswith('.md') and not source_file.endswith('.rst'):
                    # Add extension if missing
                    if Path(self.docs_dir / f"{source_file}.md").exists():
                        source_file = f"{source_file}.md"
                    elif Path(self.docs_dir / f"{source_file}.rst").exists():
                        source_file = f"{source_file}.rst"
                
                redirects.append(Redirect(
                    source_file=source_file,
                    line_number=int(line_num),
                    old_url=old_url.rstrip(':'),
                    new_url=new_url.rstrip(':'),
                    redirect_type=redirect_type
                ))
                
                self.log(f"Found redirect: {redirects[-1]}")
        
        return redirects
    
    def get_file_path(self, source_file: str) -> Path:
        """
        Get the full path to a source file.
        
        Args:
            source_file: Relative path from docs/
            
        Returns:
            Full Path object
        """
        return self.docs_dir / source_file
    
    def update_url_in_file(self, redirect: Redirect, dry_run: bool = False) -> bool:
        """
        Update a URL in a file.
        
        This function is conservative:
        - Only updates if the old URL is found exactly
        - Preserves surrounding context
        - Validates the file exists and is readable
        
        Args:
            redirect: The Redirect object containing update information
            dry_run: If True, don't actually modify files
            
        Returns:
            True if update was successful or would be successful, False otherwise
        """
        file_path = self.get_file_path(redirect.source_file)
        
        if not file_path.exists():
            self.log(f"SKIP: File not found: {file_path}")
            self.skipped.append({
                'reason': 'file_not_found',
                'redirect': str(redirect)
            })
            return False
        
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Check if the old URL exists in the file
            if redirect.old_url not in content:
                self.log(f"SKIP: URL not found in {redirect.source_file}: {redirect.old_url}")
                self.skipped.append({
                    'reason': 'url_not_found',
                    'redirect': str(redirect)
                })
                return False
            
            # Replace all occurrences of the old URL with the new URL
            # Use exact string replacement to be safe
            updated_content = content.replace(redirect.old_url, redirect.new_url)
            
            # Verify we made changes
            if updated_content == content:
                self.log(f"SKIP: No changes made in {redirect.source_file}")
                self.skipped.append({
                    'reason': 'no_change',
                    'redirect': str(redirect)
                })
                return False
            
            # Count how many replacements were made
            num_replacements = content.count(redirect.old_url)
            
            if not dry_run:
                # Write the updated content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                self.log(
                    f"UPDATED: {redirect.source_file} - "
                    f"replaced {num_replacements} occurrence(s) of {redirect.old_url}",
                    force=True
                )
            else:
                self.log(
                    f"DRY-RUN: Would update {redirect.source_file} - "
                    f"would replace {num_replacements} occurrence(s) of {redirect.old_url}"
                )
            
            self.changes_made.append({
                'file': redirect.source_file,
                'line': redirect.line_number,
                'old_url': redirect.old_url,
                'new_url': redirect.new_url,
                'redirect_type': redirect.redirect_type,
                'num_replacements': num_replacements
            })
            
            return True
            
        except Exception as e:
            self.log(f"ERROR: Failed to update {file_path}: {e}", force=True)
            self.skipped.append({
                'reason': 'error',
                'redirect': str(redirect),
                'error': str(e)
            })
            return False
    
    def group_redirects_by_file(self) -> Dict[str, List[Redirect]]:
        """
        Group redirects by source file.
        
        Returns:
            Dictionary mapping file paths to lists of redirects
        """
        grouped = {}
        for redirect in self.redirects:
            if redirect.source_file not in grouped:
                grouped[redirect.source_file] = []
            grouped[redirect.source_file].append(redirect)
        return grouped
    
    def process_redirects(self, dry_run: bool = False) -> int:
        """
        Process all redirects and update files.
        
        Args:
            dry_run: If True, don't actually modify files
            
        Returns:
            Number of files successfully updated
        """
        if not self.redirects:
            self.log("No redirects to process.", force=True)
            return 0
        
        self.log(f"\nProcessing {len(self.redirects)} redirects...", force=True)
        
        # Group by file to show progress better
        grouped = self.group_redirects_by_file()
        self.log(f"Redirects found in {len(grouped)} files", force=True)
        
        success_count = 0
        for source_file, file_redirects in sorted(grouped.items()):
            self.log(f"\nProcessing {source_file} ({len(file_redirects)} redirects)...")
            
            for redirect in file_redirects:
                if self.update_url_in_file(redirect, dry_run):
                    success_count += 1
        
        return success_count
    
    def generate_report(self, initial_redirect_count: int) -> str:
        """
        Generate a summary report of changes.
        
        Args:
            initial_redirect_count: Number of redirects found initially
            
        Returns:
            Report as a string
        """
        report = []
        report.append("\n" + "="*70)
        report.append("REDIRECT UPDATE REPORT")
        report.append("="*70)
        report.append(f"\nInitial redirects found: {initial_redirect_count}")
        report.append(f"Changes made: {len(self.changes_made)}")
        report.append(f"Skipped: {len(self.skipped)}")
        
        if self.changes_made:
            report.append("\n" + "-"*70)
            report.append("CHANGES MADE:")
            report.append("-"*70)
            
            # Group by file
            by_file = {}
            for change in self.changes_made:
                file = change['file']
                if file not in by_file:
                    by_file[file] = []
                by_file[file].append(change)
            
            for file, changes in sorted(by_file.items()):
                report.append(f"\n{file}:")
                for change in changes:
                    report.append(f"  Line {change['line']}: {change['old_url']}")
                    report.append(f"    -> {change['new_url']}")
                    if change['num_replacements'] > 1:
                        report.append(f"    ({change['num_replacements']} occurrences replaced)")
        
        if self.skipped:
            report.append("\n" + "-"*70)
            report.append("SKIPPED:")
            report.append("-"*70)
            
            # Group by reason
            by_reason = {}
            for skip in self.skipped:
                reason = skip['reason']
                if reason not in by_reason:
                    by_reason[reason] = []
                by_reason[reason].append(skip)
            
            for reason, skips in sorted(by_reason.items()):
                report.append(f"\n{reason} ({len(skips)}):")
                for skip in skips[:10]:  # Limit to first 10 per reason
                    report.append(f"  {skip['redirect']}")
                if len(skips) > 10:
                    report.append(f"  ... and {len(skips) - 10} more")
        
        report.append("\n" + "="*70)
        
        return "\n".join(report)
    
    def run(self, dry_run: bool = False) -> int:
        """
        Main execution flow.
        
        Args:
            dry_run: If True, don't actually modify files
            
        Returns:
            Exit code (0 for success, 1 for failure)
        """
        # Run initial linkcheck
        self.log("="*70, force=True)
        self.log("STEP 1: Running initial linkcheck", force=True)
        self.log("="*70, force=True)
        
        exit_code, output = self.run_linkcheck()
        
        # Parse redirects (we expect linkcheck to exit with 2 if there are issues)
        self.log("\n" + "="*70, force=True)
        self.log("STEP 2: Parsing redirect information", force=True)
        self.log("="*70, force=True)
        
        self.redirects = self.parse_linkcheck_output(output)
        
        if not self.redirects:
            self.log("No redirects found. Nothing to do.", force=True)
            return 0
        
        self.log(f"Found {len(self.redirects)} redirecting links", force=True)
        
        # Process redirects
        self.log("\n" + "="*70, force=True)
        self.log(f"STEP 3: {'Simulating' if dry_run else 'Applying'} updates", force=True)
        self.log("="*70, force=True)
        
        success_count = self.process_redirects(dry_run)
        
        # Generate report
        report = self.generate_report(len(self.redirects))
        print(report)
        
        if not dry_run and self.changes_made:
            # Run validation linkcheck
            self.log("\n" + "="*70, force=True)
            self.log("STEP 4: Running validation linkcheck", force=True)
            self.log("="*70, force=True)
            
            exit_code, output = self.run_linkcheck()
            
            # Parse to see if redirects were reduced
            new_redirects = self.parse_linkcheck_output(output)
            self.log(f"\nValidation: {len(new_redirects)} redirects remain", force=True)
            
            if len(new_redirects) < len(self.redirects):
                self.log(
                    f"SUCCESS: Reduced redirects from {len(self.redirects)} "
                    f"to {len(new_redirects)}",
                    force=True
                )
            elif len(new_redirects) == len(self.redirects):
                self.log(
                    "WARNING: Redirect count unchanged. Manual review may be needed.",
                    force=True
                )
        
        # Save detailed report to file
        report_file = self.docs_dir.parent / 'redirect_update_report.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        self.log(f"\nDetailed report saved to: {report_file}", force=True)
        
        # Also save machine-readable JSON report
        json_report = {
            'initial_redirects': len(self.redirects),
            'changes_made': self.changes_made,
            'skipped': self.skipped
        }
        json_file = self.docs_dir.parent / 'redirect_update_report.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, indent=2)
        self.log(f"JSON report saved to: {json_file}", force=True)
        
        return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Update redirecting links in documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Perform a dry run to see what would be changed
  python3 update_redirecting_links.py --dry-run

  # Update links with verbose output
  python3 update_redirecting_links.py --verbose

  # Update links (default behavior)
  python3 update_redirecting_links.py
"""
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without modifying files'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--docs-dir',
        type=Path,
        default=None,
        help='Path to docs directory (default: ./docs)'
    )
    
    args = parser.parse_args()
    
    # Determine docs directory
    if args.docs_dir:
        docs_dir = args.docs_dir
    else:
        # Try to find docs directory
        script_dir = Path(__file__).parent
        docs_dir = script_dir / 'docs'
        
        if not docs_dir.exists():
            print(f"ERROR: docs directory not found at {docs_dir}", file=sys.stderr)
            print("Please run from repository root or use --docs-dir", file=sys.stderr)
            return 1
    
    if not docs_dir.is_dir():
        print(f"ERROR: {docs_dir} is not a directory", file=sys.stderr)
        return 1
    
    # Run the updater
    updater = LinkUpdater(docs_dir, verbose=args.verbose)
    return updater.run(dry_run=args.dry_run)


if __name__ == '__main__':
    sys.exit(main())
