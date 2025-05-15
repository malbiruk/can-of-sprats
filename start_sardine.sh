#!/bin/bash

DEBUG=0
if [[ "$1" == "-d" ]] || [[ "$1" == "--debug" ]]; then
  DEBUG=1
  shift # Remove the flag from arguments
fi

source .venv/bin/activate

# Create a temporary SuperCollider file
TMP_SC_FILE=$(mktemp /tmp/sardine-boot.XXXXXX.scd)

# Create log file - either temporary or in current directory for debug
if [ $DEBUG -eq 1 ]; then
  LOG_FILE="./superdirt_startup.log"
  echo "Debug mode: SC log will be saved to $LOG_FILE"
else
  LOG_FILE=$(mktemp /tmp/sardine-sc-log.XXXXXX.log)
fi

CONFIG_FILE="/home/klim/Documents/REAPER Media/sardine/sc_config.scd"

# Check if the config file exists
if [ -f "$CONFIG_FILE" ]; then
  echo "Using SuperDirt config from: $CONFIG_FILE"
  # Simply load your config file instead of using SuperDirt.start
  cat > $TMP_SC_FILE << EOF
// Load the custom SuperDirt config
(
var file = "$CONFIG_FILE";
if(File.exists(file)) {
  file.load;
} {
  "Config file not found, falling back to default".postln;
  SuperDirt.start;
};
)
EOF
else
  echo "Custom config not found, using default SuperDirt config"
  # Fall back to the default startup
  cat > $TMP_SC_FILE << 'EOF'
SuperDirt.start;
EOF
fi

echo "Starting SuperCollider with SuperDirt..."
# Start SuperCollider with the temp file in the background, redirecting output to log file
sclang $TMP_SC_FILE > $LOG_FILE 2>&1 &
SC_PID=$!

# Trap to ensure cleanup on exit, interrupt, or termination
cleanup() {
  # Kill SuperCollider more thoroughly
  if ps -p $SC_PID > /dev/null; then
    echo "Stopping SuperCollider..."
    kill -TERM $SC_PID
    sleep 1
    # If it's still running, force kill
    if ps -p $SC_PID > /dev/null; then
      kill -9 $SC_PID
    fi
  fi

  # Also look for any stray sclang or scsynth processes
  pkill -f sclang
  pkill -f scsynth

  # Remove the temp files
  rm -f $TMP_SC_FILE
  rm -f $LOG_FILE
  exit 0
}

# Set up traps for different signals
trap cleanup EXIT INT TERM

# Wait for SuperDirt to be ready
echo "Waiting for SuperDirt to start..."

MAX_WAIT=120  # Maximum wait time in seconds (doubled to 120)
WAIT_COUNTER=0
CHECK_INTERVAL=1  # Check every second (integer value)

while [ $WAIT_COUNTER -lt $MAX_WAIT ]; do
  if grep -q "SuperDirt: listening on port 57120" $LOG_FILE; then
    echo "SuperDirt is ready!"
    break
  fi

  # Show a spinner to indicate we're waiting
  printf "."
  sleep $CHECK_INTERVAL
  WAIT_COUNTER=$((WAIT_COUNTER + 1))
done

echo ""  # New line after dots

if [ $WAIT_COUNTER -ge $MAX_WAIT ]; then
  echo "Warning: Timeout waiting for SuperDirt to start. Continuing anyway..."
fi

# Connect SuperCollider outputs to system outputs
./connect_sc_system.sh

# Now start Sardine
echo "Starting Sardine..."
sardine
