# Claude Code on the Adastra login nodes

The login nodes kill any process that has used more than 15 minutes of CPU time (user + system).
The limit is per process: CPU used by child processes is not added to the parent's. A long
[Claude Code](https://claude.com/claude-code) session eventually hits it and gets killed, often in the
middle of a step.

These two scripts keep one conversation going across those kills. They also let Claude restart itself
cleanly at 14 minutes of CPU, before the watchdog kills it at 15.

| File | What it does |
| --- | --- |
| [`claude-loop.sh`](claude-loop.sh) | Runs `claude` in a loop and resumes the same session ID, with Remote Control on, after each exit. After a kill, it starts the resumed session with a prompt telling Claude to re-arm the watch and carry on. Each run is logged to `~/.claude/claude-loop.log`. The loop stops after 5 runs in a row that each last less than 30 s. |
| [`claude-cpu-watch.sh`](claude-cpu-watch.sh) | Claude runs this as a background Bash task. It finds the `claude` process it runs under, checks that process's CPU time every 5 s, and exits with one line once it reaches 840 s. Claude is notified when the task exits. It then stops whatever can't survive a restart and sends itself a delayed `SIGTERM`. |

## Setup

1. Install both scripts in `~/.local/bin`, so you can run them from any project directory. Keep them
   together: `claude-loop.sh` looks for `claude-cpu-watch.sh` in its own directory.

   ```bash
   mkdir -p ~/.local/bin
   install -m 755 claude-code/claude-loop.sh claude-code/claude-cpu-watch.sh ~/.local/bin/
   ```

   `~/.local/bin` is usually on your `PATH` already. If `command -v claude-loop.sh` prints nothing, add
   `export PATH="$HOME/.local/bin:$PATH"` to `~/.bashrc`.
2. Start the loop inside tmux, so it survives SSH disconnects, from the directory Claude should work in:

   ```bash
   tmux new -s claude
   cd <your project>
   claude-loop.sh --permission-mode auto     # any extra arguments are passed to claude
   ```

   To resume an existing conversation: `CLAUDE_LOOP_SESSION=<session uuid> ./claude-loop.sh`.
3. Tell Claude about the watchdog, for example in the project's `CLAUDE.md` or in `~/.claude/CLAUDE.md`:

   ```markdown
   ## CPU-time watchdog
   This session runs under claude-loop.sh on a login node that kills any process after 15 min of CPU time.
   - At session start, check whether claude-cpu-watch.sh is already running under your claude process. If it
     isn't, start `~/.local/bin/claude-cpu-watch.sh 840 5` with Bash `run_in_background`.
   - When it reports "CPU LIMIT NEAR", stop the background shells and Monitors that can't be resumed. Work
     started with setsid/nohup and Slurm jobs can keep running. Then run the `setsid nohup ... kill -TERM <pid>`
     command it prints and end your turn with one line.
   ```

   After a restart, the loop's prompt tells Claude to re-arm the watch, so this snippet matters mostly for
   the first start.

## How a restart goes

1. The watch reaches 840 s of CPU and exits. Claude receives the notification.
2. Claude stops its background shells and Monitors. It then starts a detached `sleep 5; kill -TERM <claude pid>`
   and ends its turn, so the turn is saved before the process exits.
3. `claude-loop.sh` sees the `SIGTERM` and waits 5 s. During that pause, Enter restarts right away and `q`
   quits. It then runs `claude --resume <id> "<continue prompt>"`.
4. Claude re-arms the watch and continues the task it was on. If no task was in progress, it replies in one line.

If the watchdog's kill arrives first (for example while a single step is using a lot of CPU), the loop still
resumes the session. The prompt then names the signal and asks Claude to check for half-finished work first.

A normal exit (`/exit`, Ctrl-D) is treated as you quitting. The session reopens without a prompt.

## Environment variables

| Variable | Default | Meaning |
| --- | --- | --- |
| `CLAUDE_LOOP_SESSION` | new UUID | Session to resume instead of starting a new one |
| `CLAUDE_LOOP_NAME` | `<host>-<dir>` | Remote Control name |
| `CLAUDE_LOOP_LOG` | `~/.claude/claude-loop.log` | Restart log |
| `CLAUDE_LOOP_AUTO_CONTINUE` | `1` | Set to `0` to resume after a kill without the continue prompt |

## Notes

- To update, run the `install` command from step 1 again. A loop that is already running keeps its old code,
  because bash parsed the whole `while` loop when it entered it. To pick up changes, press `q` at the
  "restarting in 5s" prompt and start the loop again with `CLAUDE_LOOP_SESSION=<session uuid> claude-loop.sh`.
- `claude-cpu-watch.sh` takes the threshold and poll interval as arguments: `claude-cpu-watch.sh [840] [5]`.
