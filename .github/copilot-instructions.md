This repository is a small Flask-based service (project root files: `app.py`, `requirements.txt`). The codebase is minimal today, so start by inspecting `app.py` and `requirements.txt` for how the application is wired before making changes.

Key facts (discoverable):
- Framework: Flask. See `requirements.txt` for `Flask` and related extensions.
- Persistence: SQLAlchemy / Flask-SQLAlchemy are installed; expect models and DB access to live near the app package or a `models.py` file.
- Auth & forms: `Flask-Login`, `Flask-WTF`, `bcrypt` and `email-validator` indicate form-based auth flows.
- Analytics: `pandas`, `numpy`, `matplotlib`, `seaborn` are present — the project runs data analysis or generates plots server-side.
- Config: `python-dotenv` is listed; the app likely uses environment variables in a `.env` file (look for `os.getenv` or `load_dotenv`).

What to do first (walkthrough for an AI coding agent):
1. Open `app.py` (project entry point). If it's empty or small, search the repo for `create_app`, `Flask(__name__)`, `Blueprint`, `models`, or `db = SQLAlchemy()` to discover the app factory, blueprints and models.
2. Inspect `requirements.txt` to confirm runtime expectations (already present). If adding code, keep dependencies minimal and add to `requirements.txt`.
3. Look for environment-driven configuration: search for `DATABASE_URL`, `SQLALCHEMY_DATABASE_URI`, `FLASK_APP`, or usage of `dotenv`.

Common workflows and exact commands
- Create and activate a venv, install deps:
  - `python -m venv .venv`
  - Windows PowerShell: `.\.venv\Scripts\Activate.ps1` (or `.\.venv\Scripts\activate`)
  - `pip install -r requirements.txt`
- Run locally (development):
  - If the repo exposes `app`/`create_app`: `set FLASK_APP=app.py` then `flask run` (Windows) or `python -m flask run`.
  - If `app.py` has a runnable block: `python app.py`.
- Tests: `pytest` (project includes `pytest` in requirements).
- Production serve (example): `gunicorn app:app` (adjust to the actual app callable or factory wrapper).

Project-specific conventions and patterns to follow
- Keep database configuration in env variables (the presence of `python-dotenv` implies this pattern).
- Prefer an app factory (`create_app`) and blueprints for modularity if you add routes — search the codebase to match existing structure.
- For data-processing endpoints, use clear separation: a service layer or module that returns DataFrame/JSON (example: `services/analytics.py`) rather than embedding heavy logic directly in route handlers.
- Use `Flask-WTF` forms or JSON schemas consistently for endpoints that accept structured input; this repo uses `Flask-WTF` packages.

Integration points to check before editing
- DB: locate where `SQLAlchemy()` is instantiated and how migrations (if any) are handled. No migration tool appears in `requirements.txt`, so be conservative when changing the schema.
- Authentication: check for `login_manager` and user model fields before changing auth flows.
- Long-running data work: endpoints that call pandas/numpy/matplotlib should be reviewed for blocking behavior; consider background tasks for heavy jobs.

When you change the repo
- Update `requirements.txt` when adding new runtime dependencies.
- Add/modify unit tests under `tests/` and run `pytest` locally.
- If you add environment variables, document them in a new `README.md` and provide a sample `.env.example` rather than committing secrets.

Examples from this repo to reference while coding
- Entry point: `app.py` — always open this file first to find the app callable or factory.
- Dependencies: `requirements.txt` — use it to decide runtime imports and test commands.

Guidance on edits an AI agent should follow
- If `app.py` is empty, ask the repository owner before scaffolding a large app layout; offer a minimal patch that implements an app factory and a placeholder route.
- Avoid guessing DB schemas or adding migrations automatically — surface proposed schema changes for review.
- Keep changes minimal and focused: small, test-backed commits are preferred.

If anything here is unclear or you want the instructions tailored (for example: add an app factory scaffolding, add CI, or add tests), tell me which area to expand and I will update this file.
