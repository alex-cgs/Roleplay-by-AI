import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the model and tokenizer
model_name = "mistralai/Mistral-7B-v0.1"  # Replace with your model
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"  # Use GPU if available, fallback to CPU
)

# Define your test prompt
prompt = "Once upon a time, in a magical forest,"

# Tokenize the input
inputs = tokenizer(
    prompt,
    return_tensors="pt",
    padding=True,        # Add padding if required
    truncation=True,     # Ensure the input isn't too long
    max_length=512       # Adjust maximum length as needed
).to("cuda" if torch.cuda.is_available() else "cpu")


# Generate text
output_ids = model.generate(
    inputs.input_ids,
    attention_mask=inputs.attention_mask,  # Include the attention mask
    max_length=50,                        # Adjust this value to your needs
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id   # Ensure an end-of-sequence token
)

generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

# Print the result
print("Generated Story:")
print(generated_text)
