#!/usr/bin/env python3
"""
Search or inspect Gerrit changes on Rockchip internal Gerrit.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gerrit_client import GerritSSHClient


def format_status(status: str) -> str:
    return {
        "MERGED": "[MERGED]",
        "NEW": "[NEW]",
        "ABANDONED": "[ABANDONED]",
    }.get(status, f"[{status}]")


def format_timestamp(ts: int) -> str:
    try:
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
    except Exception:
        return "N/A"


def search_by_keyword(
    client: GerritSSHClient,
    keyword: str,
    limit: int,
    project: str = None,
    branch: str = None,
    status: str = None,
    rk_only: bool = True,
) -> None:
    query_parts: List[str] = []
    if keyword:
        query_parts.append(keyword)
    if project:
        query_parts.append(f"project:{project}")
    if branch:
        query_parts.append(f"branch:{branch}")
    if status:
        query_parts.append(f"status:{status}")
    if rk_only:
        query_parts.append("owner:rock-chips.com")

    query = " ".join(query_parts) if query_parts else "status:open"
    results = client.search_changes(query, limit=limit)
    if not results:
        print("No results")
        return

    print(f"Search: {query}")
    print("=" * 80)
    for change in results:
        print(f"{format_status(change.get('status', 'UNKNOWN'))} #{change.get('number')}")
        print(f"  {change.get('subject', 'N/A')}")
        print(f"  Project: {change.get('project', 'N/A')} | Branch: {change.get('branch', 'N/A')}")
        print(f"  Updated: {format_timestamp(change.get('lastUpdated', 0))}")
        print(f"  URL: {change.get('url', 'N/A')}")
        print("-" * 80)


def print_basic_metadata(change: Dict[str, Any]) -> None:
    print(f"{format_status(change.get('status', 'UNKNOWN'))} Change #{change.get('number')}")
    print(f"Title: {change.get('subject', 'N/A')}")
    print(f"Change-Id: {change.get('id', 'N/A')}")
    print(f"Project: {change.get('project', 'N/A')}")
    print(f"Branch: {change.get('branch', 'N/A')}")
    owner = change.get("owner", {})
    print(f"Owner: {owner.get('name', 'Unknown')} <{owner.get('email', 'N/A')}>")
    print(f"URL: {change.get('url', 'N/A')}")


def print_current_patch_set(change: Dict[str, Any]) -> None:
    cps = change.get("currentPatchSet", {})
    if not cps:
        return
    print("\nCurrent Patch Set:")
    print(f"  Number: {cps.get('number', 'N/A')}")
    print(f"  Kind: {cps.get('kind', 'N/A')}")
    print(f"  Revision: {cps.get('revision', 'N/A')}")
    print(f"  Ref: {cps.get('ref', 'N/A')}")


def print_changed_files(change: Dict[str, Any]) -> None:
    files = change.get("currentPatchSet", {}).get("files", [])
    if not files:
        return

    visible_files = [entry for entry in files if entry.get("file") != "/COMMIT_MSG"]
    print(f"\nChanged Files ({len(visible_files)}):")
    for entry in visible_files:
        print(
            f"  [{entry.get('type', 'MODIFIED')}] {entry.get('file')} "
            f"(+{entry.get('insertions', 0)} -{abs(entry.get('deletions', 0))})"
        )


def print_submit_records(change: Dict[str, Any]) -> None:
    records = change.get("submitRecords", [])
    if not records:
        return

    print("\nSubmit Records:")
    for idx, record in enumerate(records, start=1):
        print(f"  Record {idx}: {record.get('status', 'N/A')}")
        for label in record.get("labels", []):
            print(f"    - {label.get('label', 'N/A')}: {label.get('status', 'N/A')}")


def print_current_ps_approvals(change: Dict[str, Any]) -> None:
    approvals = change.get("currentPatchSet", {}).get("approvals", [])
    if not approvals:
        return

    print("\nCurrent Patch Set Approvals:")
    for approval in approvals:
        reviewer = approval.get("by", {}).get("name") or approval.get("by", {}).get("username", "unknown")
        print(f"  - {approval.get('type', 'N/A')}{approval.get('value', 'N/A')} by {reviewer}")


def print_current_ps_comments(change: Dict[str, Any]) -> None:
    comments = change.get("currentPatchSet", {}).get("comments", [])
    if not comments:
        return

    print(f"\nCurrent Patch Set Line Comments ({len(comments)}):")
    for comment in comments:
        reviewer = comment.get("reviewer", {}).get("name") or comment.get("reviewer", {}).get("username", "unknown")
        print(
            f"  - {comment.get('file', 'N/A')}:{comment.get('line', 'N/A')} "
            f"[{reviewer}] {comment.get('message', '').strip()}"
        )


def print_timeline_comments(change: Dict[str, Any], limit: int = 10) -> None:
    comments = change.get("comments", [])
    if not comments:
        return

    print(f"\nTimeline Comments (latest {min(limit, len(comments))}):")
    for comment in comments[-limit:]:
        reviewer = comment.get("reviewer", {}).get("name") or comment.get("reviewer", {}).get("username", "unknown")
        message = (comment.get("message") or "").replace("\n", " ").strip()
        if len(message) > 180:
            message = message[:177] + "..."
        print(f"  - {format_timestamp(comment.get('timestamp', 0))} [{reviewer}] {message}")


def print_commit_message(change: Dict[str, Any]) -> None:
    if "commitMessage" in change:
        print("\nCommit Message:")
        print(change["commitMessage"])


def query_by_id(
    client: GerritSSHClient,
    change_id: str,
    show_files: bool = False,
    show_comments: bool = False,
    show_approvals: bool = False,
    show_submit_records: bool = False,
    show_patch_sets: bool = False,
    show_commit_message: bool = False,
    show_timeline: bool = False,
) -> None:
    change = client.get_change_detail(
        change_id,
        include_current_patch_set=True,
        include_patch_sets=show_patch_sets,
        include_files=show_files,
        include_comments=show_comments or show_timeline,
        include_all_approvals=show_approvals,
        include_submit_records=show_submit_records,
        include_commit_message=show_commit_message,
    )

    print_basic_metadata(change)
    print_current_patch_set(change)

    if show_files:
        print_changed_files(change)
    if show_submit_records:
        print_submit_records(change)
    if show_approvals:
        print_current_ps_approvals(change)
    if show_comments:
        print_current_ps_comments(change)
    if show_timeline:
        print_timeline_comments(change)
    if show_commit_message:
        print_commit_message(change)



def main() -> None:
    parser = argparse.ArgumentParser(description="Search Gerrit changes")
    parser.add_argument("keyword", nargs="?", help="search keyword")
    parser.add_argument("--id", "-i", dest="change_id", help="change number or Change-Id")
    parser.add_argument("--limit", "-n", type=int, default=20, help="result limit")
    parser.add_argument("--project", "-p", help="project filter")
    parser.add_argument("--branch", "-b", help="branch filter")
    parser.add_argument("--status", "-s", choices=["merged", "open", "abandoned"], help="status filter")
    parser.add_argument("--all-owners", "-a", action="store_true", help="include all owners")
    parser.add_argument("--files", "-f", action="store_true", help="show changed files")
    parser.add_argument("--comments", action="store_true", help="include current patch set line comments")
    parser.add_argument("--approvals", action="store_true", help="include current patch set approvals")
    parser.add_argument("--submit-records", action="store_true", help="include submit records")
    parser.add_argument("--patch-sets", action="store_true", help="include all patch set metadata")
    parser.add_argument("--timeline", action="store_true", help="show latest timeline comments")
    parser.add_argument("--commit-message", action="store_true", help="include commit message")
    parser.add_argument("--json", "-j", action="store_true", help="print JSON")
    parser.add_argument("--config", help="config path")
    args = parser.parse_args()

    if not args.keyword and not args.change_id and not args.project:
        parser.print_help()
        sys.exit(1)

    client = GerritSSHClient(args.config)
    if args.change_id:
        change = client.get_change_detail(
            args.change_id,
            include_current_patch_set=True,
            include_patch_sets=args.patch_sets,
            include_files=args.files,
            include_comments=args.comments or args.timeline,
            include_all_approvals=args.approvals,
            include_submit_records=args.submit_records,
            include_commit_message=args.commit_message,
        )
        if args.json:
            print(json.dumps(change, indent=2, ensure_ascii=False))
        else:
            query_by_id(
                client,
                args.change_id,
                show_files=args.files,
                show_comments=args.comments,
                show_approvals=args.approvals,
                show_submit_records=args.submit_records,
                show_patch_sets=args.patch_sets,
                show_commit_message=args.commit_message,
                show_timeline=args.timeline,
            )
        return

    rk_only = not args.all_owners
    if args.json:
        query_parts: List[str] = []
        if args.keyword:
            query_parts.append(args.keyword)
        if args.project:
            query_parts.append(f"project:{args.project}")
        if args.branch:
            query_parts.append(f"branch:{args.branch}")
        if args.status:
            query_parts.append(f"status:{args.status}")
        if rk_only:
            query_parts.append("owner:rock-chips.com")
        query = " ".join(query_parts) if query_parts else "status:open"
        print(json.dumps(client.search_changes(query, limit=args.limit), indent=2, ensure_ascii=False))
    else:
        search_by_keyword(client, args.keyword, args.limit, args.project, args.branch, args.status, rk_only)


if __name__ == "__main__":
    main()
