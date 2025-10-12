#!/usr/bin/env python3
"""
Generate project_context.md with current project state.

This script creates a comprehensive snapshot of the project for Claude Code
to quickly understand the current state when starting a new session.

Usage:
    python scripts/generate_context.py
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime
import json


def run_command(cmd, cwd=None):
    """Run shell command and return output."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"


def get_git_info(project_root):
    """Get git repository information."""
    info = {}
    info['branch'] = run_command('git branch --show-current', cwd=project_root)
    info['last_commit'] = run_command('git log -1 --oneline', cwd=project_root)
    info['recent_commits'] = run_command('git log -5 --oneline', cwd=project_root)
    info['status'] = run_command('git status --short', cwd=project_root)
    return info


def get_directory_structure(project_root, exclude_dirs=None):
    """Generate directory tree structure."""
    if exclude_dirs is None:
        exclude_dirs = {'venv', '__pycache__', '.git', 'node_modules', 'minio'}

    tree_lines = []

    def walk_dir(path, prefix='', is_last=True):
        if path.name in exclude_dirs or path.name.startswith('.'):
            return

        connector = '└── ' if is_last else '├── '
        tree_lines.append(f"{prefix}{connector}{path.name}/")

        if path.is_dir():
            try:
                children = sorted(list(path.iterdir()), key=lambda x: (not x.is_dir(), x.name))
                children = [c for c in children if c.name not in exclude_dirs and not c.name.startswith('.')]

                for i, child in enumerate(children):
                    is_last_child = (i == len(children) - 1)
                    extension = '    ' if is_last else '│   '

                    if child.is_dir():
                        walk_dir(child, prefix + extension, is_last_child)
                    else:
                        child_connector = '└── ' if is_last_child else '├── '
                        tree_lines.append(f"{prefix}{extension}{child_connector}{child.name}")
            except PermissionError:
                pass

    tree_lines.append(f"{project_root.name}/")
    try:
        children = sorted(list(project_root.iterdir()), key=lambda x: (not x.is_dir(), x.name))
        children = [c for c in children if c.name not in exclude_dirs and not c.name.startswith('.')]

        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)

            if child.is_dir():
                walk_dir(child, '', is_last_child)
            else:
                connector = '└── ' if is_last_child else '├── '
                tree_lines.append(f"{connector}{child.name}")
    except PermissionError:
        pass

    return '\n'.join(tree_lines)


def count_files_by_type(project_root, exclude_dirs=None):
    """Count files by extension."""
    if exclude_dirs is None:
        exclude_dirs = {'venv', '__pycache__', '.git', 'node_modules', 'minio'}

    counts = {}

    for path in project_root.rglob('*'):
        # Skip excluded directories
        if any(excluded in path.parts for excluded in exclude_dirs):
            continue

        if path.is_file():
            ext = path.suffix if path.suffix else 'no_extension'
            counts[ext] = counts.get(ext, 0) + 1

    return counts


def get_data_files_info(project_root):
    """Get information about data files."""
    data_dir = project_root / 'data'
    info = []

    if not data_dir.exists():
        return ["No data/ directory found"]

    for csv_file in data_dir.rglob('*.csv'):
        rel_path = csv_file.relative_to(project_root)
        try:
            line_count = len(csv_file.read_text().splitlines()) - 1  # Subtract header
            size = csv_file.stat().st_size
            info.append(f"  - `{rel_path}`: {line_count} rows, {size / 1024:.1f} KB")
        except Exception as e:
            info.append(f"  - `{rel_path}`: Error reading file")

    for parquet_file in data_dir.rglob('*.parquet'):
        rel_path = parquet_file.relative_to(project_root)
        size = parquet_file.stat().st_size
        info.append(f"  - `{rel_path}`: {size / 1024:.1f} KB")

    return info if info else ["No data files found"]


def get_docker_status():
    """Get Docker container status."""
    try:
        containers = run_command('docker ps --format "{{.Names}}: {{.Status}}"')
        return containers if containers else "No running containers"
    except Exception:
        return "Docker not available or not running"


def get_python_packages():
    """Get installed Python packages."""
    try:
        packages = run_command('pip list --format=json')
        if packages.startswith('Error'):
            return "Unable to read packages"

        packages_list = json.loads(packages)
        # Only show key packages (not entire list)
        key_packages = ['pandas', 'pyspark', 'boto3', 'minio', 'pytest', 'delta-spark']
        relevant = [p for p in packages_list if p['name'].lower() in key_packages]
        return '\n'.join([f"  - {p['name']}=={p['version']}" for p in relevant]) or "No key packages found"
    except Exception:
        return "Unable to read packages"


def generate_context():
    """Generate project_context.md file."""

    # Get project root (2 levels up from this script)
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent

    # Gather information
    git_info = get_git_info(project_root)
    dir_structure = get_directory_structure(project_root)
    file_counts = count_files_by_type(project_root)
    data_info = get_data_files_info(project_root)
    docker_status = get_docker_status()
    python_packages = get_python_packages()

    # Read README if exists
    readme_path = project_root / 'README.md'
    project_description = "No README.md found"
    if readme_path.exists():
        readme_content = readme_path.read_text()
        # Extract first paragraph or first 500 chars
        lines = [l for l in readme_content.split('\n') if l.strip() and not l.startswith('#')]
        if lines:
            project_description = lines[0][:500]

    # Generate markdown content
    content = f"""# Project Context - Auto-Generated

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

> This file is automatically generated by `scripts/generate_context.py`. It provides a snapshot of the current project state for Claude Code to quickly understand context in new sessions.

---

## 📋 Project Overview

**Project:** {project_root.name}

**Description:** {project_description}

---

## 📁 Project Structure

```
{dir_structure}
```

---

## 📊 File Statistics

**Files by type:**
{chr(10).join([f"- `{ext}`: {count} files" for ext, count in sorted(file_counts.items(), key=lambda x: x[1], reverse=True)[:10]])}

---

## 💾 Data Assets

{chr(10).join(data_info)}

---

## 🔧 Infrastructure Status

### Docker Containers
```
{docker_status}
```

### Python Environment
```
{python_packages}
```

---

## 🔀 Git Status

**Current Branch:** `{git_info['branch']}`

**Last Commit:** `{git_info['last_commit']}`

**Recent Commits:**
```
{git_info['recent_commits']}
```

**Working Directory Status:**
```
{git_info['status'] if git_info['status'] else 'Clean working directory'}
```

---

## 🎯 Current Development Stage

<!-- Update this section manually or via log_session.py -->

**Stage:** [UPDATE MANUALLY]

**Completed:**
- [ ] Bronze layer ingestion
- [ ] Silver layer transformations
- [ ] Gold layer aggregations
- [ ] Pipeline orchestration
- [ ] Visualization/Dashboard

**In Progress:**
- [ ] [UPDATE MANUALLY]

**Next Steps:**
- [ ] [UPDATE MANUALLY]

---

## 📝 Key Files and Their Purpose

<!-- Auto-detected key files -->

**Configuration:**
- `docker-compose.yml` - Local infrastructure setup
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template

**Scripts:**
{chr(10).join([f"- `{f.relative_to(project_root)}` - [DESCRIBE PURPOSE]" for f in (project_root / 'scripts').glob('*.py')]) if (project_root / 'scripts').exists() else '- No scripts directory'}

**Notebooks:**
{chr(10).join([f"- `{f.relative_to(project_root)}` - [DESCRIBE PURPOSE]" for f in list(project_root.glob('*.ipynb'))[:5]]) or '- No notebooks in root'}

**Tests:**
{chr(10).join([f"- `{f.relative_to(project_root)}` - [DESCRIBE PURPOSE]" for f in (project_root / 'tests').glob('*.py')]) if (project_root / 'tests').exists() else '- No tests directory'}

---

## 🚀 Quick Start Commands

```bash
# Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt

# Start infrastructure (if using Docker)
docker compose up -d

# Run main pipeline (adjust as needed)
python scripts/run_pipeline.py

# Run tests
pytest tests/ -v
```

---

## 🐛 Known Issues

<!-- Update this section as issues are discovered -->

- None currently

---

## 📌 Important Notes

<!-- Add project-specific notes here -->

- **Token Optimization:** Use specific queries, reference files with `@filename`, and use `/compact` when context grows
- **Context Regeneration:** Run `python scripts/generate_context.py` before major sessions or after significant changes
- **Session Logging:** Use `python scripts/log_session.py "description"` to append to chat_history.md

---

## 🔗 Related Files

- [claude.md](claude.md) - Claude Code guidelines and best practices
- [chat_history.md](chat_history.md) - Development session history
- [README.md](../README.md) - User-facing project documentation

---

*This file was auto-generated by generate_context.py. Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    # Write to notes/claude-code-context/project_context.md
    output_path = project_root / 'notes' / 'claude-code-context' / 'project_context.md'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)

    print(f"✅ Project context generated: {output_path}")
    print(f"📄 Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Project: {project_root.name}")
    print(f"🔀 Branch: {git_info['branch']}")
    print(f"📝 Last commit: {git_info['last_commit']}")


if __name__ == '__main__':
    generate_context()
