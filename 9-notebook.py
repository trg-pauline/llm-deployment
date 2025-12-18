import requests
import json

# Replace with your own endpoint URL
API_URL = "https://your-llm-endpoint.example.com/v1/chat/completions"

# Message to send to the model
user_message = "What is the capital of France?"

# Payload for chat completion
payload = {
    "model": "your-model-name",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_message}
    ],
    "max_tokens": 256,
    "temperature": 0
}

# Request headers
headers = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer YOUR_API_KEY"  # Uncomment if your endpoint requires a token
}

# Send request
response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

# Parse response
if response.status_code == 200:
    result = response.json()
    # Extract answer from chat API response
    answer = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    print("Answer:", answer)
else:
    print(f"Error {response.status_code}: {response.text}")
