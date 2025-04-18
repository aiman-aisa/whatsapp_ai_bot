import os
from flask import Flask, request
from dotenv import load_dotenv
from openai import OpenAI

# Load .env variables
load_dotenv()

# OpenRouter endpoint
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

app = Flask(__name__)

@app.route("/bot", methods=["POST"])
def bot():
    user_message = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')
    
    print(f"Received message from {sender}: {user_message}")  # Log it

    # Create OpenAI response
    try:
        response = client.chat.completions.create(
            model="thudm/glm-z1-32b:free",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Error: {str(e)}"
        
    print(f"Replying: {reply}")
    return reply

if __name__ == "__main__":
    from os import environ
    port = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
