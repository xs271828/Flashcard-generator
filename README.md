# 📚 AI Flashcard Generator

A reading flashcard tool powered by the DeepSeek API. Paste text or upload a PDF, enter keywords, and get AI-generated Q&A flashcards instantly. Supports both English and Chinese.

## Features

- Paste text or upload a PDF as reading material
- Enter keywords and let AI generate question-answer pairs
- Supports English and Chinese content
- Enter your API Key in the sidebar — no code changes needed

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

Once running, enter your DeepSeek API Key in the sidebar (get one at [platform.deepseek.com](https://platform.deepseek.com)), then:

1. Choose input method: paste text or upload a PDF
2. Enter keywords (comma-separated)
3. Click "Generate Flashcards"

## Dependencies

| Package | Purpose |
|---|---|
| streamlit | Web interface |
| openai | DeepSeek API calls |
| pymupdf | PDF text extraction |
