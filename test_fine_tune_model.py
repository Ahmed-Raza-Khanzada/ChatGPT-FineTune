from flask import Flask, request, jsonify
import openai
from bs4 import BeautifulSoup
from api_credentials import api_key,model_id

app = Flask(__name__)
openai.api_key = api_key  # Be cautious with your API keys!

def clean_html(message):
    soup = BeautifulSoup(message, 'html.parser')
    text = soup.get_text()
    return text

def chat_with_fine_tuned_model(messages):
    response = openai.ChatCompletion.create(
        model=model_id,  # Replace with your fine-tuned model ID
        messages=messages
    )
    reply = response['choices'][0]['message']['content']
    return reply

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Extract message from POST request
        data = request.json
        message = clean_html(data["message"])
        message = " ".join(message.split("\u00a0"))

        # Prepare messages for ChatGPT
        messages = [
            {"role": "system", "content": "You are an assistant from staff that responds to user queries:"},
            {"role": "user", "content": message}
        ]

        # Get response from ChatGPT
        response = chat_with_fine_tuned_model(messages)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host = "0.0.0.0",port =5000 , debug=True)
