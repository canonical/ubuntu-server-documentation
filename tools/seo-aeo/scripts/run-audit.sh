#!/bin/bash
# Quick Start Script for SEO/AEO Audit
# Run this script to perform your first audit

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Ubuntu Server Documentation SEO/AEO Audit Tool   ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python3 --version

# Create audits directory if it doesn't exist
if [ ! -d "tools/seo-aeo/audits" ]; then
    echo -e "${YELLOW}Creating tools/seo-aeo/audits/ directory...${NC}"
    mkdir -p tools/seo-aeo/audits
fi

# Run the audit
echo -e "${GREEN}Running SEO/AEO audit...${NC}"
echo ""

TIMESTAMP=$(date +%Y-%m-%d)
OUTPUT_FILE="tools/seo-aeo/audits/audit-${TIMESTAMP}.csv"

python3 tools/seo-aeo/scripts/seo_aeo_analyzer.py --output "$OUTPUT_FILE"

echo ""
echo -e "${GREEN}✅ Audit complete!${NC}"
echo -e "${BLUE}Results saved to: ${OUTPUT_FILE}${NC}"
echo ""

# Check if this is the first audit
AUDIT_COUNT=$(ls -1 tools/seo-aeo/audits/*.csv 2>/dev/null | wc -l)

if [ "$AUDIT_COUNT" -eq 1 ]; then
    echo -e "${YELLOW}This is your first audit (baseline).${NC}"
    echo -e "Save this as your baseline for future comparisons:"
    echo -e "  ${BLUE}cp $OUTPUT_FILE tools/seo-aeo/audits/baseline.csv${NC}"
    echo ""
    echo -e "Next steps:"
    echo -e "  1. Review the summary above"
    echo -e "  2. Check $OUTPUT_FILE for detailed scores"
    echo -e "  3. Run this script again after making improvements"
elif [ "$AUDIT_COUNT" -gt 1 ]; then
    echo -e "${GREEN}Previous audits found!${NC}"
    echo -e "Run a comparison with:"
    echo -e "  ${BLUE}python3 tools/seo-aeo/scripts/compare_audits.py tools/seo-aeo/audits/baseline.csv $OUTPUT_FILE${NC}"
    echo ""
    
    # Ask if user wants to compare now
    read -p "Would you like to compare with the most recent audit now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        PREVIOUS_AUDIT=$(ls -t tools/seo-aeo/audits/*.csv | grep -v "$OUTPUT_FILE" | head -1)
        if [ -n "$PREVIOUS_AUDIT" ]; then
            echo -e "${YELLOW}Comparing with: $PREVIOUS_AUDIT${NC}"
            echo ""
            python3 tools/seo-aeo/scripts/compare_audits.py "$PREVIOUS_AUDIT" "$OUTPUT_FILE" --output "tools/seo-aeo/audits/report-${TIMESTAMP}.md"
            echo ""
            echo -e "${GREEN}✅ Comparison report saved to: tools/seo-aeo/audits/report-${TIMESTAMP}.md${NC}"
        fi
    fi
fi

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}All done! 🎉${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════${NC}"
