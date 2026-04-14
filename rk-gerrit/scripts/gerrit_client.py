#!/usr/bin/env python3
"""
Gerrit SSH client for Rockchip internal Gerrit.
"""

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional


class GerritSSHClient:
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_path = Path(__file__).resolve().parent.parent / "config" / "gerrit_config.json"
        config_path = Path(config_path)
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.config_path = config_path
        self.server = config["server"]
        self.port = config.get("port", 29418)
        self.username = config["username"]
        self.key_file = config_path.parent / config["key_file"]
        self.default_limit = config.get("default_limit", 20)
        self.web_url_template = config.get(
            "web_url_template",
            f"https://{self.server}/c/{{project}}/+/{{number}}",
        )

    def _run_ssh_command(self, gerrit_cmd: str) -> str:
        cmd = [
            "ssh",
            "-p",
            str(self.port),
            "-i",
            str(self.key_file),
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "UserKnownHostsFile=/dev/null",
            "-o",
            "LogLevel=ERROR",
            f"{self.username}@{self.server}",
            f"gerrit {gerrit_cmd}",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "SSH command failed")
        return result.stdout

    @staticmethod
    def _parse_json_lines(output: str) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for line in output.strip().splitlines():
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            if data.get("type") != "stats":
                results.append(data)
        return results

    def search_changes(self, query: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        limit = limit or self.default_limit
        cmd = f'query --format=JSON --commit-message "{query}" limit:{limit}'
        return self._parse_json_lines(self._run_ssh_command(cmd))

    def get_change_detail(
        self,
        change_id: str,
        include_current_patch_set: bool = True,
        include_patch_sets: bool = False,
        include_files: bool = False,
        include_comments: bool = False,
        include_all_approvals: bool = False,
        include_submit_records: bool = False,
        include_commit_message: bool = False,
    ) -> Dict[str, Any]:
        flags: List[str] = []
        if include_current_patch_set:
            flags.append("--current-patch-set")
        if include_patch_sets:
            flags.append("--patch-sets")
        if include_files:
            flags.append("--files")
        if include_comments:
            flags.append("--comments")
        if include_all_approvals:
            flags.append("--all-approvals")
        if include_submit_records:
            flags.append("--submit-records")
        if include_commit_message:
            flags.append("--commit-message")

        flags_text = " ".join(flags)
        cmd = f"query --format=JSON {flags_text} change:{change_id}".strip()
        results = self._parse_json_lines(self._run_ssh_command(cmd))
        if not results:
            raise ValueError(f"Change {change_id} not found")
        return results[0]

    def get_change(self, change_id: str) -> Dict[str, Any]:
        return self.get_change_detail(change_id, include_current_patch_set=True, include_commit_message=True)

    def get_change_with_files(self, change_id: str) -> Dict[str, Any]:
        return self.get_change_detail(
            change_id,
            include_current_patch_set=True,
            include_files=True,
            include_commit_message=True,
        )

    def list_projects(self, prefix: Optional[str] = None) -> List[str]:
        cmd = "ls-projects"
        if prefix:
            cmd += f" --prefix {prefix}"
        output = self._run_ssh_command(cmd)
        return [line.strip() for line in output.splitlines() if line.strip()]

    def get_version(self) -> str:
        return self._run_ssh_command("version").strip()


def main() -> None:
    client = GerritSSHClient()
    print("Testing Gerrit SSH access...")
    print(f"Server: {client.server}:{client.port}")
    print(f"User: {client.username}")
    version = client.get_version()
    print(f"Gerrit version: {version}")
    print("\nRecent merged changes:")
    for change in client.search_changes("status:merged", limit=3):
        print(f"  #{change.get('number')}: {change.get('subject', '')}")
    projects = client.list_projects()
    print(f"\nProject count: {len(projects)}")


if __name__ == "__main__":
    main()
