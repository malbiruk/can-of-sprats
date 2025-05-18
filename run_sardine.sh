#!/bin/bash
# This script serves as sardine client, running start_sardine.sh in a pipe.

# Set up the named pipe
PIPE_FILE="/tmp/sardine_pipe"

# Clean up previous pipe if it exists
rm -f "$PIPE_FILE"
mkfifo "$PIPE_FILE"

echo "Starting Sardine with input pipe..."

# More robust handling of the pipe
tail -f "$PIPE_FILE" | scripts/start_sardine.sh "$@"

# Clean up on exit
trap "rm -f $PIPE_FILE" EXIT
