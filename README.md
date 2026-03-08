# UPSC PYQ Practice App

A lightweight Streamlit app to practice UPSC Previous Year Questions (PYQs).

## Features
- Filter by `year`, `subject`, and `difficulty`
- Search by question text
- Practice in quiz mode with instant feedback
- Track score in current session
- Bookmark questions for revision

## Run Locally
### Standard commands
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Windows fallback (recommended for this setup)
```powershell
.\run_app.ps1
```

## Project Structure
- `app.py` - Main Streamlit application
- `run_app.ps1` - Windows launcher using the installed Python path
- `data/pyqs.json` - Sample PYQ question bank
- `requirements.txt` - Dependencies

## Notes
- Add more questions by extending `data/pyqs.json`.
- Keep question IDs unique.
