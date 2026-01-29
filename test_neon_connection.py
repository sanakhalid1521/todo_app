#!/usr/bin/env python3
"""
Simple script to test Neon database connection
"""

import asyncio
import os
from dotenv import load_dotenv
import asyncpg

# Load environment variables
load_dotenv()

async def test_neon_connection():
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("ERROR: DATABASE_URL not found in environment!")
        return False

    print(f"Testing connection to: {database_url}")

    try:
        # Connect to the database
        conn = await asyncpg.connect(database_url)

        # Test the connection with a simple query
        version = await conn.fetchval("SELECT version();")
        print(f"SUCCESS: Connected! Database version: {version}")

        # Test creating and querying a simple table to verify full functionality
        await conn.execute("""
            CREATE TEMPORARY TABLE test_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)

        # Insert a test record
        await conn.execute(
            "INSERT INTO test_table (name) VALUES ($1);",
            "Neon Connection Test"
        )

        # Query the record back
        result = await conn.fetchrow("SELECT * FROM test_table WHERE name = $1;", "Neon Connection Test")

        if result:
            print(f"SUCCESS: Database write/read test successful! ID: {result['id']}, Name: {result['name']}")
        else:
            print("ERROR: Database write/read test failed!")
            return False

        # Close the connection
        await conn.close()
        print("Connection closed.")

        return True

    except Exception as e:
        print(f"ERROR: Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Neon Database Connection...")
    success = asyncio.run(test_neon_connection())

    if success:
        print("\nNeon database connection is working properly!")
    else:
        print("\nNeon database connection failed!")
        exit(1)