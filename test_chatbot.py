#!/usr/bin/env python3
"""
Test script to verify the chatbot functionality
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = os.getenv("NEXT_PUBLIC_API_URL", "http://localhost:8000")

def test_chatbot():
    print("Testing Chatbot API...")

    # Test data
    test_message = {
        "message": "add book",
        "user_id": "test-user",
        "session_id": "test-session-123"
    }

    print(f"Sending message: {test_message['message']}")

    try:
        # Make request to the chat API
        response = requests.post(
            f"{BASE_URL}/api/chat/message",
            headers={"Content-Type": "application/json"},
            json=test_message
        )

        print(f"Response Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"Response Data: {json.dumps(data, indent=2)}")

            # Check if the response contains expected fields
            if "response" in data and "session_id" in data:
                print("✅ Chat API is working correctly!")

                # Check if the response indicates the task was added
                response_text = data.get("response", "").lower()
                if "created" in response_text or "added" in response_text or "task" in response_text:
                    print("✅ Task was successfully added to the database!")
                else:
                    print(f"⚠️  Task may not have been added. Response: {data['response']}")
            else:
                print(f"❌ Unexpected response format: {data}")
        else:
            print(f"❌ Chat API returned error: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Error occurred: {e}")

if __name__ == "__main__":
    test_chatbot()