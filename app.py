import yt_dlp
import requests
import json
import subprocess  # Fetch Ollama models
from flask import Flask, request, render_template, session, redirect, url_for, jsonify
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"  # For session handling

def get_timedtext_url(video_url, lang="en"):
    """Extracts YouTube subtitle URL dynamically using yt-dlp."""
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': [lang],
        'dump_single_json': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            subtitles = info.get("automatic_captions") or info.get("subtitles")
            
            if subtitles and lang in subtitles:
                return subtitles[lang][0]["url"]
    
    except Exception as e:
        print(f"Error extracting subtitles: {e}")

    return None

def fetch_timedtext_subtitles(timedtext_url):
    """Fetches subtitles from YouTube's timedtext API."""
    try:
        response = requests.get(timedtext_url)
        if response.status_code == 200:
            data = response.json()
            events = data.get("events", [])
            
            subtitles = []
            for event in events:
                if "segs" in event:
                    text = "".join(seg["utf8"] for seg in event["segs"] if "utf8" in seg)
                    subtitles.append(text)
            
            return " ".join(subtitles)  # Combine subtitles into one string
    except Exception as e:
        print(f"Error fetching subtitles: {e}")

    return None

def get_ollama_models():
    """Fetch installed Ollama models from the local system."""
    try:
        output = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        models = [line.split()[0] for line in output.stdout.strip().split("\n") if line]
        return models
    except Exception as e:
        print(f"Error fetching Ollama models: {e}")
        return []

def process_with_langchain(api_key, text, user_request, model, model_name):
    """Processes text using Gemini, OpenAI, or Ollama based on user's choice."""
    try:
        if model == "gemini":
            llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)
        elif model == "openai":
            llm = ChatOpenAI(model_name=model_name, openai_api_key=api_key)
        elif model == "ollama":
            llm = Ollama(model=model_name)
        else:
            return "Invalid model selected."

        prompt = PromptTemplate(
            input_variables=["text", "user_request"],
            template="Based on the following transcript, {user_request}:\n\n{text}"
        )

        chain = LLMChain(llm=llm, prompt=prompt)
        response = chain.run({"text": text, "user_request": user_request})

        return response
    except Exception as e:
        return f"Error processing request: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    if "history" not in session:
        session["history"] = []

    ollama_models = get_ollama_models()  # Fetch installed Ollama models

    if request.method == "POST":
        if "reset" in request.form:
            session.pop("subtitles", None)
            session.pop("video_url", None)
            session["history"] = []
            session.modified = True
            return redirect(url_for("index"))

        user_request = request.form.get("user_request")
        model = request.form.get("model")
        model_name = request.form.get("model_name")

        video_url = request.form.get("video_url")
        if video_url:
            timedtext_url = get_timedtext_url(video_url)
            if not timedtext_url:
                return render_template("index.html", error="Could not extract subtitles. Try another video.", model=model, ollama_models=ollama_models)

            subtitles = fetch_timedtext_subtitles(timedtext_url)
            if not subtitles:
                return render_template("index.html", error="No subtitles found for this video.", model=model, ollama_models=ollama_models)

            session["subtitles"] = subtitles
            session["video_url"] = video_url
            session["history"] = []
            session.modified = True

        if "subtitles" not in session:
            return render_template("index.html", error="Please upload a video first!", model=model, ollama_models=ollama_models)

        api_key = session.get(f"{model}_api_key") if model in ["gemini", "openai"] else None
        if model in ["gemini", "openai"] and not api_key:
            return redirect(url_for("settings"))

        result = process_with_langchain(api_key, session["subtitles"], user_request, model, model_name)

        session["history"].insert(0, {"model": model, "request": user_request, "response": result})
        session.modified = True

        return render_template("index.html", result=result, model=model, history=session["history"], video_url=session.get("video_url"), ollama_models=ollama_models)

    return render_template("index.html", history=session["history"], video_url=session.get("video_url"), ollama_models=ollama_models)

@app.route("/ollama_models")
def ollama_models():
    """Fetch available Ollama models and return as JSON."""
    models = get_ollama_models()
    return jsonify(models=models)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    """Handles API key input for Gemini and OpenAI models."""
    if request.method == "POST":
        model = request.form.get("model")
        api_key = request.form.get("api_key")

        if model in ["gemini", "openai"] and api_key:
            session[f"{model}_api_key"] = api_key
            return redirect(url_for("index"))

    return render_template("settings.html", gemini_api_key=session.get("gemini_api_key"), openai_api_key=session.get("openai_api_key"))

if __name__ == "__main__":
    app.run(debug=True)
