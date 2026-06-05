# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spendly** — a personal expense tracker for the Indian market (₹ currency). This is a step-by-step teaching project where the scaffold (design, routing shell, templates) is provided and students implement the backend in numbered steps.

## Commands

```bash
# Activate virtual environment (Windows)
venv\Scripts\activate

# Run the development server
python app.py
# App runs at http://localhost:5001

# Run tests
pytest

# Run a single test file
pytest tests/test_auth.py

# Install dependencies
pip install -r requirements.txt
```

## Architecture

**Stack:** Flask 3.1.3 + Jinja2 templates, SQLite (not yet connected), vanilla CSS/JS, pytest + pytest-flask.

**Key files:**
- `app.py` — all routes; currently stubs for most handlers
- `database/db.py` — placeholder; students implement `get_db()`, `init_db()`, `seed_db()`
- `templates/base.html` — shared layout with navbar/footer; all pages extend this
- `static/css/style.css` — full design system using CSS variables; warm editorial aesthetic (cream/dark ink/deep green `#1a472a`)
- `static/js/main.js` — empty placeholder

**Template blocks:** `title`, `head`, `content`, `scripts`

## Planned Implementation Steps (student tasks)

1. `database/db.py` — SQLite connection with `row_factory`, foreign keys enabled, `CREATE TABLE IF NOT EXISTS` schema, seed data
2. POST `/register` — user registration handler
3. POST `/login` + GET `/logout` — auth with Flask sessions
4. GET `/profile` — user profile page
5–6. GET `/dashboard` + `/expenses` — listing pages
7. GET/POST `/expenses/add` — create expense
8. GET/POST `/expenses/<id>/edit` — update expense
9. POST `/expenses/<id>/delete` — delete expense

## Design Constraints

- Currency is always ₹ (Indian Rupees)
- Responsive breakpoint at 900px (single-column below)
- Fonts: DM Serif Display (headings) + DM Sans (body) from Google Fonts
- Do not introduce CSS frameworks — the existing design system in `style.css` is intentional
