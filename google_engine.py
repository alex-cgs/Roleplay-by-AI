import requests
import re
import spacy
import subprocess

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm")

API_KEY = "AIzaSyDjKs4P4zVpKjiNEXN750Qp2zVH7Gssuqs"
SEARCH_ENGINE_ID = "9423b21bfcaca4f17" 

def extract_unknown_topics(prompt: str) -> str:

    doc = nlp(prompt)
    topics = set()
    for token in doc:
        if token.pos_ in ["PROPN", "NOUN"] and token.text.lower() not in {"you", "he", "she", "it", "they", "we"}:
            topics.add(token.text)
    return " ".join(topics)

def google_search(query: str, top_n: int = 3) -> list:

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": top_n
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error: Google API returned status code {response.status_code}")
    results = response.json().get("items", [])
    # Extract titles and links from the results
    top_results = [f"{item['title']}: {item['link']}" for item in results]
    return top_results

def process_prompt(prompt: str) -> str:

    print("Current prompt: ", prompt)

    topics = extract_unknown_topics(prompt)
    if not topics:
        return "No significant topics found in the prompt."

    try:
        search_results = google_search(topics)
    except Exception as e:
        return f"Error while performing search: {e}"
 
    response = f"\nIdentified Topics: {topics}\nTop Google Search Results:\n"
    response += "\n".join([f"{i+1}. {result}" for i, result in enumerate(search_results)])
    print(response)
    return response

# Example usage
if __name__ == "__main__":
    prompt = "You are trapped with Nicolas Guelfi in Software Engineering 1, you must master the Messir Methodology, you cannot outsmart him."
    result = process_prompt(prompt)
    print(result)
