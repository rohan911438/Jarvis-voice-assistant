import openai

# Set the new API key
openai.api_key = "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"

# Define the conversation history
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello! How are you?"},
]

# Make the request to the API for a chat completion using the gpt-3.5-turbo model
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # Use the newer model
    messages=messages,       # Include the conversation history
    max_tokens=150,          # Limit the length of the response
    temperature=0.7          # Control creativity of the response
)

# Extract and print the assistant's response from the completion
assistant_response = completion['choices'][0]['message']['content']
print(assistant_response)
