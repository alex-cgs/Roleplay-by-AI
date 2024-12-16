import os
from mistralai import Mistral

def main():
    # Load API key
    api_key = "AYcJkmy5cx0IpkYh4GCUsu4Svy1eTJR5"
    if not api_key:
        print("API key not found! Make sure it's set in the environment.")
        return

    # Initialize Mistral client
    client = Mistral(api_key=api_key)
    model = "mistral-large-latest"

    print("Chatbot is running! Type 'exit' to end the conversation.\n")

    # Store conversation history
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."}  # System message for instructions
    ]

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Add user's input to the conversation history
        conversation.append({"role": "user", "content": user_input})

        try:
            # Send the full conversation history to Mistral
            response = client.chat.complete(
                model=model,
                messages=conversation
            )
            bot_message = response.choices[0].message.content.strip()
            print(f"Bot: {bot_message}")

            # Add bot's response to the conversation history
            conversation.append({"role": "assistant", "content": bot_message})

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
