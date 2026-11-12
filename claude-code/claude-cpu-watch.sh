#!/usr/bin/env bash
# claude-cpu-watch.sh: companion to claude-loop.sh.
# Waits until the enclosing Claude Code process has used THRESHOLD seconds of CPU (user+sys),
# then prints one line and exits. Claude runs it with Bash run_in_background, so the exit is
# the notification that it is time to clean up and restart before the CPU watchdog kills it.
#
# Usage: claude-cpu-watch.sh [threshold_seconds=840] [poll_seconds=5]
set -u
threshold=${1:-840}
poll=${2:-5}
hz=$(getconf CLK_TCK)

# Walk up from this shell to the nearest ancestor named "claude".
pid=$$
while ((pid > 1)); do
  read -r comm </proc/$pid/comm
  [[ $comm == claude ]] && break
  while read -r key val; do [[ $key == PPid: ]] && pid=$val && break; done </proc/$pid/status
done
if ((pid <= 1)); then
  echo "cpu-watch: no claude ancestor found"
  exit 2
fi

while :; do
  if ! read -r stat </proc/$pid/stat 2>/dev/null; then
    echo "cpu-watch: claude pid $pid is gone"
    exit 3
  fi
  rest=${stat##*) }   # drop "pid (comm) "; comm may contain spaces
  set -- $rest        # $1 = field 3 (state), so utime = $12, stime = $13
  secs=$(((${12} + ${13}) / hz))
  if ((secs >= threshold)); then
    echo "CPU LIMIT NEAR: claude pid $pid at ${secs}s CPU (threshold ${threshold}s, watchdog ~900s)." \
         "Stop non-resumable shells/monitors, then: setsid nohup bash -c 'sleep 5; kill -TERM $pid' >/dev/null 2>&1 &"
    exit 0
  fi
  sleep "$poll"
done
