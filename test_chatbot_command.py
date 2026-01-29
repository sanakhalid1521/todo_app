import requests
import json

# Test the chatbot API directly
def test_add_book():
    url = "http://127.0.0.1:8001/api/chat/message"

    payload = {
        "message": "add book",
        "user_id": "test-user",
        "session_id": "test-session-123"
    }

    headers = {
        'Content-Type': 'application/json'
    }

    print("Testing 'add book' command...")
    print(f"Sending request to: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, headers=headers, json=payload)

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")

        if response.status_code == 200:
            response_data = response.json()
            print(f"Response Data: {json.dumps(response_data, indent=2)}")

            if "response" in response_data:
                print(f"\n✅ SUCCESS: Chatbot responded with: '{response_data['response']}'")

                # Check if it indicates the task was added
                response_text = response_data['response'].lower()
                if "created" in response_text or "added" in response_text or "task" in response_text:
                    print("✅ The 'add book' command was processed successfully!")
                else:
                    print("⚠️  Command processed but may not have added a task")
            else:
                print("❌ Response doesn't contain expected 'response' field")
        else:
            print(f"ERROR: Request failed with status {response.status_code}")
            print(f"Response Text: {response.text}")

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the server. Is it running on http://127.0.0.1:8001?")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    test_add_book()