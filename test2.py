import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

# === Load the LLM ===
# Example using GPT-4 or Mistral; modify model_name accordingly
model_name = "mistralai/Mistral-7B-v0.1"  # Replace with "gpt-4" if using OpenAI API
#model_name = "gpt-neo-1.3B"  # Example of a smaller model on Hugging Face

tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="cpu",
    quantization_config=None 
    #load_in_8bit=True
    )

# === Load Sentence Transformer for Retrieval ===
retriever_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# === Prepare FAISS Index ===
# Simulate loading a preprocessed dataset
# Replace with your curated dataset of story passages
stories = [
    "Once upon a time, in a faraway land, there was a brave knight.",
    "Deep in the enchanted forest, a mysterious wizard lived.",
    "The princess found a hidden map to the treasure.",
    "A young boy discovered he could talk to animals."
]
story_embeddings = retriever_model.encode(stories, convert_to_tensor=False)
index = faiss.IndexFlatL2(story_embeddings.shape[1])
index.add(np.array(story_embeddings))

# === Function to Retrieve Context and Generate Story ===
def retrieve_and_generate(prompt):
    # Retrieve relevant passages
    prompt_embedding = retriever_model.encode([prompt], convert_to_tensor=False)
    _, indices = index.search(np.array(prompt_embedding), k=3)  # Retrieve top 3
    retrieved_contexts = " ".join([stories[i] for i in indices[0]])

    # Generate continuation
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)  # Removed `device` argument
    input_with_context = f"{retrieved_contexts} {prompt}"
    story_continuation = generator(
        input_with_context,
        max_length=50, 
        num_return_sequences=1
        )[0]["generated_text"]

    return story_continuation


# === Gradio Interface ===
def storytelling_interface(user_input):
    continuation = retrieve_and_generate(user_input)
    return continuation

# Create Gradio UI
with gr.Blocks() as interface:
    gr.Markdown("## Interactive Storytelling with RAG")
    user_input = gr.Textbox(label="Your Story Prompt")
    output = gr.Textbox(label="Story Continuation")
    submit_button = gr.Button("Generate")
    submit_button.click(storytelling_interface, inputs=user_input, outputs=output)

# Launch Interface
interface.launch()
