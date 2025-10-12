#!/usr/bin/env python3
"""
Log Claude Code session to chat_history.md

This script appends session summaries to chat_history.md to maintain
development continuity across Claude Code resets.

Usage:
    python scripts/log_session.py "Session description"
    python scripts/log_session.py "Completed Bronze to Silver transformations"

    # Auto-use last commit message
    python scripts/log_session.py "$(git log -1 --pretty=%B)"
"""

import sys
from pathlib import Path
from datetime import datetime


def log_session(description):
    """Append session log to chat_history.md"""

    # Get project root (2 levels up from this script)
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent

    # Path to chat_history.md
    history_path = project_root / 'notes' / 'claude-code-context' / 'chat_history.md'

    # Read existing content or create new file
    if history_path.exists():
        existing_content = history_path.read_text()
    else:
        # Create new chat_history.md with header
        history_path.parent.mkdir(exist_ok=True)
        existing_content = """# Chat History - Development Sessions

> This file logs Claude Code sessions to maintain context across resets. Append new sessions with `python scripts/log_session.py "description"`.

**Purpose:** When Claude Code is reset, this file provides historical context of development decisions, challenges faced, and solutions implemented.

---

"""
        history_path.write_text(existing_content)

    # Create session entry
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    session_entry = f"""## Session: {timestamp}

**Description:** {description}

**Activities:**
- [Document activities here or let Claude Code update after review]

**Key Decisions:**
- [Document decisions made during this session]

**Challenges & Solutions:**
- [Document any issues encountered and how they were resolved]

**Next Steps:**
- [Document what should be done next]

**Files Modified:**
- [List files changed during this session]

---

"""

    # Append to file
    with history_path.open('a') as f:
        f.write(session_entry)

    print(f"✅ Session logged: {history_path}")
    print(f"📅 Timestamp: {timestamp}")
    print(f"📝 Description: {description}")
    print(f"\n💡 Tip: Edit {history_path} to add more details about activities, decisions, and next steps.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/log_session.py \"Session description\"")
        print("\nExample:")
        print("  python scripts/log_session.py \"Completed Bronze to Silver transformations\"")
        print("  python scripts/log_session.py \"$(git log -1 --pretty=%B)\"")
        sys.exit(1)

    description = ' '.join(sys.argv[1:])
    log_session(description)


if __name__ == '__main__':
    main()
