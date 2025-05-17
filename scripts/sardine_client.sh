#!/bin/bash
# This script sends text to the Sardine server via a named pipe.

PIPE_FILE="/tmp/sardine_pipe"

# Check if pipe exists
if [ ! -p "$PIPE_FILE" ]; then
    echo "Error: Sardine pipe not found. Please start the server first."
    exit 1
fi

# Get command from first argument
TEXT="$1"

# If we have text to send
if [ -n "$TEXT" ]; then
    # Remove empty lines from the text while preserving indentation
    # and add a single carriage return + newline at the end
    CLEANED_TEXT=$(echo "$TEXT" | sed '/^[[:space:]]*$/d')
    printf '%s\r\n' "$CLEANED_TEXT" > "$PIPE_FILE"

    # For debugging, show what we're sending (up to first 3 lines)
    echo "Sent to Sardine:"
    echo "$CLEANED_TEXT" | head -n 3 | sed 's/^/  /'
    if [ $(echo "$CLEANED_TEXT" | wc -l) -gt 3 ]; then
        echo "  ..."
    fi
    exit 0
else
    echo "No text to send."
    exit 1
fi
