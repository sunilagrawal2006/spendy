# Spec: Login and Logout

## Overview
This step wires up POST `/login` and GET `/logout` so registered users can authenticate and end their session. The GET `/login` route and `login.html` template already exist; the work here is the form-submission handler, session management, and the logout action. On successful login the user's `id` and `name` are stored in the Flask session and they are redirected to `/dashboard`. On failure the login form is re-rendered with an error message. Logout clears the session and redirects to the landing page.

## Depends on
- Step 01 — Database setup (`get_db()`, `users` table)
- Step 02 — Registration (users exist in the database to log in with)

## Routes
- `POST /login` — validates credentials, sets session, redirects to `/dashboard` — public
- `GET /logout` — clears the session, redirects to `/` — logged-in (no hard guard needed yet)

## Database changes
No database changes. The existing `users` table with `id`, `name`, `email`, and `password_hash` columns is sufficient.

## Templates
- **Create:** none — `login.html` already renders `{{ error }}` and POSTs to `/login`
- **Modify:** none

## Files to change
- `app.py`
  - Add `session` to the Flask import
  - Add `check_password_hash` to the werkzeug import
  - Add `methods=["GET", "POST"]` to the `/login` route decorator
  - Implement the POST branch: look up user by email, verify password, set `session["user_id"]` and `session["user_name"]`, redirect to `/dashboard`
  - On any error, re-render `login.html` with `error=<message>`
  - Implement `GET /logout`: call `session.clear()`, redirect to `/`
  - Add a stub `GET /dashboard` route that returns `"Dashboard — coming in Step 5"` (if it does not already exist)

## Files to create
None.

## New dependencies
No new pip packages.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never use string formatting in SQL
- Passwords verified with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Session keys to set on login: `session["user_id"]` (integer), `session["user_name"]` (string)
- Validation order: email blank → "Email is required", password blank → "Password is required", no user found OR password wrong → "Invalid email or password" (same message for both — do not reveal which field is wrong)
- On any validation error re-render `login.html` with `error=<message>`; do not redirect
- On success: set session, then `redirect(url_for("dashboard"))`
- Logout must call `session.clear()` (not just `session.pop`), then `redirect(url_for("landing"))`

## Definition of done
- [ ] Submitting valid credentials sets `session["user_id"]` and `session["user_name"]` and redirects to `/dashboard`
- [ ] Leaving email blank shows "Email is required" on the login form
- [ ] Leaving password blank shows "Password is required" on the login form
- [ ] Entering a wrong email or wrong password shows "Invalid email or password"
- [ ] After logout, visiting `/dashboard` no longer shows a logged-in session (verified by checking the session is empty)
- [ ] `/logout` redirects to the landing page `/`
- [ ] The demo user (`demo@spendly.com` / `demo123`) can log in successfully
- [ ] App starts without errors
