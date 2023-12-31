import openai

# Set your OpenAI API key
api_key = "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"

# Initialize the OpenAI API client
openai.api_key = api_key

# Function to send a message to ChatGPT
def chat_with_gpt(message):
    response = openai.Completion.create(
        engine="text-davinci-002",  # You can choose different engines depending on your use case
        prompt=f"ChatGPT: {message}\nYou:",
        max_tokens=50  # Adjust the number of tokens as needed
    )
    return response.choices[0].text.strip()

# Example usage
user_message = "Tell me about artificial intelligence."
response = chat_with_gpt(user_message)
print(f"User: {user_message}")
print(f"ChatGPT: {response}")
