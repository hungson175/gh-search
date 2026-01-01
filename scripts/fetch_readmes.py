#!/usr/bin/env python3
"""
Fetch READMEs from GitHub for repositories in the database.
Progressive approach: Start small (10), validate, then scale.
"""

import psycopg2
import urllib.request
import time
import sys
import argparse
from datetime import datetime

# Database connection
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'postgres',
    'database': 'github_projects'
}

def fetch_readme_from_github(owner: str, repo_name: str) -> tuple[str, str]:
    """
    Fetch README from GitHub, trying multiple branch names.

    Returns: (readme_content, branch_used) or (None, None) if not found
    """
    # Extract just repo name if full path given
    if '/' in repo_name:
        repo_name = repo_name.split('/')[-1]

    branches = ['main', 'master']

    for branch in branches:
        try:
            url = f'https://raw.githubusercontent.com/{owner}/{repo_name}/{branch}/README.md'
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (gh-search README fetcher)')

            with urllib.request.urlopen(req, timeout=10) as response:
                readme = response.read().decode('utf-8', errors='ignore')
                return readme, branch
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue  # Try next branch
            else:
                print(f"  HTTP Error {e.code} for {owner}/{repo_name} on {branch}")
                continue
        except Exception as e:
            print(f"  Error fetching {owner}/{repo_name} on {branch}: {e}")
            continue

    return None, None

def update_readme_in_db(repo_name: str, readme_text: str, branch_used: str):
    """Store README in database."""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE github_repositories
            SET readme_text = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE repo_name = %s
        """, (readme_text, repo_name))

        conn.commit()
        return True
    except Exception as e:
        print(f"  DB Error updating {repo_name}: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def mark_readme_failed(repo_name: str):
    """Mark repo as having no README (don't retry)."""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        # Store empty string to indicate we tried and failed
        cursor.execute("""
            UPDATE github_repositories
            SET readme_text = '',
                updated_at = CURRENT_TIMESTAMP
            WHERE repo_name = %s
        """, (repo_name,))

        conn.commit()
        return True
    except Exception as e:
        print(f"  DB Error marking failed {repo_name}: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def get_repos_without_readmes(limit: int):
    """Get repos that need README fetching."""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT repo_name, owner, stars
            FROM github_repositories
            WHERE readme_text IS NULL
            ORDER BY stars DESC
            LIMIT %s
        """, (limit,))

        repos = cursor.fetchall()
        return repos
    finally:
        cursor.close()
        conn.close()

def get_stats():
    """Get current README fetching statistics."""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                COUNT(*) as total,
                COUNT(*) FILTER (WHERE readme_text IS NOT NULL AND readme_text != '') as fetched,
                COUNT(*) FILTER (WHERE readme_text = '') as failed,
                COUNT(*) FILTER (WHERE readme_text IS NULL) as pending
            FROM github_repositories
        """)

        total, fetched, failed, pending = cursor.fetchone()
        return {
            'total': total,
            'fetched': fetched,
            'failed': failed,
            'pending': pending
        }
    finally:
        cursor.close()
        conn.close()

def fetch_readmes_batch(limit: int, delay: float = 1.0):
    """
    Fetch READMEs for a batch of repos.

    Args:
        limit: Number of repos to process
        delay: Delay between requests (seconds) to be nice to GitHub
    """
    print(f"\n{'='*80}")
    print(f"README Fetching Session - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")

    # Get initial stats
    stats = get_stats()
    print(f"Initial Status:")
    print(f"  Total repos:    {stats['total']:,}")
    print(f"  Already fetched: {stats['fetched']:,}")
    print(f"  Failed (no README): {stats['failed']:,}")
    print(f"  Pending:        {stats['pending']:,}")
    print(f"\nFetching {limit} READMEs...\n")

    # Get repos to process
    repos = get_repos_without_readmes(limit)

    if not repos:
        print("✅ No repos to process!")
        return

    success_count = 0
    fail_count = 0
    start_time = time.time()

    for idx, (repo_name, owner, stars) in enumerate(repos, 1):
        print(f"[{idx}/{len(repos)}] {repo_name} ({stars:,} ⭐)")

        # Fetch README
        readme, branch = fetch_readme_from_github(owner, repo_name)

        if readme and len(readme) > 50:  # Valid README (>50 chars)
            if update_readme_in_db(repo_name, readme, branch):
                print(f"  ✅ Fetched {len(readme):,} chars from {branch}")
                success_count += 1
            else:
                print(f"  ❌ Failed to save to database")
                fail_count += 1
        else:
            # No README found
            print(f"  ⚠️  No README found")
            mark_readme_failed(repo_name)
            fail_count += 1

        # Rate limiting - be nice to GitHub
        if idx < len(repos):  # Don't sleep after last one
            time.sleep(delay)

    # Final stats
    elapsed = time.time() - start_time
    final_stats = get_stats()

    print(f"\n{'='*80}")
    print(f"Batch Complete!")
    print(f"{'='*80}")
    print(f"Results:")
    print(f"  ✅ Successfully fetched: {success_count}")
    print(f"  ⚠️  No README found:     {fail_count}")
    print(f"  ⏱️  Time elapsed:        {elapsed:.1f}s ({elapsed/60:.1f} min)")
    print(f"  ⚡ Rate:               {len(repos)/elapsed:.2f} repos/sec")
    print(f"\nDatabase Status:")
    print(f"  Total repos:    {final_stats['total']:,}")
    print(f"  With README:    {final_stats['fetched']:,} ({final_stats['fetched']/final_stats['total']*100:.1f}%)")
    print(f"  No README:      {final_stats['failed']:,}")
    print(f"  Pending:        {final_stats['pending']:,}")

    if final_stats['pending'] > 0:
        estimated_time = (final_stats['pending'] / (len(repos) / elapsed)) / 60
        print(f"\nEstimated time for remaining {final_stats['pending']:,} repos: {estimated_time:.1f} minutes")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch READMEs from GitHub')
    parser.add_argument('--limit', type=int, default=10,
                       help='Number of repos to process (default: 10)')
    parser.add_argument('--delay', type=float, default=1.0,
                       help='Delay between requests in seconds (default: 1.0)')

    args = parser.parse_args()

    try:
        fetch_readmes_batch(args.limit, args.delay)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Progress saved to database.")
        print("Run again to resume from where you left off.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
