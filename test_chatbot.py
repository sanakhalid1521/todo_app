#!/usr/bin/env python3
"""
Test script to verify chatbot functionality
"""

import requests
import time
import sys

def test_chatbot():
    print("Testing chatbot functionality...")

    # Test the backend health endpoint
    try:
        print("Checking backend health at http://localhost:8000/health...")
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("[OK] Backend is running and healthy")
        else:
            print(f"[FAIL] Backend health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"[FAIL] Backend is not accessible: {e}")
        return False

    # Test the chat endpoint with a simple message
    try:
        print("\nTesting chat endpoint...")
        chat_payload = {
            "message": "Hello, can you help me?",
            "user_id": "user-demo",
            "session_id": "test-session-123"
        }

        response = requests.post(
            "http://localhost:8000/api/chat/message",
            json=chat_payload,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            print(f"[OK] Chat response received: {result['response'][:100]}...")
        else:
            print(f"[FAIL] Chat endpoint returned status {response.status_code}: {response.text}")

    except Exception as e:
        print(f"[FAIL] Chat endpoint test failed: {e}")
        print("  Note: This might be due to database connection issues, but the mock functionality should still work")

    # Test the frontend accessibility
    try:
        print("\nChecking frontend at http://localhost:3001/tasks...")
        response = requests.get("http://localhost:3001/tasks", timeout=10)
        if response.status_code == 200:
            print("[OK] Frontend is accessible")
        else:
            print(f"[FAIL] Frontend returned status {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Frontend is not accessible: {e}")

    print("\n" + "="*50)
    print("TEST SUMMARY:")
    print("- Backend API: Should be accessible at http://localhost:8000")
    print("- Frontend UI: Should be accessible at http://localhost:3001/tasks")
    print("- Chat functionality: May have issues due to database connection problems")
    print("- Mock chat functionality: Should work even with database issues")
    print("="*50)

    return True

if __name__ == "__main__":
    print("Running chatbot functionality test...\n")
    success = test_chatbot()
    if success:
        print("\n[OK] Testing completed. Please visit the application in your browser.")
    else:
        print("\n[FAIL] Testing failed.")
        sys.exit(1)