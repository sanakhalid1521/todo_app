#!/usr/bin/env python3
"""
Test script to verify database connection and table creation.
"""

import asyncio
import sys
from sqlalchemy import inspect
from app.database import init_db, async_engine
from sqlmodel import SQLModel


async def test_db_connection():
    """Test database connection and table creation."""
    try:
        print("Testing database connection...")

        # Initialize the database (create tables)
        await init_db()
        print("✓ Database tables initialized successfully")

        # Check if tables exist
        async with async_engine.begin() as conn:
            # Get table names
            table_names = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
            print(f"Tables in database: {table_names}")

            # Check for specific tables
            if 'tasks' in table_names:
                print("✓ 'tasks' table exists")
            else:
                print("✗ 'tasks' table does not exist")

            if 'users' in table_names:
                print("✓ 'users' table exists")
            else:
                print("✗ 'users' table does not exist")

        print("\nDatabase test completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_db_connection())
    sys.exit(0 if success else 1)