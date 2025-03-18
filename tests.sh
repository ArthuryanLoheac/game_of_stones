#!/bin/bash

# Colors for better visibility in terminal
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters for passed and failed tests
PASSED=0
FAILED=0
TOTAL=0

function run_test() {
    local file="$1"
    local test_name=$(basename "$file")
    ((TOTAL++))
    
    echo -e "${YELLOW}Running test: ${test_name}${NC}"
    
    # Get the command from the first line of the file
    local cmd=$(head -n 1 "$file")
    
    # Get the expected output (lines 3 and beyond)
    local expected_output=$(tail -n +3 "$file")
    
    # Run the command and capture output
    local actual_output=$(eval "$cmd" 2>&1)
    
    # Compare outputs
    if [ "$actual_output" == "$expected_output" ]; then
        echo -e "${GREEN}✓ Test passed${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ Test failed${NC}"
        echo -e "${RED}Expected:${NC}"
        echo "$expected_output"
        echo -e "${RED}Got:${NC}"
        echo "$actual_output"
        ((FAILED++))
    fi
    echo ""
}

echo "Starting tests..."

# Run all tests in tests/outputs/plots/
echo "Testing plots scenarios:"
for plot_file in tests/outputs/plots/*.txt; do
    run_test "$plot_file"
done

# Run all tests in tests/outputs/links/
echo "Testing links scenarios:"
for link_file in tests/outputs/links/*.txt; do
    run_test "$link_file"
done

# Print summary
echo "Tests summary:"
echo -e "Total: $TOTAL"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"

# Exit with error if any test failed
if [ $FAILED -gt 0 ]; then
    exit 1
fi

exit 0
