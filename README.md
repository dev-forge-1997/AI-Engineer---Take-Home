# Multi-Agent Book Writer

## Project Overview

Multi-Agent Book Writer is a Python application that uses multiple AI agents to research, write, review, and fact-check a book.

It generates a three-chapter book titled **“Pay Me on UPI: How Digital Payments Changed Small Business in India.”** The book is intended for first-time small-business owners in India and explains digital payments in simple, practical language.

## Features

- Uses multiple AI agents for planning, research, writing, editing, and fact-checking.
- Generates a three-chapter book.
- Adds citations and references for factual information.
- Reviews generated content for quality and completeness.
- Provides a Streamlit interface.

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- Pytest

## Installation

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project folder and add your Gemini API key using the environment variable name expected by your code. For example:

   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

   Keep your API key private. Do not upload the `.env` file to GitHub.

## Run the Application

Run the following command:

```bash
streamlit run app.py
```

If your main Python file has a different name, replace `app.py` with that filename.

## Run Tests

If tests are included, run:

```bash
pytest -q
```

## Project Workflow

1. The planner agent creates the book outline.
2. The researcher agent gathers information and sources.
3. The writer agent drafts the chapters.
4. The editor agent reviews clarity and structure.
5. The fact-checking and validation steps review citations and content.

## Notes

- Check that citations and source URLs are valid before submitting the book.
- Review AI-generated content for errors.
- Keep API keys and other secrets out of GitHub.

## Author

Seema Kashyap
