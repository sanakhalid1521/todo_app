#!/usr/bin/env python3
"""Debug script to check imports."""

try:
    print("Importing main...")
    from main import app
    print("Success: Backend imported successfully")
except Exception as e:
    print(f"Error importing: {e}")
    import traceback
    traceback.print_exc()