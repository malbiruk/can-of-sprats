#!/bin/bash
# This script starts SuperCollider with SuperDirt and then runs Sardine.

DEBUG=0
CONFIG_FILE="/home/klim/Documents/REAPER Media/sardine/common/sc_config.scd"  # Default config path

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -d|--debug)
      DEBUG=1
      shift
      ;;
    -c|--config)
      if [[ -n "$2" && "$2" != -* ]]; then
        CONFIG_FILE="$2"
        shift 2
      else
        echo "Error: Argument for $1 is missing" >&2
        exit 1
      fi
      ;;
    *)
      # Unknown option
      echo "Unknown option: $1"
      echo "Usage: $0 [-d|--debug] [-c|--config PATH_TO_CONFIG]"
      exit 1
      ;;
  esac
done

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
  echo "Warning: Config file not found at $CONFIG_FILE"
  echo "Falling back to default SuperDirt config"
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
  if [ $DEBUG -eq 0 ]; then
    rm -f $TMP_SC_FILE
    rm -f $LOG_FILE
  else
    echo "Debug mode: Keeping temporary files:"
    echo "- SC file: $TMP_SC_FILE"
    echo "- Log file: $LOG_FILE"
  fi
  exit 0
}

# Set up traps for different signals
trap cleanup EXIT INT TERM

# Wait for SuperDirt to be ready
echo "Waiting for SuperDirt to start..."

MAX_WAIT=60  # Maximum wait time in seconds
WAIT_COUNTER=0
CHECK_INTERVAL=1  # Check every second

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
  echo "Check $LOG_FILE for any errors"
fi

# Now start Sardine
echo "Starting Sardine..."
sardine
