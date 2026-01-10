#!/usr/bin/env python3
"""Test script to run the backend server."""

import asyncio
from main import app
import uvicorn

if __name__ == "__main__":
    print("Starting backend server on http://0.0.0.0:8000")
    print("Press Ctrl+C to stop the server")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False  # Disable reload to avoid multiprocessing issues
    )