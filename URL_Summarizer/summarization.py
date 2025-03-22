import requests
from bs4 import BeautifulSoup

# API Configuration
OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"

class Website:
    def __init__(self, url):
        self.url = url
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            
            self.title = soup.title.string if soup.title else "No title found"
            
            if soup.body:
                for element in soup.body(["script", "style", "img", "input", "nav", "footer"]):
                    element.decompose()
                self.text = soup.body.get_text(separator="\n", strip=True)
            else:
                self.text = "No content found"
        except requests.exceptions.RequestException as e:
            self.title = "Error"
            self.text = str(e)

def user_prompt_for(website):
    return f"""
    You are looking at a website titled {website.title}.
    The contents of this website are as follows:
    {website.text}
    Please provide a short summary in markdown. If there are news or announcements, summarize them too.
    """

def summarize_website(url):
    """Fetches and summarizes a website using the AI API."""
    website_instance = Website(url)

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": user_prompt_for(website_instance)}],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API, json=payload, headers=HEADERS, timeout=15)
        response.raise_for_status()
        summary = response.json().get("message", {}).get("content", "No summary provided.")
    except requests.exceptions.RequestException as e:
        summary = f"Error: {e}"

    return {"title": website_instance.title, "summary": summary}
