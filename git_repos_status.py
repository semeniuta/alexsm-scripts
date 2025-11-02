#!/usr/bin/env python3
import os
import subprocess

def run_git_command(repo_path, *args):
    """Run a git command in the given repo and return (success, output)."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)

def check_repo_status(repo_path):
    status = {"path": repo_path}

    # 1. Check if this is a Git repository
    success, output = run_git_command(repo_path, "rev-parse", "--is-inside-work-tree")
    if not success:
        status["is_git_repo"] = False
        return status
    status["is_git_repo"] = True

    # 2. Check for unstaged or uncommitted changes
    success, output = run_git_command(repo_path, "status", "--porcelain")
    status["has_unstaged_changes"] = bool(output.strip())

    # 3. Check if a remote exists
    success, output = run_git_command(repo_path, "remote")
    remotes = output.splitlines()
    status["has_remote"] = len(remotes) > 0

    # 4. Check sync status with remote
    if status["has_remote"]:
        run_git_command(repo_path, "fetch", "--quiet")
        success, output = run_git_command(repo_path, "status", "-sb")
        if success:
            # Example: "## main...origin/main [ahead 1]"
            if "ahead" in output or "behind" in output:
                status["is_synced"] = False
            else:
                status["is_synced"] = True
        else:
            status["is_synced"] = None
    else:
        status["is_synced"] = None

    return status


def main():
    print("Scanning subdirectories...\n")
    current_dir = os.getcwd()
    dirs = [d for d in os.listdir(current_dir) if os.path.isdir(d)]

    for d in sorted(dirs):
        repo_path = os.path.join(current_dir, d)
        status = check_repo_status(repo_path)

        print(f"📁 {d}")
        if not status["is_git_repo"]:
            print("  ❌ Not a Git repository\n")
            continue

        print(f"  🧩 Unstaged changes: {'Yes' if status['has_unstaged_changes'] else 'No'}")
        print(f"  🌐 Has remote: {'Yes' if status['has_remote'] else 'No'}")
        if status["has_remote"]:
            sync_state = (
                "✅ Synced" if status["is_synced"] else
                "⚠️ Out of sync" if status["is_synced"] is False else
                "❓ Unknown"
            )
            print(f"  🔄 Sync status: {sync_state}")
        print()

if __name__ == "__main__":
    main()

