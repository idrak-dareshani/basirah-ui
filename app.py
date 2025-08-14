import streamlit as st
import json
from api_client import (
    login_user, logout_user,
    get_tafsir, get_reflection, search_topic
)

# -----------------------
# Load Surah and Quran data
# -----------------------
with open("surah.json", encoding="utf-8") as f:
    surah_data = json.load(f)

with open("quran.json", encoding="utf-8") as f:
    quran_data = json.load(f)

# Author Mapping
authors = {
    "alaloosi": "Al Alusi", "alrazi": "Al Razi", "ibn-aashoor": "Ibn Ashur",
    "ibn-katheer": "Ibn Kathir", "qurtubi": "Al Qurtubi", "tabari": "Al Tabari"
}

# Language Mapping
languages = {
    "ar": "العربية", "en": "English", "fr": "Français", "de": "Deutsch", "es": "Spanish", "ur": "اردو"
}

# Surah and Ayah Mappings
surahs = {s['surah_number']: s['surah_name'] for s in surah_data['surahs']}
total_ayah_map = {s['surah_number']: s['total_ayat'] for s in surah_data['surahs']}

# -----------------------
# Helpers
# -----------------------
def get_ayah_text(surah_num, ayah_num):
    surah = quran_data.get(f"{surah_num}")
    ayah = surah.get(f"{ayah_num}")
    return f"{surah_num}:{ayah_num} {ayah.get('arabic')}"

# -----------------------
# Page Config & Styling
# -----------------------
st.set_page_config(layout="wide", page_title="Basirah - Quranic Insights", page_icon="📖", initial_sidebar_state="collapsed")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <style>
            
        /* Remove top padding from main content */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 1rem;
        }
            
        /* Arabic Text Styles */
        .arabic-text {
            font-family: 'Amiri', serif;
            font-size: 22px;
            direction: rtl;
            text-align: right;
            margin-bottom: 1rem;
            line-height: 1.8;
            color: #2c3e50;
        }
        
        .arabic-subheading {
            font-family: 'Amiri', serif;
            font-size: 24px;
            font-weight: 600;
            direction: rtl;
            text-align: right;
            margin-bottom: 1rem;
            color: #2d3748;
        }
            
        /* Urdu Text Styles */
        .urdu-text {
            font-family: 'Noto Nastaliq Urdu', serif;
            font-size: 20px;
            direction: rtl;
            text-align: right;
            margin-bottom: 1rem;
            line-height: 2;
            color: #2c3e50;
        }
            
        /* English Text Styles */
        .english-text {
            font-family: 'Inter', sans-serif;
            font-size: 16px;
            direction: ltr;
            text-align: left;
            margin-bottom: 1rem;
            line-height: 1.6;
            color: #2c3e50;
            font-weight: 400;
        }            
    </style>
""", unsafe_allow_html=True)

# -----------------------
# Login Screen
# -----------------------
def login_screen():
    st.title("🔐 Login to Basirah - Quranic Insights")
    with st.form("login_form", enter_to_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if login_user(username, password):
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Login failed. Please check your credentials.")

# -----------------------
# Main Application
# -----------------------
def main_app():
    st.sidebar.header("🧭 Navigation")
    if st.sidebar.button("Logout"):
        logout_user()
        st.rerun()

    option = st.sidebar.radio("Choose Feature", ["📘 View Tafsir", "💡 Reflection", "🔍 Topic Search"])

    if option == "📘 View Tafsir":
        st.subheader("View Tafsir by Author, Surah, and Ayah")
    
        surah_number = st.selectbox("Surah", list(surahs.keys()), format_func=lambda x: f"{x}. {surahs[x]}")
        with st.form("tafsir_form", border=False):
            max_ayah = total_ayah_map.get(surah_number, 286)
            ayah = st.selectbox("Ayah", list(range(1, max_ayah + 1)))
            author_key = st.selectbox("Select Author", list(authors.keys()), format_func=lambda x: authors[x])
            lang = st.selectbox("Language", list(languages.keys()), format_func=lambda x: languages[x])
            submitted = st.form_submit_button("Get Tafsir")

        if submitted:
            with st.spinner("Fetching tafsir..."):
                result = get_tafsir(author_key, surah_number, ayah, lang)
            if "error" in result:
                st.error(result["error"])
            else:
                ayah_text = get_ayah_text(surah_number, ayah)
                st.markdown(f"<div class='arabic-subheading'>{ayah_text}</div>", unsafe_allow_html=True)
                if lang == "ar":
                    st.markdown(f"<div class='arabic-text'>{result['tafsir_text']}</div>", unsafe_allow_html=True)
                elif lang == "ur":
                    st.markdown(f"<div class='urdu-text'>{result['tafsir_text']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='english-text'>{result['tafsir_text']}</div>", unsafe_allow_html=True)
                    #st.markdown(result["tafsir_text"])

    elif option == "💡 Reflection":
        st.subheader("Generate a Reflection")

        surah_number = st.selectbox("Surah", list(surahs.keys()), format_func=lambda x: f"{x}. {surahs[x]}")
        max_ayah = total_ayah_map.get(surah_number, 286)

        col1, col2 = st.columns(2)
        with col1:
            from_ayah = st.selectbox("From Ayah", list(range(1, max_ayah + 1)))
        with col2:
            to_ayah = st.selectbox("To Ayah", list(range(from_ayah, max_ayah + 1)))

        with st.form("reflection_form", border=False):
            author_key = st.selectbox("Select Author", list(authors.keys()), format_func=lambda x: authors[x])
            lang = st.selectbox("Language", list(languages.keys()), format_func=lambda x: languages[x])
            submitted = st.form_submit_button("Generate Reflection")

        if submitted:
            with st.spinner("Generating reflection..."):
                result = get_reflection(author_key, surah_number, from_ayah, to_ayah, lang)
            if "error" in result:
                st.error(result["error"])
            else:
                for ayah in range(from_ayah, to_ayah + 1):
                    ayah_text = get_ayah_text(surah_number, ayah)
                    st.markdown(f"<div class='arabic-subheading'>{ayah_text}</div>", unsafe_allow_html=True)
                st.markdown(f"### ✨ Reflection for Surah {surah_number}: Ayah {from_ayah} - {to_ayah}")
                if lang == "ar":
                    st.markdown(f"<div class='arabic-text'>{result['reflection']}</div>", unsafe_allow_html=True)
                elif lang == "ur":
                    st.markdown(f"<div class='urdu-text'>{result['reflection']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='english-text'>{result['reflection']}</div>", unsafe_allow_html=True)
                    #st.markdown(result["reflection"])

    elif option == "🔍 Topic Search":
        st.subheader("Search Tafsir by Topic")
        with st.form("topic_form", border=False):
            query = st.text_input("Enter topic or phrase")
            author_key = st.selectbox("Filter by Author (optional)", ["", *authors.keys()], format_func=lambda x: authors[x] if x else "All Authors")
            surah_number = st.selectbox("Filter by Surah (optional)", [0] + list(surahs.keys()), format_func=lambda x: f"{x}. {surahs.get(x, '')}" if x else "All Surahs")
            lang = st.selectbox("Language", list(languages.keys()), format_func=lambda x: languages[x])
            top_k = st.slider("Number of Results", 1, 10, 3)
            submitted = st.form_submit_button("Search")

        if submitted and query:
            with st.spinner("Searching topic..."):
                selected_author = author_key if author_key else None
                selected_surah = surah_number if surah_number > 0 else None
                result = search_topic(query, selected_author, selected_surah, lang, top_k)
            if "error" in result:
                st.error(result["error"])
            else:
                for r in result["results"]:
                    ayah_text = get_ayah_text(r["surah"], int(r["ayah_range"][0]))
                    surah_name = surahs.get(int(r["surah"]))
                    with st.expander(f"Surah {r['surah']} ({surah_name}) - Ayah {r['ayah_range'][0]} | Score: {round(r['score'], 3)}"):
                        st.markdown(f"<div class='arabic-subheading'>{ayah_text}</div>", unsafe_allow_html=True)
                        st.markdown(f"**Author:** {r['author']}")
                        if lang == "ar":
                            st.markdown(f"<div class='arabic-text'>{r['text']}</div>", unsafe_allow_html=True)
                        elif lang == "ur":
                            st.markdown(f"<div class='urdu-text'>{r['translated_text']}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='english-text'>{r['translated_text']}</div>", unsafe_allow_html=True)
                            #st.markdown(f"{r['translated_text']}")

# -----------------------
# Run
# -----------------------
if "token" not in st.session_state:
    login_screen()
else:
    main_app()

# --- Footer Disclaimer ---
st.markdown("""
---
**Disclaimer:**  
Translations may contain errors or omissions. Reflections are generated by AI and may not represent scholarly or authoritative interpretations. If you notice any inaccuracies or potentially misleading content, please email **idrak.dareshani@basirah-ai.com** with a brief description or a screenshot.
""")