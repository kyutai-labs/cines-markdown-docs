#!/usr/bin/env bash
# claude-loop.sh: keep one Claude Code conversation alive across kills (e.g. a CPU-time watchdog).
# Each restart resumes the same session ID with Remote Control on, under the same name.
# After a kill (Claude's own planned SIGTERM, or the watchdog), the resumed session gets a prompt
# telling Claude to re-arm claude-cpu-watch.sh and carry on with its task.
#
# Usage:  ./claude-loop.sh [extra claude args...]     e.g. ./claude-loop.sh --permission-mode auto
# Env:    CLAUDE_LOOP_SESSION=<uuid>  pick up an existing session instead of starting a new one
#         CLAUDE_LOOP_NAME=<name>     Remote Control name (default: <host>-<dir>)
#         CLAUDE_LOOP_LOG=<file>      restart log (default: ~/.claude/claude-loop.log)
#         CLAUDE_LOOP_AUTO_CONTINUE=0 resume after a kill without sending the continue prompt
set -u

session_id=${CLAUDE_LOOP_SESSION:-$(cat /proc/sys/kernel/random/uuid)}
rc_name=${CLAUDE_LOOP_NAME:-"$(hostname -s)-$(basename "$PWD")"}
config_dir=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
log=${CLAUDE_LOOP_LOG:-$config_dir/claude-loop.log}
min_uptime=30      # a run shorter than this (seconds) counts as a fast failure
max_fast_fails=5   # stop after this many fast failures in a row
delay=5            # seconds to wait before restarting
auto_continue=${CLAUDE_LOOP_AUTO_CONTINUE:-1}
watch_script="$(cd "$(dirname "$0")" && pwd)/claude-cpu-watch.sh"

# A killed TUI leaves the terminal in raw mode / alt screen / mouse mode; undo that.
restore_tty() {
  stty sane 2>/dev/null
  printf '\e[?1049l\e[?25h\e[?1000l\e[?1002l\e[?1003l\e[?1006l\e[?2004l\e[<u'
}

# Claude only writes the transcript after the first message; until then --resume would fail.
session_exists() { compgen -G "$config_dir/projects/*/$session_id.jsonl" >/dev/null; }

say() { printf '\e[1;36m[claude-loop]\e[0m %s\n' "$*"; }

# Total user+sys CPU seconds of all children this shell has reaped (counts killed ones too).
# Must not run in a $(...) subshell, so it sets $children_cpu instead of printing.
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT
read_children_cpu() {
  times >"$tmp"
  children_cpu=$(awk 'NR == 2 { for (i = 1; i <= 2; i++) { split($i, t, /[ms]/); n += t[1] * 60 + t[2] }
                                printf "%.0f", n }' "$tmp")
}
fast_fails=0
run=0
resume_prompt=()   # initial prompt for the next run; set only after a kill

say "session $session_id, remote control name '$rc_name', log $log"
while :; do
  run=$((run + 1))
  if session_exists; then mode=(--resume "$session_id"); else mode=(--session-id "$session_id"); fi

  trap ':' INT     # a stray SIGINT while claude runs must not kill the loop
  start=$SECONDS
  read_children_cpu; cpu_before=$children_cpu
  # The prompt goes right after the Remote Control name so no flag in "$@" can swallow it.
  claude "${mode[@]}" --remote-control "$rc_name" "${resume_prompt[@]}" "$@"
  rc=$?
  uptime=$((SECONDS - start))
  restore_tty
  read_children_cpu; cpu=$((children_cpu - cpu_before))
  sig=""
  if ((rc > 128)); then sig=$(kill -l $((rc - 128)) 2>/dev/null || echo $((rc - 128))); why="killed by SIG$sig"
  else why="exited with code $rc"; fi

  # A kill interrupts Claude, so the next run tells it to pick up where it left off.
  # A normal exit (/exit, Ctrl-D) means the user quit, so the next run just reopens the session.
  resume_prompt=()
  if [[ -n $sig && $auto_continue != 0 ]] && session_exists; then
    if [[ $sig == TERM ]]; then
      what="Claude Code was restarted by your planned SIGTERM after the CPU watch fired."
    else
      what="Claude Code was killed by SIG$sig (probably the CPU watchdog), possibly in the middle of a step."
    fi
    resume_prompt=("[claude-loop] Session resumed automatically. $what" \
      "First re-arm the CPU watch: run $watch_script 840 5 with Bash run_in_background." \
      "Then check whatever may have been interrupted (half-finished commands or edits) and carry on with the task you were working on." \
      "If no task was in progress, reply in one line and stop.")
    resume_prompt=("${resume_prompt[*]}")   # join into a single argument
  fi

  echo
  say "run $run $why after ${uptime}s wall, ${cpu}s CPU"
  printf '%s run=%d session=%s %s wall=%ss cpu=%ss\n' \
    "$(date '+%F %T')" "$run" "$session_id" "${why// /_}" "$uptime" "$cpu" >>"$log"

  if ((uptime < min_uptime)); then fast_fails=$((fast_fails + 1)); else fast_fails=0; fi
  if ((fast_fails >= max_fast_fails)); then
    say "$fast_fails quick exits in a row, giving up. Resume by hand: claude --resume $session_id"
    exit 1
  fi

  trap 'echo; say "stopped. Resume by hand: claude --resume $session_id"; exit 0' INT
  say "restarting in ${delay}s. Enter: restart now, q or Ctrl-C: quit"
  if read -r -s -n1 -t "$delay" key && [[ $key == q ]]; then
    say "stopped. Resume by hand: claude --resume $session_id"
    exit 0
  fi
done
