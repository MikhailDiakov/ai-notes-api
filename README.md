# AI NOTES API

- **Startup**

  ```
    git clone <repository URL>
    cd <project directory>
    cp .env.example .env
    docker-compose up -d
  ```

- **Utilize** 'http://localhost/docs'

# Notes Analytics

This script analyzes the content of notes stored in a database, providing insights into word count and frequency.

## Features

- **Total Notes**: Total number of notes in the database.
- **Total Word Count**: Cumulative word count across all notes.
- **Average Note Length**: Average word count per note.
- **Most Common Words**: Top 10 most frequent words in all notes.
- **Longest Notes**: IDs of the 3 longest notes (by word count).
- **Shortest Notes**: IDs of the 3 shortest notes (by word count)

# Text Summarization with Gemini AI

This script summarizes the provided text using the **Gemini AI API**.

## Features

- **Summarize Text**: Takes input text and returns a summary.

## Requirements

- Change GEMINI_API_KEY to the actual API from (https://aistudio.google.com/prompts/new_chat).

# Testing

- **Pytest**:
  ```
  docker-compose --profile test up
  ```
  or in the “fastapi_app” docker container.
- Pytest will also show a coverage of around 99%.
