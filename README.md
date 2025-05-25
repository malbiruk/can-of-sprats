# can of sprats

Yo! Welcome to my can of sprats! This is where I mess around with [Sardine](https://github.com/Bubobubobubobubo/sardine), a cool Python library for making algorithmic music and live coding.

**Why "can of sprats"?** Think of it as a collection of things packed tightly together – Sardine code, custom tools, experiments, and musical sketches, all swimming in their own little brine.

## What's Inside?

*   **Projects:** These are actual musical pieces or recreations. Right now, there's a recreation of Platina's "NEO" beat. Check it out: [NEO Beat Recreation](./projects/neo/README.md)
*   **My Sardine Tools:** A custom Python package with utilities to make Sardine even more fun. Think of it as my personal toolbox. More details here: [My Sardine Tools](./my_sardine_tools/README.md)
*   **Scripts:** Little helpers for setting things up and connecting stuff.
*   **Common:** Shared resources and configurations.

## Getting Started

Wanna dive in? Here's the basic flow:

1.  **Dependencies:** Make sure you have everything installed. [Install Sardine](https://sardine.raphaelforment.fr/installation.html), then do this:
    ```bash
    pip install -r requirements.txt
    pip install -e ./my_sardine_tools
    ```
2.  **Start Sardine:** Use the script to get SuperCollider and Sardine running smoothly:
    ```bash
    ./scripts/start_sardine.sh
    ```
    (This script makes sure SuperCollider and SuperDirt are up and running before Sardine starts. In some cases Sardine doesn't do it automatically, otherwise just running `sardine` might work.)

3.  **Load a Project:** Sardine works as a REPL. You edit code in your editor and send it to the REPL.

    *   **Option 1: Direct Terminal:** If your editor can send text to the terminal, just run `./scripts/start_sardine.sh` in terminal and send the selected code there from editor pane.
    *   **Option 2: Client/Server:** If your editor can't send text to the terminal, use the client/server approach:
        *   Start the Sardine server: `./run_sardine.sh`
        *   Configure your editor to send selected text via the client script: `./scripts/sardine_client.sh "YOUR_SELECTED_CODE"`
    *   **Option 3: Editor extension:** For some editors extensions are available, check [here](https://sardine.raphaelforment.fr/editors.html).

## License

This is all for fun and learning. Do what you want with it.
