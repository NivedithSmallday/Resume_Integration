# Resume Integration System

A production-ready, modular system for automated resume collection, parsing, storage, and dashboard visualization. Built with FastAPI (Python) for the backend and React + Tailwind CSS for the dashboard.

---

## Features

- **Automated Resume Fetching:** Collect resumes from email attachments.
- **Resume Parsing:** Extracts candidate details, education, experience, and skills from PDF/DOCX files.
- **Database Storage:** Saves structured resume data and file paths in a relational database.
- **Real-Time Dashboard:** Responsive UI with live notifications when new resumes are added (no page refresh needed).
- **Resume Viewer:** Click to view resumes directly from the dashboard.
- **Modular Codebase:** Follows SOLID principles for maintainability and scalability.

---

## Project Structure

```
api/                # FastAPI routes and SSE notifications
core/               # Parsing, extraction, and DB logic
models/             # Data models (ResumeData, Education, Experience)
repositories/       # Data access layer
services/           # Business logic (email, resume)
resume-dashboard/   # React frontend (dashboard)
worker.py           # Background worker for email fetching and parsing
main.py             # FastAPI entry point
public/             # Directory for storing resume files
requirements.txt    # Python dependencies
.env.example        # Environment variable template
```

---

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd resume_integration
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Copy `.env.example` to `.env` and fill in your secrets.

4. **Run database migrations**
   - Ensure your database has the correct schema (see `ALTER TABLE` in documentation for `resume_file`).

5. **Start the backend**
   ```bash
   uvicorn main:app --reload
   ```

6. **Start the worker**
   ```bash
   python worker.py
   ```

7. **Start the dashboard**
   ```bash
   cd resume-dashboard
   npm install
   npm start
   ```

---

## Usage

- Access the dashboard at [http://localhost:3000](http://localhost:3000)
- New resumes will appear in real-time with notifications.
- Click "View Resume" to open the resume file.

---

## API Endpoints

- `GET /api/resumes` — List all resumes (with file links)
- `POST /api/resumes` — Add a resume
- `GET /api/events` — Server-Sent Events for real-time updates
- `GET /public/{filename}` — Serve resume files

---

## Contributing

- Fork the repo and submit pull requests.
- Follow modular and SOLID principles for new code.
- Add tests for new features.

---

## License

MIT

---

## Authors

- [Your