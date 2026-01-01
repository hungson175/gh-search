#!/usr/bin/env python3
"""Check status of background README fetching."""

import psycopg2
from datetime import datetime
import os
import sys

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'postgres',
    'database': 'github_projects'
}

def get_stats():
    """Get current stats."""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) as total,
            COUNT(*) FILTER (WHERE readme_text IS NOT NULL AND readme_text != '') as fetched,
            COUNT(*) FILTER (WHERE readme_text = '') as failed,
            COUNT(*) FILTER (WHERE readme_text IS NULL) as pending
        FROM github_repositories
    """)

    total, fetched, failed, pending = cursor.fetchone()
    cursor.close()
    conn.close()

    return {
        'total': total,
        'fetched': fetched,
        'failed': failed,
        'pending': pending
    }

def check_process():
    """Check if background process is running."""
    pid_file = "logs/readme_fetch.pid"
    if not os.path.exists(pid_file):
        return None

    with open(pid_file) as f:
        pid = int(f.read().strip())

    try:
        os.kill(pid, 0)  # Check if process exists
        return pid
    except OSError:
        return None

def estimate_completion(stats, avg_rate=1.74):
    """Estimate time to completion."""
    remaining = stats['pending']
    if remaining == 0:
        return "Complete!"

    # avg_rate is seconds per repo (from Phase 1 results)
    seconds = remaining * avg_rate
    hours = seconds / 3600

    if hours < 1:
        return f"{seconds/60:.1f} minutes"
    else:
        return f"{hours:.1f} hours"

if __name__ == '__main__':
    print("=" * 80)
    print(f"README Fetch Status - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()

    # Check if process running
    pid = check_process()
    if pid:
        print(f"✅ Background process RUNNING (PID: {pid})")
    else:
        print(f"⚠️  Background process NOT running")
    print()

    # Get stats
    stats = get_stats()

    print("Database Status:")
    print(f"  Total repos:    {stats['total']:,}")
    print(f"  With README:    {stats['fetched']:,} ({stats['fetched']/stats['total']*100:.1f}%)")
    print(f"  No README:      {stats['failed']:,}")
    print(f"  Pending:        {stats['pending']:,}")
    print()

    # ETA
    if stats['pending'] > 0:
        eta = estimate_completion(stats)
        print(f"Estimated time to completion: {eta}")
        print()

    # Recent log
    log_file = "logs/readme_fetch.log"
    if os.path.exists(log_file):
        print("Recent log (last 10 lines):")
        print("-" * 80)
        os.system(f"tail -n 10 {log_file}")
