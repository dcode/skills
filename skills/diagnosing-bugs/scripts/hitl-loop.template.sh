#!/usr/bin/env bash
# ==============================================================================
# Script Name:   hitl-debug-template.sh
# Description:   Agent-driven Human-in-the-Loop (HITL) interactive debugging
#                and telemetry capture template.
#
#                IMMUTABLE HARNESS: Do not edit outside the clearly marked
#                AGENT-EDITABLE SECTION below.
# ==============================================================================

set -Eeuo pipefail
IFS=$'\n\t'

# ==============================================================================
# IMMUTABLE HARNESS — DO NOT EDIT ABOVE THE AGENT-EDITABLE SECTION
# ==============================================================================

readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly RUN_ID="$(date -u +"%Y%m%dT%H%M%SZ")-$$"

BUNDLE_DIR="${BUNDLE_DIR:-/tmp/hitl-debug-${RUN_ID}}"
ARCHIVE_BUNDLE=false
PROMPT_TIMEOUT=0

declare -a BG_PIDS=()
declare -a BG_NAMES=()
TIMELINE_FILE=""
NOTES_FILE=""

# --- Colors & Formatting ------------------------------------------------------
if [[ -t 1 ]]; then
  readonly RED=$'\033[0;31m'
  readonly GREEN=$'\033[0;32m'
  readonly YELLOW=$'\033[1;33m'
  readonly CYAN=$'\033[0;36m'
  readonly BOLD=$'\033[1m'
  readonly NC=$'\033[0m'
else
  readonly RED='' GREEN='' YELLOW='' CYAN='' BOLD='' NC=''
fi

# --- Portable Timestamps & Logging --------------------------------------------
utc_now() {
  local ts
  ts="$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ" 2>/dev/null || true)"
  if [[ -z "$ts" || "$ts" == *"%3N"* || "$ts" == *"3N"* ]]; then
    date -u +"%Y-%m-%dT%H:%M:%SZ"
  else
    printf '%s' "$ts"
  fi
}

record_event() {
  local category="$1"
  shift
  local msg="$*"
  if [[ -n "$TIMELINE_FILE" ]]; then
    printf '[%s] [%s] %s\n' "$(utc_now)" "$category" "$msg" >> "$TIMELINE_FILE"
  fi
}

info()  { printf "${CYAN}[INFO]${NC} %s\n" "$*"; record_event "INFO" "$*"; }
warn()  { printf "${YELLOW}[WARN]${NC} %s\n" "$*" >&2; record_event "WARN" "$*"; }
error() { printf "${RED}[ERROR]${NC} %s\n" "$*" >&2; record_event "ERROR" "$*"; }

# --- Bundle Initialization & Cleanup ------------------------------------------
init_bundle() {
  mkdir -p "$BUNDLE_DIR"/{snapshots,logs,notes}
  TIMELINE_FILE="$BUNDLE_DIR/timeline.log"
  NOTES_FILE="$BUNDLE_DIR/notes/operator-observations.md"

  cat <<EOF > "$NOTES_FILE"
# HITL Debug Capture: ${SESSION_TITLE:-Untitled Session}
- **Goal:** ${SESSION_GOAL:-Not specified}
- **Run ID:** ${RUN_ID}
- **Operator:** ${USER:-unknown}
- **Host:** $(hostname -f 2>/dev/null || hostname)
- **Started (UTC):** $(utc_now)

## Timeline & Operator Observations
EOF
  record_event "START" "Session='${SESSION_TITLE:-Untitled}' Bundle='${BUNDLE_DIR}'"
}

stop_collectors() {
  local i pid name
  for (( i = 0; i < ${#BG_PIDS[@]}; i++ )); do
    pid="${BG_PIDS[$i]}"
    name="${BG_NAMES[$i]}"
    if kill -0 "$pid" 2>/dev/null; then
      record_event "COLLECTOR_STOP" "Stopping collector '$name' (pid=$pid)"
      # SIGINT first so tools like tcpdump/serial loggers flush buffers cleanly
      kill -INT "$pid" 2>/dev/null || true
    fi
  done

  sleep 0.5

  for (( i = 0; i < ${#BG_PIDS[@]}; i++ )); do
    pid="${BG_PIDS[$i]}"
    if kill -0 "$pid" 2>/dev/null; then
      kill -TERM "$pid" 2>/dev/null || true
      sleep 0.3
      if kill -0 "$pid" 2>/dev/null; then
        kill -KILL "$pid" 2>/dev/null || true
      fi
    fi
    wait "$pid" 2>/dev/null || true
  done
}

cleanup() {
  local exit_code=$?
  stop_collectors
  record_event "END" "Capture session ended with exit code $exit_code"

  if [[ -d "$BUNDLE_DIR" ]]; then
    if [[ "$ARCHIVE_BUNDLE" == true ]]; then
      local tarball="${BUNDLE_DIR}.tar.gz"
      tar -czf "$tarball" -C "$(dirname "$BUNDLE_DIR")" "$(basename "$BUNDLE_DIR")"
      printf "\n${GREEN}[BUNDLE READY]${NC} Archive: ${BOLD}%s${NC}\n" "$tarball"
      printf "AGENT_BUNDLE_ARCHIVE=%s\n" "$tarball"
    else
      printf "\n${GREEN}[BUNDLE READY]${NC} Directory: ${BOLD}%s${NC}\n" "$BUNDLE_DIR"
    fi
    printf "AGENT_BUNDLE_DIR=%s\n" "$BUNDLE_DIR"
    printf "AGENT_NOTES_FILE=%s\n" "$NOTES_FILE"
    printf "AGENT_TIMELINE_FILE=%s\n" "$TIMELINE_FILE"
  fi
}
trap cleanup EXIT

usage() {
  cat <<EOF
Usage: $SCRIPT_NAME [OPTIONS]

Agent-driven Human-in-the-Loop (HITL) interactive debugging & telemetry capture.

Options:
  -o, --out-dir DIR      Directory to store captured artifacts (default: /tmp/hitl-debug-<ts>)
  -t, --timeout SEC      Abort if human input is not received within SEC seconds
  -a, --archive          Also package output into a .tar.gz archive on exit
  -h, --help             Show this help message
EOF
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -o|--out-dir)
        BUNDLE_DIR="${2:?--out-dir requires a directory path}"
        shift 2
        ;;
      -t|--timeout)
        PROMPT_TIMEOUT="${2:?--timeout requires a numeric value}"
        shift 2
        ;;
      -a|--archive)
        ARCHIVE_BUNDLE=true
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        error "Unknown option: $1"
        usage
        exit 1
        ;;
    esac
  done
}

# --- Telemetry & HITL Primitives (Callable from Agent-Editable Section) -------

# Start a background telemetry collector and log its stdout/stderr to $BUNDLE_DIR/logs/<name>.log
# Usage: register_collector "<name>" <command> [args...]
register_collector() {
  local name="$1"
  shift
  local logfile="$BUNDLE_DIR/logs/${name}.log"
  info "Starting collector '${name}' -> ${logfile}"
  "$@" > "$logfile" 2>&1 &
  local pid=$!
  BG_PIDS+=("$pid")
  BG_NAMES+=("$name")
  record_event "COLLECTOR_START" "Started collector '$name' (pid=$pid) cmd='$*'"
}

# Run a snapshot probe via the agent-defined capture_state_snapshot hook
_run_snapshot() {
  local label="$1"
  local snap_dir="$BUNDLE_DIR/snapshots/${label}"
  mkdir -p "$snap_dir"
  record_event "SNAPSHOT" "Capturing state: $label"
  capture_state_snapshot "$snap_dir" "$label" || warn "Snapshot hook returned non-zero for $label"
}

# Prompt the human to read/enter a specific value (e.g., LCD fault code, voltage, LED state)
# Usage: hitl_capture_reading "<reading_id>" "<prompt_text>"
hitl_capture_reading() {
  local reading_id="$1"
  local prompt_text="$2"

  if [[ ! -t 0 ]]; then
    error "Interactive TTY required for HITL reading '${reading_id}'."
    return 1
  fi

  printf "\n${YELLOW}INPUT REQUIRED [%s]:${NC} %s\n" "$reading_id" "$prompt_text"
  local read_args=(-r -p "${BOLD}Value: ${NC}")
  [[ "$PROMPT_TIMEOUT" -gt 0 ]] && read_args=(-t "$PROMPT_TIMEOUT" "${read_args[@]}")

  local val=""
  read "${read_args[@]}" val || exit 1
  record_event "HUMAN_READING" "[$reading_id] $val"
  cat <<EOF >> "$NOTES_FILE"
### Reading \`$reading_id\`
- **Timestamp (UTC):** \`$(utc_now)\`
- **Prompt:** $prompt_text
- **Captured Value:** \`${val:-_Empty_}\`

EOF
}

# Guide the human through a physical or software action, bracketed by timestamps & state diffs
# Usage: hitl_step "<step_id>" "<step_title>" "<multiline_instructions>"
hitl_step() {
  local step_id="$1"
  local step_title="$2"
  local instructions="$3"

  _run_snapshot "${step_id}_pre"

  printf "\n${BOLD}======================================================================${NC}\n"
  printf "${YELLOW}HITL STEP [%s]:${NC} %s\n" "$step_id" "$step_title"
  printf "${BOLD}----------------------------------------------------------------------${NC}\n"
  printf "%b\n" "$instructions"
  printf "${BOLD}======================================================================${NC}\n"

  if [[ ! -t 0 ]]; then
    error "Interactive TTY required for HITL debugging."
    return 1
  fi

  local read_args=(-r -p "${BOLD}Press [Enter] right BEFORE starting (or 's' to skip, 'q' to abort): ${NC}")
  [[ "$PROMPT_TIMEOUT" -gt 0 ]] && read_args=(-t "$PROMPT_TIMEOUT" "${read_args[@]}")

  local ready=""
  read "${read_args[@]}" ready || exit 1
  case "${ready,,}" in
    q|quit) exit 1 ;;
    s|skip)
      warn "Operator skipped step [$step_id]: $step_title"
      record_event "HUMAN_ACTION_SKIPPED" "[$step_id] $step_title"
      cat <<EOF >> "$NOTES_FILE"
### Step $step_id: $step_title
- **Outcome:** \`SKIPPED\`

EOF
      return 0
      ;;
  esac

  local action_start
  action_start="$(utc_now)"
  record_event "HUMAN_ACTION_START" "[$step_id] $step_title"
  printf "${CYAN}>>> Telemetry active. Perform the action now...${NC}\n\n"

  while true; do
    read -r -p "${BOLD}Outcome: [p]ass / [f]ail (issue observed) / [n]ote / [r]etry: ${NC}" outcome
    case "${outcome,,}" in
      p|pass|f|fail)
        local status_label="EXPECTED_BEHAVIOR"
        [[ "${outcome,,}" == f* ]] && status_label="ISSUE_OBSERVED"

        record_event "HUMAN_ACTION_END" "[$step_id] Outcome=$status_label"
        _run_snapshot "${step_id}_post"

        diff -ruN "$BUNDLE_DIR/snapshots/${step_id}_pre" "$BUNDLE_DIR/snapshots/${step_id}_post" \
          > "$BUNDLE_DIR/snapshots/${step_id}_diff.patch" 2>&1 || true

        read -r -p "Briefly describe what you observed (optional): " obs
        cat <<EOF >> "$NOTES_FILE"
### Step $step_id: $step_title
- **Window (UTC):** \`$action_start\` -> \`$(utc_now)\`
- **Outcome:** \`$status_label\`
- **Operator Note:** ${obs:-_None provided_}

EOF
        break
        ;;
      n|note)
        read -r -p "Enter timestamped observation note: " mid_note
        record_event "OPERATOR_NOTE" "[$step_id] $mid_note"
        printf -- "- **[%s] Note:** %s\n" "$(utc_now)" "$mid_note" >> "$NOTES_FILE"
        ;;
      r|retry)
        record_event "HUMAN_ACTION_RETRY" "[$step_id] Operator retrying step"
        printf "${CYAN}>>> Marker recorded. Retry the action now...${NC}\n"
        ;;
      *)
        printf "Invalid choice. Enter p (pass), f (fail), n (note), or r (retry).\n"
        ;;
    esac
  done
}

# ==============================================================================
# >>> BEGIN AGENT-EDITABLE SECTION <<<
# ==============================================================================
# AGENTS: Modify ONLY this section. Do NOT edit anything above or below it.
#
# Available harness primitives:
#   register_collector "<log_name>" <cmd> [args...]
#       Runs a background telemetry stream; output saved to $BUNDLE_DIR/logs/<log_name>.log
#   hitl_step "<step_id>" "<step_title>" "<instructions>"
#       Guides the human through an action with pre/post snapshots, diffs, and timestamps.
#   hitl_capture_reading "<reading_id>" "<prompt_text>"
#       Prompts the human to enter an observed value (e.g., LCD code, voltage, LED state).
#   info / warn / error / record_event "<CATEGORY>" "<message>"
#       Structured logging into $BUNDLE_DIR/timeline.log.
# ==============================================================================

SESSION_TITLE="Interactive Debug Session"
SESSION_GOAL="Reproduce issue and capture correlated telemetry and operator observations."

# Called automatically before and after each hitl_step.
# Write any point-in-time state files into "$snap_dir". Leave as ':' if not needed.
capture_state_snapshot() {
  local snap_dir="$1"
  local label="$2"
  : "$snap_dir" "$label"

  # Examples (uncomment/replace for your target):
  # ps -ef > "$snap_dir/processes.txt" 2>&1 || true
  # ss -tulnp > "$snap_dir/sockets.txt" 2>&1 || true
  # ip -s link > "$snap_dir/net_links.txt" 2>&1 || true
}

# Called once before steps begin. Use register_collector for any background streams.
start_background_collectors() {
  :
  # Examples (uncomment/replace for your target):
  # register_collector "journal" journalctl -u my-service -f
  # register_collector "pcap" tcpdump -i any -w "$BUNDLE_DIR/logs/capture.pcap" port 443
  # register_collector "serial" stdbuf -oL cat /dev/ttyUSB0
}

# Define the interactive sequence that drives the human operator.
run_debug_steps() {
  hitl_capture_reading \
    "00-initial-state" \
    "Record the current status/display reading or version before starting."

  hitl_step \
    "01-trigger" \
    "Trigger the Target Behavior" \
    "1. Perform the action that triggers the issue.\n2. Observe the target output, display, or behavior for 10 seconds."

  hitl_step \
    "02-recovery" \
    "Observe Recovery or Reset" \
    "1. Attempt recovery or reset the target.\n2. Note whether normal operation resumes."
}

# ==============================================================================
# >>> END AGENT-EDITABLE SECTION <<<
# ==============================================================================

# ==============================================================================
# IMMUTABLE ENTRYPOINT — DO NOT EDIT BELOW THIS LINE
# ==============================================================================
main() {
  parse_args "$@"
  init_bundle
  info "Initialized capture bundle at $BUNDLE_DIR"
  start_background_collectors
  run_debug_steps
  info "All debug steps completed."
}

main "$@"
