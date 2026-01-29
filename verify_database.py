#!/usr/bin/env python3
"""
Script to verify database connection and chatbot functionality
"""

import asyncio
import os
from dotenv import load_dotenv
from backend.database import test_connection, init_db, get_async_session
from backend.app.models.task import Task
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

# Load environment variables
load_dotenv()

async def verify_database():
    print("🔍 Verifying database connection...")

    # Test the connection
    success = await test_connection()
    if not success:
        print("❌ Database connection failed!")
        return False

    print("✅ Database connection successful!")

    # Initialize database tables
    print("\n🔧 Initializing database tables...")
    try:
        await init_db()
        print("✅ Database tables initialized!")
    except Exception as e:
        print(f"❌ Failed to initialize database tables: {e}")
        return False

    # Test basic operations
    print("\n🧪 Testing basic database operations...")
    try:
        # Test creating a session and querying
        async for session in get_async_session():
            # Test that we can query tasks (even if none exist)
            statement = select(Task)
            result = await session.execute(statement)
            tasks = result.scalars().all()
            print(f"✅ Successfully queried tasks. Found {len(tasks)} tasks.")

            # Close session properly
            await session.close()

    except Exception as e:
        print(f"❌ Database operation test failed: {e}")
        return False

    print("\n🎉 Database verification completed successfully!")
    print("💡 The chatbot should now work properly with database operations.")

    return True

if __name__ == "__main__":
    print("🚀 Starting database verification...")
    success = asyncio.run(verify_database())

    if success:
        print("\n✅ All systems ready! The chatbot should work properly.")
    else:
        print("\n❌ Issues found! Please check the errors above and fix them.")
        exit(1)