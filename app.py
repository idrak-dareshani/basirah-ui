import streamlit as st
import json
from api_client import get_tafsir, get_reflection, search_topic

# Load data
with open("surah.json", encoding="utf-8") as f:
    surah_data = json.load(f)

with open("quran.json", encoding="utf-8") as f:
    quran_data = json.load(f)

# Mappings
authors = {
    "alaloosi": "Al Alusi", "alrazi": "Al Razi", "ibn-aashoor": "Ibn Ashur",
    "ibn-katheer": "Ibn Kathir", "qurtubi": "Al Qurtubi", "tabari": "Al Tabari"
}

languages = {
    "ar": "العربية", "en": "English", "fr": "Français", "de": "Deutsch", "ur": "اردو"
}

surahs = {s['surah_number']: s['surah_name'] for s in surah_data['surahs']}
total_ayah_map = {s['surah_number']: s['total_ayat'] for s in surah_data['surahs']}

# Utilities
def get_ayah_text(surah_num, ayah_num):
    return f"{surah_num}:{ayah_num} {quran_data.get(str(surah_num), {}).get(str(ayah_num), {}).get('arabic', '(Ayah not found)')}"

# Page config
st.set_page_config(layout="wide", page_title="Basirah - Quranic Insights", page_icon="📖", initial_sidebar_state="collapsed")

# Styling
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; padding-bottom: 0rem; }
        .main-title { font-family: 'Inter', sans-serif; font-size: 2.2rem; margin-bottom: 0.2rem; }
        .subtitle { font-size: 1.1rem; color: #555; margin-bottom: 1rem; }
        .arabic-text { font-family: 'Amiri', serif; font-size: 1.4rem; direction: rtl; text-align: right; margin: 1rem 0; }
        .english-text { font-size: 1rem; line-height: 1.6; margin: 1rem 0; }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""<h1 class="main-title">📖 Basirah Project</h1>
<p class="subtitle">Explore Quranic wisdom through classical Tafsir</p>""", unsafe_allow_html=True)

# Navigation
tabs = st.columns(3)
if tabs[0].button("📘 Tafsir", use_container_width=True): st.session_state.active_tab = 'tafsir'
if tabs[1].button("💡 Reflection", use_container_width=True): st.session_state.active_tab = 'reflection'
if tabs[2].button("🔍 Topic Search", use_container_width=True): st.session_state.active_tab = 'search'

st.divider()

# Tafsir Tab
if st.session_state.get('active_tab', 'tafsir') == 'tafsir':
    with st.form("tafsir_form"):
        st.subheader("📘 View Tafsir")
        col1, col2 = st.columns(2)
        with col1:
            author = st.selectbox("Author", list(authors), format_func=lambda x: authors[x])
            surah = st.selectbox("Surah", list(surahs), format_func=lambda x: f"{x}. {surahs[x]}")
        with col2:
            lang = st.selectbox("Language", list(languages), format_func=lambda x: languages[x])
            max_ayah = total_ayah_map.get(surah, 286)
            ayah = st.selectbox("Ayah", range(1, max_ayah + 1))
        submitted = st.form_submit_button("✨ Get Tafsir")

    if submitted:
        with st.spinner("🔍 Fetching tafsir..."):
            result = get_tafsir(author, surah, ayah, lang)
        if "error" in result:
            st.error(f"❌ {result['error']}")
        else:
            st.markdown(f"<div class='arabic-text'>{get_ayah_text(surah, ayah)}</div>", unsafe_allow_html=True)
            st.subheader("📖 Tafsir")
            st.markdown(f"<div class='{'arabic-text' if lang == 'ar' else 'english-text'}'>{result['tafsir_text']}</div>", unsafe_allow_html=True)

# Reflection Tab
elif st.session_state.active_tab == 'reflection':
    with st.form("reflection_form"):
        st.subheader("💡 Generate Reflection")
        col1, col2 = st.columns(2)
        with col1:
            author = st.selectbox("Author", list(authors), format_func=lambda x: authors[x])
            surah = st.selectbox("Surah", list(surahs), format_func=lambda x: f"{x}. {surahs[x]}")
        with col2:
            lang = st.selectbox("Language", list(languages), format_func=lambda x: languages[x])
            max_ayah = total_ayah_map.get(surah, 286)
        col3, col4 = st.columns(2)
        with col3:
            from_ayah = st.selectbox("From Ayah", range(1, max_ayah + 1))
        with col4:
            to_ayah = st.selectbox("To Ayah", range(from_ayah, max_ayah + 1))
        submitted = st.form_submit_button("✨ Generate Reflection")

    if submitted:
        with st.spinner("🤔 Generating reflection..."):
            result = get_reflection(author, surah, from_ayah, to_ayah, lang)
        if "error" in result:
            st.error(f"❌ {result['error']}")
        else:
            st.subheader("📜 Selected Verses")
            for a in range(from_ayah, to_ayah + 1):
                st.markdown(f"<div class='arabic-text'>{get_ayah_text(surah, a)}</div>", unsafe_allow_html=True)
            st.subheader(f"✨ Reflection for Surah {surah}: Ayah {from_ayah}-{to_ayah}")
            st.markdown(f"<div class='english-text'>{result['reflection']}</div>", unsafe_allow_html=True)

# Search Tab
elif st.session_state.active_tab == 'search':
    with st.form("search_form"):
        st.subheader("🔍 Search by Topic")
        query = st.text_input("Topic or keyword", placeholder="e.g., prayer, patience")
        with st.expander("🔧 Filters"):
            col1, col2, col3 = st.columns(3)
            with col1:
                author = st.selectbox("Author", [""] + list(authors), format_func=lambda x: authors.get(x, "All Authors"))
            with col2:
                surah = st.selectbox("Surah", [0] + list(surahs), format_func=lambda x: f"{x}. {surahs.get(x, '')}" if x else "All Surahs")
            with col3:
                lang = st.selectbox("Language", list(languages), format_func=lambda x: languages[x])
            top_k = st.slider("Number of Results", 1, 20, 5)
        submitted = st.form_submit_button("🔍 Search")

    if submitted and query:
        with st.spinner("🔍 Searching..."):
            result = search_topic(query, author or None, surah or None, lang, top_k)
        if "error" in result:
            st.error(f"❌ {result['error']}")
        else:
            st.subheader(f"📊 Results ({len(result['results'])})")
            for i, r in enumerate(result['results'], 1):
                ayah_text = get_ayah_text(r['surah'], int(r['ayah_range'][0]))
                with st.expander(f"#{i} • Surah {r['surah']} - Ayah {r['ayah_range'][0]} • Score: {round(r['score'], 3)}"):
                    st.markdown(f"<div class='arabic-text'>{ayah_text}</div>", unsafe_allow_html=True)
                    st.markdown(f"**📚 Author:** {r['author']}")
                    if lang != "ar":
                        st.markdown(f"<div class='english-text'>{r['translated_text']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='arabic-text'>{r['text']}</div>", unsafe_allow_html=True)
