# Project Notes

## Gemini free-tier quota optimization

The workflow intentionally limits LLM calls so the three-chapter assessment can run on a low free-tier request-per-minute limit:

- 1 Planner call for the book outline
- 1 Researcher call for research packets for all chapters
- 3 Writer calls (one per chapter)
- 3 Editor calls (one per chapter)
- 3 Fact-checker calls (one per chapter)
- At most 3 additional Writer/Editor/Fact-checker calls for one revision per chapter

The Researcher fetches public web pages directly with HTTP requests and then uses one LLM call to organize the evidence. A failed fact-check reuses the existing research packet instead of calling the Researcher again.

The Gemini client spaces requests using `GEMINI_MIN_REQUEST_INTERVAL` (default 5 seconds) to reduce burst rate-limit failures.

## Important

Demo mode is only for workflow testing. Do not submit demo citations as research evidence.
