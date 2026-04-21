import base64, httpx, os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

load_dotenv()

# The AI model we'll use to describe images
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


# A tool the AI agent can use to find images on a website
@tool
def search_images() -> list[str]:
    """Find and return image URLs from the website set in PICTURES_URL."""
    base_url = os.getenv("PICTURES_URL")
    soup = BeautifulSoup(httpx.get(base_url).text, "html.parser")
    return list(dict.fromkeys(
        urljoin(base_url, img["src"])
        for img in soup.find_all("img") if img.get("src")
    ))[:5]


def image_part(url: str) -> dict:
    """Download an image and convert it to a format the AI understands."""
    image_base64 = base64.b64encode(httpx.get(url).content).decode()
    return {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}


def main() -> list[dict]:
    # Step 1: Give the agent access to the tool and ask it to find images
    agent = model.bind_tools([search_images])
    response = agent.invoke("Find images using the search_images tool")

    # Step 2: Execute the tool call the agent decided to make
    urls = search_images.invoke(response.tool_calls[0]["args"])

    # Step 3: Ask the AI to describe ALL images in a single call
    instruction = {"type": "text", 
                   "text": "Describe each image with bullet points (- Subject: / - Background:). "
                   "Separate each description with ---"}
    reply = model.invoke([HumanMessage(content=[instruction] + [image_part(url) for url in urls])])

    # Step 4: Split the reply and pair each description with its image URL
    descriptions = reply.content.split("---")
    return [{"image": url, "text": desc.strip()} for url, desc in zip(urls, descriptions)]
