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
    # First, remove all empty lines
    NO_EMPTIES=$(echo "$TEXT" | sed '/^[[:space:]]*$/d')

    # Now, use awk for more advanced pattern matching
    CLEANED_TEXT=$(echo "$NO_EMPTIES" | awk '
        # Store the previous line
        { prev_line = curr_line; curr_line = $0 }

        # At the beginning, no previous line
        NR == 1 { print; next }

        # Add blank line when:
        # 1. Previous line is indented (starts with whitespace)
        # 2. Current line is NOT indented (doesnt start with whitespace)
        # 3. Previous line doesnt end with ":" (not a function/class/if definition)
        prev_line ~ /^[[:space:]]/ &&
        $0 !~ /^[[:space:]]/ &&
        prev_line !~ /,$/ {
            print ""  # Add blank line
        }

        # Print the current line
        { print }
    ')

    printf '%s\r\n' "$CLEANED_TEXT" > "$PIPE_FILE"

    # For debugging, show what we're sending (up to first 3 lines)
    # echo "Sent to Sardine:"
    # echo "$CLEANED_TEXT" | sed 's/^/  /'
    fi
    exit 0
else
    echo "No text to send."
    exit 1
fi
