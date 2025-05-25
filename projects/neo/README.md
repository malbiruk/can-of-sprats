# NEO

This is my attempt to recreate the beat from Platina's "NEO" using Sardine. The goal was to get as close as possible to the original, using code to capture that Matrix-inspired vibe.

[Listen to the original on Spotify](https://open.spotify.com/track/6QMdoaaVCEoolddEncgRvA?si=d4a53d58468643fe)

## The Idea

"NEO" is a complex track, and I wanted to see if I could break it down and rebuild it using live coding. It's a fun exercise in pattern composition, drum programming, and synth control. I chose Sardine because I wanted to explore algorithmic music creation with Python, and I ended up building my own tools ([My Sardine Tools](../../my_sardine_tools/README.md)) along the way to make it easier.

## Project Structure

```
neo/
├── README.md      # This file
├── neo.py         # Main composition script
├── sc_config.scd  # SuperCollider configuration
└── samples/       # Audio samples
    ├── crash/     # Crash cymbal samples
    ├── hh/        # Hi-hat samples
    └── sn/        # Snare samples
```

## Quick Start

1.  **Start Sardine:**

    You have a couple of options here. You can either use the `start_sardine.sh` script (which will directly run REPL in terminal) or run the Sardine as a server with `./run_sardine.sh`. Check the main [README](../../README.md) for more details on these options.

    With both scripts, make sure to use the project-specific SuperCollider config:

    ```bash
    cd ../../  # Return to sardine root
    ./scripts/start_sardine.sh -c ./projects/neo/sc_config.scd
    ```

2.  **Open `neo.py` in your favorite IDE / text editor**

3.  **Send Code to the REPL:**

    Sardine works by sending chunks of code from your editor to the REPL (the Sardine terminal). Experiment with sending different sections of the `neo.py` file to see how they sound.

4.  **Control the Flow:**

    Once the code is evaluated in REPL, you can use the `start()` and `stop()` functions to control the playback:

    ```python
    # Start everything
    start(all)

    # Just the melody
    start(melody)

    # Just the drums
    start(hhh)

    # Silence!
    stop(all)
    ```

## Key Elements

*   **Tempo:** 140 BPM
*   **Time Signature:** 4/4

Here's a quick overview of the main parts:

*   **Lead Synth (`lead`):**  The main melody.
*   **Bass (`bass`):**  The deep 808.
*   **Hi-hats (`hh`):**  The intricate hi-hat pattern.
*   **Snares:**  Two different snare patterns.
*   **Percussion:**  Crashes and tom fills.
*   **Reverb:**  Separate reverb playing on the same channel (orbit) as `lead` for space.

## State Management

I'm using the `State` class from [My Sardine Tools](../../my_sardine_tools/README.md) to keep things organized. It helps manage all the parameters for the synths and effects, and access them from the global state directly or via other `swim` functions.

## Requirements

*   Sardine with SuperCollider and SuperDirt
*   [My Sardine Tools](../../my_sardine_tools/README.md)
*   Audio samples (in `samples/`)
*   My custom tweak of `super808` in `../../common/synthdefs/super808.scd`

## Credits

Original song "NEO" by Platina.
