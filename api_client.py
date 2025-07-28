import os
import requests

BASE_URL = "https://basirah-project.onrender.com"

def get_tafsir(author, surah, ayah, lang="ar"):
    url = f"{BASE_URL}/tafsir/{author}/{surah}/{ayah}"
    response = requests.get(url, params={"lang": lang})
    return response.json() if response.ok else {"error": response.text}

def get_reflection(author, surah, from_ayah, to_ayah, lang="en"):
    url = f"{BASE_URL}/reflect"
    response = requests.get(url, params={
        "author": author,
        "surah": surah,
        "from_ayah": from_ayah,
        "to_ayah": to_ayah,
        "lang": lang
    })
    return response.json() if response.ok else {"error": response.text}

def search_topic(query, author=None, surah=None, lang="ar", top_k=5):
    url = f"{BASE_URL}/tafsir/topic"
    params = {
        "q": query,
        "lang": lang,
        "top_k": top_k
    }
    if author:
        params["author"] = author
    if surah:
        params["surah"] = surah
    response = requests.get(url, params=params)
    return response.json() if response.ok else {"error": response.text}
