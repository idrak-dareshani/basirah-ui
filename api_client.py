import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

# -----------------------
# Helper: Auth Headers
# -----------------------
def get_headers():
    """Return request headers with JWT token."""
    if "token" not in st.session_state:
        st.error("You must log in first.")
        st.stop()
    return {"Authorization": f"Bearer {st.session_state['token']}"}

# -----------------------
# Auth API Calls
# -----------------------
def login_user(username: str, password: str):
    """Authenticate and store JWT token in session."""
    data = {"username": username, "password": password}
    response = requests.post(f"{API_URL}/token", data=data)
    if response.status_code == 200:
        token = response.json().get("access_token")
        st.session_state["token"] = token
        return True
    return False

def logout_user():
    """Clear JWT token from session."""
    st.session_state.pop("token", None)

# -----------------------
# Tafsir Endpoints
# -----------------------
def get_tafsir(author, surah, ayah, lang="ar"):
    params = {"lang": lang}
    response = requests.get(f"{API_URL}/tafsir/{author}/{surah}/{ayah}", params=params, headers=get_headers())
    return response.json() if response.ok else {"error": response.text}

def get_reflection(author, surah, from_ayah, to_ayah, lang="en"):
    params = {
        "author": author,
        "surah": surah,
        "from_ayah": from_ayah,
        "to_ayah": to_ayah,
        "lang": lang
    }
    response = requests.get(f"{API_URL}/reflect", params=params, headers=get_headers())
    return response.json() if response.ok else {"error": response.text}

def search_topic(query, author=None, surah=None, lang="ar", top_k=5):
    params = {
        "q": query,
        "lang": lang,
        "top_k": top_k
    }
    if author:
        params["author"] = author
    if surah:
        params["surah"] = surah
    response = requests.get(f"{API_URL}/search", params=params, headers=get_headers())
    return response.json() if response.ok else {"error": response.text}
