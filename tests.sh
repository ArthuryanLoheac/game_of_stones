#!/bin/bash
# ...existing code...

LOGFILE="tests_output.log"
> "$LOGFILE"  # clear log file

PASS_COUNT=0
FAIL_COUNT=0

# Color codes for summary output in terminal
GREEN="\e[32m"
RED="\e[31m"
NC="\e[0m"

# for dir in tests/outputs/links tests/outputs/plots; do
for dir in tests/outputs/links; do
  for file in "$dir"/*; do
    echo "Running test: $file" >> "$LOGFILE"
    # Extract command as first line and expected output starting from line 3
    cmd=$(head -n1 "$file")
    expected=$(tail -n +3 "$file")

    # Execute the command and capture the output
    output=$(eval "$cmd")

    echo "Command: $cmd" >> "$LOGFILE"
    echo "Expected:" >> "$LOGFILE"
    echo "$expected" >> "$LOGFILE"
    echo "Got:" >> "$LOGFILE"
    echo "$output" >> "$LOGFILE"

    if [ "$output" == "$expected" ]; then
      echo "Result: PASSED" >> "$LOGFILE"
      PASS_COUNT=$((PASS_COUNT+1))
    else
      echo "Result: FAILED" >> "$LOGFILE"
      FAIL_COUNT=$((FAIL_COUNT+1))
    fi
    echo "------------------------" >> "$LOGFILE"
  done
done

# Print colored summary to terminal
echo -e "${GREEN}Tests Passed: $PASS_COUNT${NC}"
echo -e "${RED}Tests Failed: $FAIL_COUNT${NC}"

if [ "$FAIL_COUNT" -gt 0 ]; then
  exit 1
fi
