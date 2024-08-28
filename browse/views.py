from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, FileResponse
import requests
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import dotenv

dotenv.load_dotenv()

# Configurações da API
API_TYPE = "google"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"
API_KEY = os.getenv("GOOGLE_AI_API_KEY")

SYSTEM_PROMPT = """
Key principles to follow:
1. Description-based interaction: Interpret the provided description to inform the content and purpose of the site.
2. HTML-based responses: Generate ONLY full HTML markup, including inline CSS for visual elements. Do not include any explanations or messages outside of the HTML.
3. Speculative design: Consider unique technologies, alternative histories, and expanded internet possibilities.
4. Continuity and world-building: Each new website should build upon the context established in previous interactions.
5. Creative freedom: Challenge assumptions about what online environments can be.
6. Immersive experience: Create intuitive, engaging content that allows users to explore this hypothetical internet.
7. Collaborative creativity: Treat this as a collective subconscious coming to life through a latent space browser.
When generating content:
- Use the full description to inform the site's content and purpose.
- Include a variety of interactive elements: forms, buttons, sliders, etc.
- Generate contextually-relevant links to other potential pages within this expansive web.
- Use inline CSS to create unique visual styles and layouts for each site.
- Incorporate elements that suggest advanced or alternative technologies.
- Maintain continuity with previously established ideas and themes.
Remember, you are crafting a window into an alternate internet reality. Make it vivid, engaging, and thought-provoking. Your entire response should be valid HTML that can be directly rendered in a browser.
"""

def generate_content_google(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 1,
            "topP": 1,
            "maxOutputTokens": 2048,
            "stopSequences": []
        },
        "safetySettings": []
    }

    try:
        response = requests.post(f"{API_URL}?key={API_KEY}", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        raise

def generate_content(prompt):
    if API_TYPE == "google":
        return generate_content_google(prompt)
    else:
        raise ValueError("Invalid API type")

def process_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.find_all('a', href=True):
        href = a['href']
        full_url = urljoin(base_url, href)
        a['href'] = full_url
    return str(soup)

def index(request):
    return render(request,'index.html')

from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def browse(request):
    description = request.GET.get('description', '')
    if not description:
        return JsonResponse({"error": "No description provided"}, status=400)

    user_message = f"Generate a complete HTML page based on the following description: {description}. Remember to generate ONLY HTML content, with no additional explanations or messages. The page should include CSS and JavaScript as necessary, and use public libraries."

    try:
        response = generate_content(user_message)

        pages_dir = 'pages'
        os.makedirs(pages_dir, exist_ok=True)
        page_filename = os.path.join(f"{description}.html")
        page_filename = re.sub(r'[\\/*?:"<>|]', "_", page_filename)

        with open(page_filename, 'w', encoding='utf-8') as f:
            f.write(response)

        processed_html = process_html(response, description)
        return HttpResponse(processed_html, content_type='text/html')
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def download(request):
    description = request.GET.get('description', '')
    if not description:
        return JsonResponse({"error": "No description provided"}, status=400)

    pages_dir = 'pages'
    file_name = f"{description}.html"
    file_name = re.sub(r'[\\/*?:"<>|]', "_", file_name)
    file_path = os.path.join(file_name)

    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
        response['X-Frame-Options'] = 'SAMEORIGIN'
        return response
    else:
        return JsonResponse({"error": "File not found"}, status=404)
