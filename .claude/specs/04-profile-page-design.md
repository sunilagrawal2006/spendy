# Spec: Profile Page Design

## Overview
This step implements the `GET /profile` route and creates the `profile.html` template. The profile page is the first access-controlled page in Spendly: it redirects unauthenticated visitors to `/login`. For logged-in users it displays their account details (name, email, member-since date) and a brief expense summary (total expenses recorded and total amount spent) drawn from the `expenses` table. This gives students practice reading from both the `users` and `expenses` tables in a single request and passing aggregated data to a template.

## Depends on
- Step 01 — Database setup (`get_db()`, `users` and `expenses` tables)
- Step 02 — Registration (users exist in the database)
- Step 03 — Login and Logout (Flask session with `user_id` is populated on login)

## Routes
- `GET /profile` — renders the user's profile with account info and expense stats — logged-in only (redirect to `/login` if `session["user_id"]` is absent)

## Database changes
No new tables or columns. The route reads from:
- `users` — `name`, `email`, `created_at` filtered by `id = session["user_id"]`
- `expenses` — `COUNT(*)` and `SUM(amount)` filtered by `user_id = session["user_id"]`

## Templates
- **Create:** `templates/profile.html` — full profile page extending `base.html`
- **Modify:** none

## Files to change
- `app.py` — replace the `/profile` stub with a real handler

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never use string formatting in SQL
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- If `session.get("user_id")` is falsy, do `redirect(url_for("login"))` immediately — do not read the DB first
- Look up the user by `session["user_id"]` from the database, not from `session["user_name"]`, so the page always shows fresh data
- If `SUM(amount)` returns `None` (user has no expenses), default it to `0` before passing to the template
- Format currency as ₹ in the template, not in Python
- The profile template must display: name, email, member-since (formatted from `created_at`), total expense count, total amount spent

## Definition of done
- [ ] Visiting `/profile` when not logged in redirects to `/login`
- [ ] Visiting `/profile` when logged in renders the page without errors
- [ ] Page shows the logged-in user's name and email
- [ ] Page shows the member-since date derived from `users.created_at`
- [ ] Page shows the correct total number of expenses for that user
- [ ] Page shows the correct total amount spent (₹-prefixed) for that user
- [ ] Page renders correctly when the user has zero expenses (no crashes, shows ₹0)
- [ ] App starts without errors (`python app.py`)
