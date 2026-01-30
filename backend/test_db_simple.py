#!/usr/bin/env python3
"""
Test script to verify database connection and table creation.
"""

import asyncio
import sys
import os
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
            expected_tables = ['tasks', 'users']
            for table in expected_tables:
                if table in table_names:
                    print(f"✓ '{table}' table exists")
                else:
                    print(f"✗ '{table}' table does not exist")

        print("\nDatabase test completed successfully!")
        return True

    except Exception as e:
        print(f"Database test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_db_connection())
    sys.exit(0 if success else 1)