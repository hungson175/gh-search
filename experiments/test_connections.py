#!/usr/bin/env python3
"""Test connections to PostgreSQL and Qdrant"""

import sys

def test_qdrant():
    """Test Qdrant connection"""
    try:
        from qdrant_client import QdrantClient

        client = QdrantClient(url="http://localhost:6333")
        collections = client.get_collections()

        print("✓ Qdrant connection successful!")
        print(f"  Collections found: {len(collections.collections)}")

        for collection in collections.collections:
            info = client.get_collection(collection.name)
            print(f"  - {collection.name}: {info.points_count} points, "
                  f"vector size: {info.config.params.vectors.size}")

        return True
    except ImportError:
        print("✗ qdrant-client not installed. Run: pip install qdrant-client")
        return False
    except Exception as e:
        print(f"✗ Qdrant connection failed: {e}")
        return False

def test_postgresql():
    """Test PostgreSQL connection"""
    try:
        import psycopg2

        # Try default PostgreSQL port first
        ports = [5432, 5433, 5434]

        for port in ports:
            try:
                conn = psycopg2.connect(
                    host="localhost",
                    port=port,
                    user="postgres",
                    password="postgres",
                    database="postgres"
                )

                cursor = conn.cursor()
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]

                cursor.execute("SELECT datname FROM pg_database;")
                databases = [row[0] for row in cursor.fetchall()]

                print(f"✓ PostgreSQL connection successful on port {port}!")
                print(f"  Version: {version.split(',')[0]}")
                print(f"  Databases: {', '.join(databases[:5])}")

                # Check for github_projects database
                if "github_projects" in databases:
                    print("  ✓ github_projects database found!")
                else:
                    print("  ⚠ github_projects database not found")

                cursor.close()
                conn.close()
                return True

            except psycopg2.OperationalError:
                continue

        print("✗ Could not connect to PostgreSQL on any port (5432, 5433, 5434)")
        return False

    except ImportError:
        print("✗ psycopg2 not installed. Run: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"✗ PostgreSQL connection failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Database Connections")
    print("=" * 60)
    print()

    print("1. Testing Qdrant:")
    print("-" * 60)
    qdrant_ok = test_qdrant()
    print()

    print("2. Testing PostgreSQL:")
    print("-" * 60)
    postgres_ok = test_postgresql()
    print()

    print("=" * 60)
    if qdrant_ok and postgres_ok:
        print("✓ All connections successful!")
        sys.exit(0)
    else:
        print("✗ Some connections failed. Install missing packages:")
        print("  pip install qdrant-client psycopg2-binary")
        sys.exit(1)
