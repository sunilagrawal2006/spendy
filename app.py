from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = "spendly-dev-secret"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name:
        return render_template("register.html", error="Name is required")
    if not email:
        return render_template("register.html", error="Email is required")
    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters")

    conn = get_db()
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        conn.close()
        return render_template("register.html", error="An account with that email already exists")

    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, generate_password_hash(password)),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email:
        return render_template("login.html", error="Email is required")
    if not password:
        return render_template("login.html", error="Password is required")

    conn = get_db()
    user = conn.execute(
        "SELECT id, name, password_hash FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password")

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("dashboard"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/dashboard")
def dashboard():
    return "Dashboard — coming in Step 5"


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    conn = get_db()
    user = conn.execute(
        "SELECT name, email, created_at FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()
    stats = conn.execute(
        "SELECT COUNT(*) AS expense_count, SUM(amount) AS total_spent "
        "FROM expenses WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()
    conn.close()

    if user is None:
        session.clear()
        return redirect(url_for("login"))

    member_since = (user["created_at"] or "")[:10]

    return render_template(
        "profile.html",
        user=user,
        expense_count=stats["expense_count"],
        total_spent=stats["total_spent"] or 0.0,
        member_since=member_since,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


with app.app_context():
    init_db()
    seed_db()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
