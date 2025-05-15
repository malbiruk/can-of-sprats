#!/bin/bash

# Define output ports
LEFT_PORT="alsa_output.pci-0000_03_00.6.analog-stereo:playback_FL"
RIGHT_PORT="alsa_output.pci-0000_03_00.6.analog-stereo:playback_FR"

# Check if we're in disconnect mode
if [[ "$1" == "-d" ]]; then
    echo "Disconnecting SuperCollider outputs from system..."

    # Disconnect each SuperCollider stereo output pair from system playback
    for i in {0..11}; do
        # Calculate channel numbers (0-based)
        LEFT=$(($i*2+1))
        RIGHT=$(($i*2+2))

        # Disconnect from system playback
        pw-link -d "SuperCollider:out_$LEFT" "$LEFT_PORT" 2>/dev/null
        pw-link -d "SuperCollider:out_$RIGHT" "$RIGHT_PORT" 2>/dev/null

        echo "Disconnected SC outputs $LEFT/$RIGHT from system playback"
    done

    echo "All SuperCollider outputs disconnected from system playback"
else
    # Connect mode (original functionality)
    echo "Connecting SuperCollider outputs to system..."

    # Connect each SuperCollider stereo output pair to system playback
    for i in {0..11}; do
        # Calculate channel numbers (0-based)
        LEFT=$(($i*2+1))
        RIGHT=$(($i*2+2))

        # Connect to system playback
        pw-link "SuperCollider:out_$LEFT" "$LEFT_PORT" 2>/dev/null
        pw-link "SuperCollider:out_$RIGHT" "$RIGHT_PORT" 2>/dev/null

        echo "Connected SC outputs $LEFT/$RIGHT to system playback"
    done

    echo "All SuperCollider outputs connected to system playback"
fi
