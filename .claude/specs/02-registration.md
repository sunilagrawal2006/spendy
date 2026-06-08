# Spec: Registration

## Overview
This step wires up the POST `/register` route so new users can create a Spendly account. The GET route and `register.html` template already exist; the only gap is the form-submission handler. On success the user is inserted into the database with a hashed password and redirected to the login page. On failure the registration form is re-rendered with a clear error message.

## Depends on
- Step 01 — Database setup (`get_db()`, `users` table, `werkzeug` password hashing)

## Routes
- `POST /register` — validates form data, inserts new user, redirects to `/login` — public

## Database changes
No database changes. The `users` table from Step 01 is sufficient:
- `name` TEXT NOT NULL
- `email` TEXT UNIQUE NOT NULL
- `password_hash` TEXT NOT NULL

## Templates
- **Create:** none
- **Modify:** none — `register.html` already renders `{{ error }}` and posts to `/register`

## Files to change
- `app.py` — add POST method to the `/register` route; add `app.secret_key`; import `redirect`, `url_for`, `request` from Flask and `generate_password_hash` from werkzeug

## Files to create
None.

## New dependencies
No new pip packages.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never use string formatting in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Set `app.secret_key` (a hard-coded dev string is fine for now)
- Add `methods=["GET", "POST"]` to the `/register` route decorator
- Keep the existing GET handler intact — only add the POST branch
- Validation order: name blank → "Name is required", email blank → "Email is required", password < 8 chars → "Password must be at least 8 characters", email already taken → "An account with that email already exists"
- On any validation error re-render `register.html` with `error=<message>`; do not redirect
- On success: insert user, then `redirect(url_for("login"))`

## Definition of done
- [ ] Submitting the form with all valid fields creates a new row in `users` with a hashed password
- [ ] Redirects to `/login` after successful registration
- [ ] Leaving name blank shows "Name is required" on the form
- [ ] Leaving email blank shows "Email is required" on the form
- [ ] Entering a password shorter than 8 characters shows "Password must be at least 8 characters"
- [ ] Registering with an already-used email shows "An account with that email already exists"
- [ ] Error messages appear in the `.auth-error` div without a full page reload to a different URL
- [ ] App starts without errors
