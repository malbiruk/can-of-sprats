#!/bin/bash

source .venv/bin/activate

# Create a temporary SuperCollider file
TMP_SC_FILE=$(mktemp /tmp/sardine-boot.XXXXXX.scd)

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
# Start SuperCollider with the temp file in the background
sclang $TMP_SC_FILE &
SC_PID=$!

# Trap to ensure cleanup on exit, interrupt, or termination
cleanup() {\
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

    # Remove the temp file
    rm -f $TMP_SC_FILE\
    exit 0
}

# Set up traps for different signals
trap cleanup EXIT INT TERM

# Give SuperCollider time to boot and start SuperDirt
echo "Waiting for SuperDirt to start..."
sleep 7  # Increased sleep time to ensure everything is ready

# Connect SuperCollider outputs to system outputs
./connect_sc_system.sh

# Now start Sardine
echo "Starting Sardine..."
sardine
