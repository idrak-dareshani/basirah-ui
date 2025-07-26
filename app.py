import streamlit as st
import json
from api_client import get_tafsir, get_reflection, search_topic

# Load Surah and Quran data
with open("surah.json", encoding="utf-8") as f:
    surah_data = json.load(f)

with open("quran.json", encoding="utf-8") as f:
    quran_data = json.load(f)

# Author map
authors = {
    "alaloosi": "Al Alusi",
    "alrazi": "Al Razi",
    "ibn-aashoor": "Ibn Ashur",
    "ibn-katheer": "Ibn Kathir",
    "qurtubi": "Al Qurtubi",
    "tabari": "Al Tabari"
}

# Languages
languages = {
    "ar": "Arabic",
    "en": "English",
    "fr": "French",
    "de": "German",
    "ur": "Urdu"
}

surahs = {s['surah_number']: s['surah_name'] for s in surah_data['surahs']}
total_ayah_map = {s['surah_number']: s['total_ayat'] for s in surah_data['surahs']}

def get_ayah_text(surah_num, ayah_num):
    surah = quran_data.get(str(surah_num))
    if surah:
        ayah = surah.get(str(ayah_num))
        if ayah:
            return f"{surah_num}:{ayah_num} {ayah.get('arabic')}"
    return "(Ayah not found)"

st.set_page_config(layout="wide", page_title="Tafsir System")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Amiri&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
        color: #333;
    }
    .main {background-color: #f9f9f9;}
    .stApp {padding: 2rem;}
    .stSelectbox label, .stNumberInput label, .stTextInput label {
        font-weight: bold;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
    }
    .arabic-text {
        font-family: 'Amiri', serif;
        font-size: 22px;
        direction: rtl;
        text-align: right;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📖 Basirah Project: Explore Qur'anic Insights")

st.sidebar.header("🧭 Navigation")
option = st.sidebar.radio("Choose Feature", ["📘 View Tafsir", "💡 Reflection", "🔍 Topic Search"], key="nav")

if option == "📘 View Tafsir":
    st.subheader("View Tafsir by Author, Surah, and Ayah")
    with st.form("tafsir_form"):
        author_key = st.selectbox("Select Author", list(authors.keys()), format_func=lambda x: authors[x], key="tafsir_author")
        surah_number = st.selectbox("Surah", list(surahs.keys()), format_func=lambda x: f"{x}. {surahs[x]}", key="tafsir_surah")
        max_ayah = total_ayah_map.get(surah_number, 286)
        ayah = st.selectbox("Ayah", list(range(1, max_ayah + 1)), key="tafsir_ayah")
        lang = st.selectbox("Language", list(languages.keys()), format_func=lambda x: languages[x], key="tafsir_lang")
        submitted = st.form_submit_button("Get Tafsir")

    if submitted:
        with st.spinner("Fetching tafsir..."):
            result = get_tafsir(author_key, surah_number, ayah, lang)
        if "error" in result:
            st.error(result["error"])
        else:
            ayah_text = get_ayah_text(surah_number, ayah)
            st.markdown(f"<div class='arabic-text'>{ayah_text}</div>", unsafe_allow_html=True)
            if lang == "ar":
                st.markdown(f"<div class='arabic-text'>{result['tafsir_text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(result["tafsir_text"])

elif option == "💡 Reflection":
    st.subheader("Generate a Reflection")
    with st.form("reflection_form"):
        author_key = st.selectbox("Select Author", list(authors.keys()), format_func=lambda x: authors[x], key="reflect_author")
        surah_number = st.selectbox("Surah", list(surahs.keys()), format_func=lambda x: f"{x}. {surahs[x]}", key="reflect_surah")
        max_ayah = total_ayah_map.get(surah_number, 286)
        col1, col2 = st.columns(2)
        with col1:
            from_ayah = st.selectbox("From Ayah", list(range(1, max_ayah + 1)), key="reflect_from")
        with col2:
            to_ayah = st.selectbox("To Ayah", list(range(from_ayah, max_ayah + 1)), key="reflect_to")
        lang = st.selectbox("Language", list(languages.keys()), format_func=lambda x: languages[x], key="reflect_lang")
        submitted = st.form_submit_button("Generate Reflection")

    if submitted:
        with st.spinner("Generating reflection..."):
            result = get_reflection(author_key, surah_number, from_ayah, to_ayah, lang)
        if "error" in result:
            st.error(result["error"])
        else:
            for ayah in range(from_ayah, to_ayah + 1):
                ayah_text = get_ayah_text(surah_number, ayah)
                st.markdown(f"<div class='arabic-text'>{ayah_text}</div>", unsafe_allow_html=True)
            st.markdown(f"### ✨ Reflection for Surah {surah_number}: Ayah {from_ayah} - {to_ayah}")
            st.markdown(result["reflection"])

elif option == "🔍 Topic Search":
    st.subheader("Search Tafsir by Topic")
    with st.form("topic_form"):
        query = st.text_input("Enter topic or phrase", key="topic_query")
        author_key = st.selectbox("Filter by Author (optional)", ["", *authors.keys()], format_func=lambda x: authors[x] if x else "All Authors", key="topic_author")
        surah_number = st.selectbox("Filter by Surah (optional)", [0] + list(surahs.keys()), format_func=lambda x: f"{x}. {surahs.get(x, '')}" if x else "All Surahs", key="topic_surah")
        lang = st.selectbox("Language", list(languages.keys()), format_func=lambda x: languages[x], key="topic_lang")
        top_k = st.slider("Number of Results", 1, 10, 3, key="topic_topk")
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
                with st.expander(f"Surah {r['surah']} ({r['surah_name_english']}) - Ayah {r['ayah_range'][0]} | Score: {round(r['score'], 3)}"):
                    st.markdown(f"<div class='arabic-text'>{ayah_text}</div>", unsafe_allow_html=True)
                    st.markdown(f"**Author:** {r['author']}")
                    if lang != "ar":
                        st.markdown(r["translated_text"])
                    else:
                        st.markdown(f"<div class='arabic-text'>{r['text']}</div>", unsafe_allow_html=True)
