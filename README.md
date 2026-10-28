# RADIX Talent Match

AI-assisted candidate-readiness and job skill-matching foundation for the RADIX Talent Match Hackathon 2026.

## Project overview

This repository is the integrated foundation for a candidate-readiness portal. It provides a React and Vite frontend, a FastAPI backend, shared sample-data folders, and local development configuration. The five required business modules are planned but not implemented in this foundation stage.

## Planned modules

1. **JD Analytics** - Analyze job-description requirements.
2. **Resume Parsing** - Convert resumes into structured candidate data.
3. **Profile Builder** - Assemble candidate readiness profiles.
4. **Talent Check** - Evaluate strengths, gaps, and readiness signals.
5. **Skill Matching** - Match candidates to roles using verified skill evidence.

## Unified frontend

The canonical frontend is the premium React + TypeScript RADIX Talent Intelligence Workspace in `frontend/`. It preserves the existing sidebar, landing experience, typography, navigation, and responsive workspace styling.

`frontend/legacy-jsx/` retains the earlier JSX implementation for reference. It is not the active frontend and is not required to run the project.

The fully API-backed business module is Job Intelligence at `/workspace/jobs`. Resume parsing, profile persistence, Talent Check, and Skill Matching now have local FastAPI endpoints. The workspace screens still contain illustrative/demo workflows and are not all wired to those new endpoints yet. Company, Roadmap, and History routes remain illustrative.

## Technology stack

- **Frontend:** React, TypeScript, Vite, React Router
- **Backend:** Python, FastAPI, Uvicorn
- **Local ports:** React `5173`, FastAPI `8000`
- **Package management:** npm and pip
- **Local persistence:** SQLite for candidate profiles and generated reports
- **Future hosted persistence:** Supabase schema migration is prepared; credentials, auth, and repository integration are still required

## Folder structure

```text
radix-talent-match/
├── backend/
│   ├── .env.example
│   ├── main.py
│   └── requirements.txt
├── data/
│   ├── company_skillsets/
│   ├── sample_jds/
│   └── sample_resumes/
├── frontend/
│   ├── src/
│   ├── .env.example
│   ├── index.html
│   └── package.json
├── tests/
├── .gitignore
└── README.md
```

Empty shared directories contain `.gitkeep` files. Private candidate resumes should never be placed in Git; add private uploads to a local `.gitignore` location or an appropriately secured store.

## Windows PowerShell setup

From the repository root:

```powershell
cd C:\Users\Lenovo\Downloads\Projects\radix-talent-match

py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt

cd frontend
npm install
cd ..
```

If PowerShell blocks virtual-environment activation, open a PowerShell window where your execution policy permits it and run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Start the backend

From the repository root, after activating `.venv`:

```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

## Start the frontend

In a second PowerShell window, start exactly one canonical frontend:

```powershell
cd C:\Users\Lenovo\Downloads\Projects\radix-talent-match\frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

Use `http://127.0.0.1:5173/workspace/jobs` for the live unified JD Analytics experience. Do not also start the external prototype or another Vite process on 5173/5174.

## Verify the API

With the backend running, open:

```text
http://127.0.0.1:8000/api/health
```

Expected JSON:

```json
{
  "status": "ok",
  "service": "radix-talent-match-api",
  "version": "0.1.0"
}
```

FastAPI also provides interactive API documentation at `http://127.0.0.1:8000/docs`.

## Verify frontend-backend communication

1. Start the backend on port `8000`.
2. Start the frontend on port `5173`.
3. Open the frontend.
4. Confirm the status shows **Connected** and identifies the API service and version.

If the backend is unavailable, the page shows a useful error instead of reporting a false connection. The request uses `http://127.0.0.1:8000/api/health` and FastAPI permits local requests from both Vite origins.

## JD Analytics

The existing interface includes a working JD Analytics workspace. It can:

- list sample job descriptions from `data/sample_jds/`
- load a selected sample
- analyze pasted text
- show the detected title and company
- extract experience, education, responsibilities, technical skills, and soft skills
- group curated technical skills under the 12 RADIX categories
- preserve unsupported terms separately under `unmatched_skills`

### API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | API health and version |
| `GET` | `/api/jd-analytics/samples` | List available sample JDs |
| `GET` | `/api/jd-analytics/samples/{sample_id}` | Retrieve a sample JD |
| `POST` | `/api/jd-analytics/analyze` | Analyze submitted JD text |
| `POST` | `/api/resumes/parse` | Parse a PDF, DOCX, or TXT resume into a review-required draft |
| `POST` | `/api/resumes/parse-text` | Parse pasted resume text into a review-required draft |
| `PUT` | `/api/profiles/{profile_id}` | Save a candidate profile locally |
| `GET` | `/api/profiles/{profile_id}` | Retrieve a saved profile |
| `POST` | `/api/talent-checks` | Check saved profile completeness (not credential verification) |
| `POST` | `/api/skill-matches` | Compare saved profile skills with a supplied job description |
| `GET` | `/api/talent-checks/{report_id}` | Retrieve a saved Talent Check report |
| `GET` | `/api/skill-matches/{report_id}` | Retrieve a saved skill-match report |

The analyze endpoint accepts:

```json
{ "text": "Raw job description text" }
```

### Skill extraction

JD Analytics uses a deterministic, curated keyword dictionary in `backend/jd_parser.py`. Aliases are matched with word boundaries to reduce obvious substring false positives. Skills are grouped using these RADIX categories:

- COD - Coding
- DSA - Data Structures and Algorithms
- OOD - Object-Oriented Design
- APTI - Aptitude
- COMM - Communication
- AI - Artificial Intelligence
- CLOUD - Cloud
- SQL - SQL and Databases
- SWE - Software Engineering
- SYSD - System Design
- NETW - Networking
- OS - Operating Systems
- OTHER - Reserved for unmatched skills

The mentor CSV in `data/mentor_framework/` contains company-specific skill expectations. Its suffix codes and scores are not parsed or interpreted as job requirements, and the CSV is not used to derive JD analysis results.

## Verify JD Analytics

Install backend test dependencies and run the focused test module:

```powershell
python -m pip install -r backend\requirements-dev.txt
python -m pytest tests\test_jd_analytics.py -q
```

Start the backend and frontend in separate terminals:

```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

```powershell
cd frontend
npm run dev
```

Verify these URLs:

- `http://127.0.0.1:8000/api/jd-analytics/samples`
- `http://127.0.0.1:8000/api/jd-analytics/samples/backend_engineer`
- `http://127.0.0.1:8000/docs`
- `http://localhost:5173`

The frontend should list both sample JDs, load one into the text area, and display real structured results after Analyze is selected.

## JD Analytics limitations

- Extraction is deterministic and approximate, not AI-generated inference.
- Missing title, company, experience, or education fields are reported as empty or `Not identified` rather than invented.
- Responsibilities are extracted from recognized responsibility headings and may be incomplete for unstructured JDs.
- Unknown terms are heuristic and can include ordinary prose despite the filtering.
- The mentor framework is reference data; its company expectations are not job requirements.
- Resume parsing uses deterministic keyword extraction, not AI inference; all extracted fields need candidate review.
- Talent Check checks completeness only. It does not verify candidate identity, education, or skill claims.
- Skill Matching uses the curated keyword list and exact canonical skill names; it does not assess proficiency or infer equivalent skills.
- The new profile/report endpoints use local SQLite and do not yet use Supabase or authentication.
- No real API keys or credentials are included.

## Local profile and matching workflows

The local backend stores profile JSON and analysis reports in `data/radix-local.sqlite3` by default. Override the location with `RADIX_DATABASE_PATH`. Resume files are parsed in memory and are not saved by the API. Do not use this unauthenticated local API with private candidate data on a shared or public network.

Install the updated backend dependencies and run both backend suites:

```powershell
python -m pip install -r backend\requirements-dev.txt
python -m pytest tests -q
```

The typed frontend client for these endpoints is in `frontend/src/workflowApi.ts`. Resume upload/review, Talent Check, and Skill Matching now call the local API; their pre-existing illustrative panels remain visible for comparison. Profile edits are held in browser demo state and are sent to the local API when a check or match runs.

## Supabase setup status

`supabase/migrations/202610280001_talent_match_core.sql` prepares private candidate-profile/report tables with Row Level Security and a private `resumes` Storage bucket. It is not applied automatically and the local SQLite repository does not connect to Supabase. To activate hosted storage, create a Supabase project, apply the migration, configure the backend credentials, implement authenticated user ownership in the backend repository, and then switch the frontend workflows to the authenticated API. Never place the Supabase service-role key in a `VITE_` variable or browser code.
