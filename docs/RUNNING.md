# Running Sophie Pallas

## One-click Windows install

Download the latest setup executable from the [GitHub Releases page](https://github.com/tiagohierath/vocaloid-strudel-cookie/releases), double-click it, and keep the default choices. It installs Sophie Pallas, creates a desktop shortcut, and opens the game. The installed launcher checks for updates automatically.

If you are testing from a source folder instead, double-click `install.bat`. It can download a private Python runtime, so Python does not need to be installed first.

## Start whenever you want

On Linux or macOS, open a terminal in the extracted project folder and run:

```sh
./run.sh
```

On Windows, double-click `run.bat`, or run this from Command Prompt:

```bat
run.bat
```

Open **http://localhost:5175** in your browser. Music starts automatically when the browser allows it; if autoplay is blocked, click or press a key anywhere on the page to start it. The game and its assets are local and can run offline.

The folder still has its original name, `vocaloid-strudel-cookie`. The game's current name is **Sophie Pallas**.

## Stop and reopen

Keep the terminal running during a session. Press **Ctrl+C** in that terminal to stop the server. To reopen the game, run the same command and open the URL again.

Progress is saved in this browser using local storage: refreshing or closing the page keeps the session. Passive note income is credited for up to eight hours while the page is closed. Automatic reload after a source edit also restores the session. Use **SAVE MIX** to write immediately, or **NEW MIX** to generate a new musical idea while keeping the rack and notes.

## Controls

- Click Mimi to earn notes and buy synths in the market.
- Drag a dial upward or downward: eight pixels changes one unit. The value stays put when you release it.
- Click a dial to add one unit, or focus it and use arrow keys. Home and End select its minimum and maximum.
- Music starts automatically and keeps playing while the page is open. Browsers that block autoplay start it after your first click or key press.
- MUTE silences a synth; ARCHIVE removes it from the active rack. RESTORE brings it back.

## If the address is busy

If Sophie Pallas is already running, open **http://localhost:5175**. Otherwise stop the previous server in its terminal, or choose another port:

```sh
./run.sh --port 5176
```

On Windows:

```bat
run.bat --port 5176
```

Then open **http://localhost:5176**.

## Requirements and editing

Only Python 3 and a modern browser are required. On Windows, install Python 3 from [python.org](https://www.python.org/downloads/windows/) and make sure the `py` launcher is available. On Linux or macOS, install Python 3 through the operating system's package manager if `python3` is missing.

The launcher serves files from the project folder regardless of the terminal's current directory. The server checks for edits to local HTML, JavaScript, and CSS files and automatically reloads connected pages. After switching from the old server, refresh an already open tab once to load this behavior.

## How the loop fits together

Each new session starts with a coherent four-bar idea: sunlit pop, dream house, a late-night groove, or broken beats. Its key, scale, chord progression, groove, and starting tempo are chosen together. The current key and chords are shown above the tempo dial. Tempo is in quarter-note BPM and the meter is 4/4. Bass follows the chord roots; leads and plucks use chord tones; pads, organ, and voice play chords. Sequencer voices share one eight-step pattern, with one eighth note per step. Existing synths bring different rhythms and registers; melodies vary gently between phrases. Levels are balanced automatically as the rack grows.

Each instrument has the same five controls: cutoff in Hz, resonance, attack and release in milliseconds, and level in dB. Filter and level changes apply to that instrument immediately; envelope changes shape its next note. Changing a sound does not change its tuning.

The WAV button bounces three minutes of the current loop from bar one, using the same instruments, knob settings, mutes, tempo, and step pattern as playback. Muting changes the music; archiving also removes that instrument's note income.
