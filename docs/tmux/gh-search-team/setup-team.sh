#!/bin/bash
# gh-search 3-Person Scrum Team - Automated Setup Script

set -e

PROJECT_ROOT="/home/hungson175/dev/mcp-servers/gh-search"
SESSION_NAME="gh-search-team"
PROMPTS_DIR="$PROJECT_ROOT/docs/tmux/gh-search-team/prompts"

echo "Starting gh-search 3-Person Scrum Team Setup..."
echo "Project: GitHub Project Search MCP Server"
echo ""

# Verify tm-send is installed globally
if ! command -v tm-send &> /dev/null; then
    echo "❌ ERROR: tm-send not found in PATH"
    echo "   tm-send must be installed globally at ~/.local/bin/tm-send"
    echo "   Please install tm-send before running this script."
    exit 1
fi

echo "✓ tm-send found at $(which tm-send)"
echo ""

# Kill existing session if exists
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "Killing existing session: $SESSION_NAME"
    tmux kill-session -t $SESSION_NAME
fi

# Create session
echo "Creating tmux session: $SESSION_NAME"
cd "$PROJECT_ROOT"
tmux new-session -d -s $SESSION_NAME

# Create 3-pane layout (PO, TL, DEV)
echo "Creating 3-pane layout..."
tmux split-window -h -t $SESSION_NAME  # Split into 2 panes
tmux split-window -h -t $SESSION_NAME  # Split into 3 panes
tmux select-layout -t $SESSION_NAME even-horizontal

# CRITICAL: Resize window for responsive panes (prevents narrow panes in detached sessions)
echo "Resizing window for responsive panes..."
tmux resize-window -t $SESSION_NAME -x 500 -y 50

# Set pane titles (visual display)
echo "Setting pane titles..."
tmux select-pane -t $SESSION_NAME:0.0 -T "PO"
tmux select-pane -t $SESSION_NAME:0.1 -T "Tech-Lead"
tmux select-pane -t $SESSION_NAME:0.2 -T "Developer"

# Set @role_name options (CRITICAL - stable role names)
echo "Setting stable role names (@role_name)..."
tmux set-option -p -t $SESSION_NAME:0.0 @role_name "PO"
tmux set-option -p -t $SESSION_NAME:0.1 @role_name "TL"
tmux set-option -p -t $SESSION_NAME:0.2 @role_name "DEV"

# Start Claude Code in each pane
echo "Starting Claude Code in each pane..."
tmux send-keys -t $SESSION_NAME:0.0 "cd $PROJECT_ROOT && claude" C-m
sleep 2
tmux send-keys -t $SESSION_NAME:0.1 "cd $PROJECT_ROOT && claude" C-m
sleep 2
tmux send-keys -t $SESSION_NAME:0.2 "cd $PROJECT_ROOT && claude" C-m

echo "Waiting for Claude Code to initialize..."
sleep 15

# Initialize roles
echo "Initializing agent roles..."
tmux send-keys -t $SESSION_NAME:0.0 "/init-role PO" C-m
sleep 1
tmux send-keys -t $SESSION_NAME:0.0 C-m
sleep 3

tmux send-keys -t $SESSION_NAME:0.1 "/init-role TL" C-m
sleep 1
tmux send-keys -t $SESSION_NAME:0.1 C-m
sleep 3

tmux send-keys -t $SESSION_NAME:0.2 "/init-role DEV" C-m
sleep 1
tmux send-keys -t $SESSION_NAME:0.2 C-m

echo ""
echo "Waiting for role initialization..."
sleep 10

# Get pane IDs
echo "Getting pane IDs..."
PANE_IDS=$(tmux list-panes -t $SESSION_NAME -F "#{pane_id}")
PO_PANE=$(echo "$PANE_IDS" | sed -n '1p')
TL_PANE=$(echo "$PANE_IDS" | sed -n '2p')
DEV_PANE=$(echo "$PANE_IDS" | sed -n '3p')

echo "Pane IDs:"
echo "  PO  (pane 0): $PO_PANE"
echo "  TL  (pane 1): $TL_PANE"
echo "  DEV (pane 2): $DEV_PANE"
echo ""

echo "=" * 80
echo "✅ Setup Complete!"
echo "=" * 80
echo ""
echo "Team Information:"
echo "  Session: $SESSION_NAME"
echo "  Roles: PO (Product Owner), TL (Tech Lead), DEV (Developer)"
echo "  Project: gh-search MCP Server"
echo ""
echo "Next Steps:"
echo "  1. Attach to session: tmux attach -t $SESSION_NAME"
echo "  2. BOSS provides initial requirements to PO"
echo "  3. PO manages backlog and assigns sprints"
echo "  4. Team self-coordinates through sprints"
echo ""
echo "Important Files:"
echo "  - PRODUCT_BACKLOG: docs/tmux/gh-search-team/PRODUCT_BACKLOG.md"
echo "  - WHITEBOARD: docs/tmux/gh-search-team/WHITEBOARD.md"
echo "  - Sprint folders: docs/tmux/gh-search-team/sprints/sprint-N/"
echo "  - Workflow docs: docs/tmux/gh-search-team/workflow.md"
echo ""
echo "Communication:"
echo "  - Use tm-send for agent messages"
echo "  - All communication flows through PO"
echo "  - BOSS uses >>> prefix to send to PO"
echo ""
echo "Progressive Development:"
echo "  - Always: 10 → 100 → 1,000 → full scale"
echo "  - Test-Driven Development (TDD) for all src/ code"
echo "  - Commit frequently (small, focused commits)"
echo ""
echo "Ready to start Sprint 0!"
echo "First task: P0-1 Clean Up Project Structure (assigned to TL)"
