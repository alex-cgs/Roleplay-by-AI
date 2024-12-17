import openai

# Replace this with your OpenAI API key
openai.api_key = ""

# List available models
try:
    models = openai.models.list()
    for model in models.data:
        print(model.id)
except Exception as e:
    print(f"Error listing models: {e}")
