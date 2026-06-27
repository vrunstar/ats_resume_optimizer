# ATS Resume Optimizer

A resume optimization web app with a React frontend and FastAPI backend.
The app analyzes resume text or uploaded PDF/DOCX files against a job description and returns ATS-relevant feedback, keyword matching, and formatting suggestions.

## Project structure

- `backend/` - Python FastAPI backend
- `frontend/` - React + Vite frontend
- `ats/` - Python virtual environment for the backend

## Requirements

- Python 3.12+ (or the version used by `ats/`)
- Node.js 18+ / npm

## Backend setup

1. Activate the Python virtual environment:
   - Windows PowerShell: `.ackend\..\ats\Scripts\Activate.ps1`
   - Windows CMD: `.ackend\..\ats\Scripts\activate.bat`

2. Install backend dependencies:
   ```powershell
   pip install -r backend\requirements.txt
   ```

3. Create a `.env` file in `backend/` with values:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_MODEL=gemini-2.5-flash
   ALLOWED_ORIGINS=http://localhost:5173
   ```

4. Start the backend server:
   ```powershell
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Frontend setup

1. Install frontend dependencies:
   ```powershell
   cd frontend
   npm install
   ```

2. Start the frontend dev server:
   ```powershell
   npm run dev
   ```

3. Open the app in your browser at `http://localhost:5173`

## Notes

- The frontend proxy is configured in `frontend/vite.config.js` to forward `/analyse` requests to `http://localhost:8000`.
- The backend requires the `GEMINI_API_KEY` environment variable and uses the `fastapi` server.
- Resume uploads are handled via multipart form data in `frontend/src/api.js`.

## Useful files

- `backend/main.py` - FastAPI endpoint implementation
- `backend/src/config.py` - environment config and Gemini API settings
- `frontend/src/api.js` - client API request logic
- `frontend/package.json` - frontend dependencies and scripts
- `frontend/vite.config.js` - Vite server and proxy config
