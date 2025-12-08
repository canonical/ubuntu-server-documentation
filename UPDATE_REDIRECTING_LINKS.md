# Update Redirecting Links

This script automatically updates redirecting links in the Ubuntu Server documentation by running `make linkcheck` and updating URLs that redirect to their final destinations.

## Purpose

Over time, web pages move and URLs change. When a URL redirects to a new location, it's better to update our documentation to point directly to the final URL. This improves:

- **Accuracy**: Documentation points to the current, stable URLs
- **Performance**: Eliminates unnecessary HTTP redirects
- **Reliability**: Reduces the chance of broken links if intermediate redirects change

## Usage

### Manual Execution

Run the script from the repository root:

```bash
# Preview changes without modifying files
python3 update_redirecting_links.py --dry-run

# Update links with verbose output
python3 update_redirecting_links.py --verbose

# Update links (default)
python3 update_redirecting_links.py
```

### Automated Execution

The script runs automatically via GitHub Actions every Monday at 9:00 AM UTC. The workflow:

1. Runs `make linkcheck` to identify redirecting links
2. Updates links that can be safely changed
3. Creates a PR with the changes
4. Includes detailed reports for review

You can also trigger the workflow manually from the GitHub Actions tab.

## How It Works

1. **Run linkcheck**: Executes `make linkcheck` to find all redirecting links
2. **Parse output**: Extracts redirect information (source file, line number, old URL, new URL)
3. **Update files**: Replaces old URLs with new ones in documentation files
4. **Validate**: Runs linkcheck again to verify improvements
5. **Report**: Generates human-readable and JSON reports

## Conservative Approach

The script prioritizes **accuracy over completeness**:

- Only updates URLs found exactly in files
- Skips ambiguous cases rather than risking broken links
- Preserves all surrounding context and formatting
- Validates changes by running linkcheck again

## Reports

Two reports are generated:

### `redirect_update_report.txt`

Human-readable summary showing:
- Number of redirects found and updated
- Detailed list of changes by file
- Skipped items with reasons

### `redirect_update_report.json`

Machine-readable data containing:
- Initial redirect count
- Detailed change information
- Skipped items with categorization

## Command-Line Options

```
usage: update_redirecting_links.py [-h] [--dry-run] [--verbose] [--docs-dir DOCS_DIR]

Update redirecting links in documentation

options:
  -h, --help           show this help message and exit
  --dry-run            Show what would be changed without modifying files
  --verbose, -v        Enable verbose output
  --docs-dir DOCS_DIR  Path to docs directory (default: ./docs)
```

## GitHub Actions Workflow

The workflow is defined in `.github/workflows/update-redirecting-links.yml`:

- **Schedule**: Runs every Monday at 9:00 AM UTC
- **Manual trigger**: Can be run on-demand via `workflow_dispatch`
- **PR creation**: Automatically creates a PR with changes
- **Labels**: Tags PRs as `automated`, `documentation`, and `maintenance`

### Reviewing PRs

When reviewing automated PRs:

1. Check the `redirect_update_report.txt` in the PR
2. Verify redirect targets are appropriate
3. Ensure no broken links were introduced
4. Run `make linkcheck` locally if needed
5. Merge when satisfied with the changes

## Skipped Links

Links may be skipped for several reasons:

- **file_not_found**: Source file doesn't exist (rare)
- **url_not_found**: Old URL not found in file (URL may have different format)
- **no_change**: Replacement didn't change content
- **error**: Unexpected error during processing

These are logged in the report and can be reviewed manually if needed.

## Dependencies

The script requires:

- Python 3.10+
- Standard library modules (argparse, json, re, subprocess, pathlib)
- `make` and Sphinx environment (for linkcheck)

## Contributing

If you encounter issues or have suggestions:

1. Check the reports for details about what was skipped
2. Open an issue with the specific redirect case
3. Consider edge cases when proposing changes

## Maintenance

The script is designed to be low-maintenance:

- No external Python dependencies beyond standard library
- Works with existing `make linkcheck` infrastructure
- Generates detailed logs for troubleshooting
- Runs automatically without intervention

## Examples

### Successful Update

```
UPDATED: how-to/networking/install-dns.md - replaced 1 occurrence(s) of 
http://shop.oreilly.com/product/9780596100575.do
→ https://www.oreilly.com/library/view/dns-and-bind/0596100574/
```

### Skipped (URL not found)

```
SKIP: URL not found in how-to/software/snapshot-service.md: 
http://docker.io
(The page may reference this URL in a different format)
```

## Workflow Integration

This script integrates with the Ubuntu Server documentation workflow:

1. **Weekly automation**: Keeps links up-to-date automatically
2. **Human review**: All changes reviewed before merging
3. **Documentation**: Changes tracked in git history
4. **Quality**: Validation ensures no regressions

## License

Part of the Ubuntu Server Documentation project. See repository LICENSE for details.
