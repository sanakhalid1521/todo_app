#!/usr/bin/env python3
"""
Diagnostic script to check chatbot and database configuration
"""

import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔍 Diagnostic Report")
print("="*50)

# Check environment variables
print("📋 Environment Variables:")
print(f"  DATABASE_URL: {'SET' if os.getenv('DATABASE_URL') else 'NOT SET'}")
print(f"  OPENAI_API_KEY: {'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET (will use mock responses)'}")
print(f"  BETTER_AUTH_SECRET: {'SET' if os.getenv('BETTER_AUTH_SECRET') else 'NOT SET'}")

database_url = os.getenv('DATABASE_URL')
if database_url:
    print(f"\n  Actual DATABASE_URL: {database_url[:50]}..." if len(database_url) > 50 else f"\n  Actual DATABASE_URL: {database_url}")

print("\n🔧 Checking database configuration...")

# Import and test database
try:
    from backend.database import test_connection
    print("  ✅ Database module imported successfully")

    print("\n📡 Testing database connection...")
    success = asyncio.run(test_connection())

    if success:
        print("  ✅ Database connection successful!")
    else:
        print("  ❌ Database connection failed!")

except Exception as e:
    print(f"  ❌ Error importing or testing database: {e}")

print("\n🤖 Checking AI agent configuration...")

try:
    from backend.app.agents.todo_agent import todo_agent
    print("  ✅ Todo agent imported successfully")
    print(f"  ✅ Has OpenAI API key: {todo_agent.has_api_key}")
    print(f"  ✅ Will use mock responses: {not todo_agent.has_api_key}")

except Exception as e:
    print(f"  ❌ Error importing todo agent: {e}")

print("\n📋 Database URL Analysis:")
if database_url:
    if database_url.startswith("postgresql://"):
        print("  ✅ Using PostgreSQL (Neon) database")
        # Check if it looks like a real Neon URL
        if "ep-" in database_url and "neon.tech" in database_url:
            print("  ✅ Appears to be a valid Neon URL format")
        else:
            print("  ⚠️  URL doesn't look like a standard Neon format")

        # Check if credentials are filled in
        if "username:password@" in database_url:
            print("  ⚠️  Credentials not filled in (still using 'username:password')")
            print("     Please update with your actual Neon credentials")
        else:
            print("  ✅ Credentials appear to be filled in")
    elif database_url.startswith("sqlite:///"):
        print("  ⚠️  Using SQLite database (not Neon)")
    else:
        print(f"  ⚠️  Unknown database type: {database_url}")

print("\n💡 Recommendations:")
print("  1. If using Neon, ensure your DATABASE_URL has real credentials")
print("  2. The format should be: postgresql://your_username:your_password@ep-your_endpoint.region.aws.neon.tech/your_db_name?sslmode=require")
print("  3. If OpenAI key is not set, mock responses will be used")
print("  4. Make sure the database tables are initialized")

print("\n" + "="*50)
print("Diagnostic complete!")