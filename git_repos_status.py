#!/usr/bin/env python3
import os
import subprocess


class GitRepositoryStatus:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.status = {"path": repo_path}

    def run_git_command(self, *args):
        """Run a git command in the repository and return (success, output)."""
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=False,
            )
            return result.returncode == 0, result.stdout.strip()
        except Exception as e:
            return False, str(e)

    def validate_git_repository(self):
        success, _ = self.run_git_command("rev-parse", "--is-inside-work-tree")
        self.status["is_git_repo"] = success
        return success

    def check_for_unstaged_changes(self):
        success, output = self.run_git_command("status", "--porcelain")
        self.status["has_unstaged_changes"] = bool(output.strip())

    def get_remote_information(self):
        success, output = self.run_git_command("remote")
        remotes = [r for r in output.splitlines() if r.strip()]
        self.status["has_remote"] = len(remotes) > 0
        self.status["remotes"] = {}

        if self.status["has_remote"]:
            for r in remotes:
                ok, url = self.run_git_command("remote", "get-url", r)
                self.status["remotes"][r] = url if ok else None

    def check_remote_sync_status(self):
        if not self.status["has_remote"]:
            self.status["is_synced"] = None
            return

        self.run_git_command("fetch", "--quiet")
        success, output = self.run_git_command("status", "-sb")

        if success:
            self.status["is_synced"] = "ahead" not in output and "behind" not in output
        else:
            self.status["is_synced"] = None

    def check_status(self):
        if not self.validate_git_repository():
            return self.status

        self.check_for_unstaged_changes()
        self.get_remote_information()
        self.check_remote_sync_status()

        return self.status


def main():
    print("Scanning subdirectories...\n")
    current_dir = os.getcwd()
    dirs = [d for d in os.listdir(current_dir) if os.path.isdir(d)]

    for d in sorted(dirs):
        repo_path = os.path.join(current_dir, d)
        repo = GitRepositoryStatus(repo_path)
        status = repo.check_status()

        print(f"📁 {d}")
        if not status["is_git_repo"]:
            print("  ❌ Not a Git repository\n")
            continue

        print(
            f"  🧩 Unstaged changes: {'Yes ⚠️' if status['has_unstaged_changes'] else 'No'}"
        )

        ok, branch = repo.run_git_command("rev-parse", "--abbrev-ref", "HEAD")
        if ok:
            print(f"  🏷️ Current branch: \033[1m{branch}\033[0m")

        print(f"  🌐 Has remote: {'Yes' if status['has_remote'] else 'No'}")
        if status["has_remote"]:
            for name, url in status.get("remotes", {}).items():
                print(f"    🔗 {name}: {url}")

            sync_state = (
                "✅ Synced"
                if status["is_synced"]
                else "⚠️⬆️ Out of sync" if status["is_synced"] is False else "❓ Unknown"
            )
            print(f"  🔄 Sync status: {sync_state}")
        print()


if __name__ == "__main__":
    main()
