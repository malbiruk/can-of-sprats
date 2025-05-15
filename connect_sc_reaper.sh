#!/bin/bash

# Wait for SuperCollider to fully start
sleep 5

# Connect each SuperCollider output to a REAPER input
for i in {1..12}; do
  # Calculate channel numbers (0-based)
  SC_OUT1=$((($i-1)*2))
  SC_OUT2=$((($i-1)*2+1))
  REAPER_IN1=$((($i-1)*2))
  REAPER_IN2=$((($i-1)*2+1))

  # Connect SuperCollider outputs to REAPER inputs
  pw-link "SuperCollider:out_$SC_OUT1" "REAPER:in_$REAPER_IN1"
  pw-link "SuperCollider:out_$SC_OUT2" "REAPER:in_$REAPER_IN2"

  echo "Connected SC outs $SC_OUT1/$SC_OUT2 to REAPER ins $REAPER_IN1/$REAPER_IN2"
done
