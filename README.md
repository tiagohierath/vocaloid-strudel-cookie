# Sophie Pallas

A local synth clicker game. Click Mimi to earn notes, buy instruments, and shape the music with the rack dials.

## One-click install

For a friend testing the game on Windows, download the latest **Sophie Pallas setup.exe** from [Releases](https://github.com/tiagohierath/vocaloid-strudel-cookie/releases), double-click it, and leave the default options selected. It installs a private runtime, creates a desktop shortcut, and opens the game immediately. No Python or terminal is needed.

The installed copy checks GitHub for new releases automatically when it opens, so the shortcut stays current.

## Run from the project folder

Requires **Python 3** and a modern browser. No package installation or internet connection is needed. After extracting the release archive, use the launcher for your operating system:

```sh
./run.sh
```

On Windows, double-click **`install.bat`** for a one-click local install. It uses Python if already installed, or downloads a private runtime if not. For developer use, double-click **`run.bat`**, or open Command Prompt in the folder and run:

```bat
run.bat
```

Open **http://localhost:5175**. Music starts automatically when the browser allows it; if autoplay is blocked, click or press a key anywhere on the page to start it.

You can also launch it from any directory using the full path to the launcher, for example:

```sh
/path/to/sophie-pallas/run.sh
```

```bat
C:\path\to\sophie-pallas\run.bat
```

Keep the terminal open while playing. Press **Ctrl+C** to stop; run the same command whenever you want to play again. Editing HTML, JavaScript, or CSS automatically reloads the page.

Your notes, owned synths, controls, drum pattern, modulation wires, tempo, and current mix are saved in this browser. Passive note income also accumulates for up to eight hours while the page is closed. Use **SAVE MIX** for an immediate save or **NEW MIX** to randomize the musical idea without losing your rack.

See [the running guide](docs/RUNNING.md) for controls and troubleshooting.
