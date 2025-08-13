# Basirah UI

A Streamlit-based web application for exploring Quranic insights, including Tafsir, Reflections, and Topic Search, with support for multiple authors and languages.

## Features

- **View Tafsir:** Browse tafsir by author, surah, and ayah.
- **Generate Reflections:** Get AI-generated reflections for selected ayat.
- **Topic Search:** Search tafsir content by topic or phrase.
- **Multi-language Support:** Arabic, English, Urdu, French, German, Spanish.
- **Author Filtering:** Filter tafsir and reflections by classical scholars.

## Project Structure

```
.env                # Environment variables (API keys, etc.)
.gitignore
api_client.py       # Handles API requests to backend services
app.py              # Main Streamlit application
quran.json          # Quranic text data
requiremetns.txt    # Python dependencies
surah.json          # Surah metadata (names, ayah counts)
__pycache__/        # Python bytecode cache
```

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/idrak-dareshani/basirah-ui.git
   cd basirah-ui
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requiremetns.txt
   ```

3. **Configure environment:**
   - Copy `.env.example` to `.env` (if provided) and set required variables (e.g., `API_URL`, authentication tokens).

4. **Run the app:**
   ```sh
   streamlit run app.py
   ```

## Usage

- Log in with your credentials.
- Use the sidebar to navigate between Tafsir, Reflection, and Topic Search.
- Select filters and options as needed, then submit forms to view results.

## Dependencies

- [Streamlit](https://streamlit.io/)
- [Requests](https://docs.python-requests.org/)

## Data Files

- `quran.json`: Contains Quranic text.
- `surah.json`: Contains surah names and ayah counts.

## Notes

- Ensure the backend API is running and accessible at the URL specified in your `.env`.
- For development, update `requiremetns.txt` if you add new dependencies.

---

**License:** MIT