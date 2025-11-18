import os

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from core.db import ResumeDB
import asyncio
from typing import Optional, List, Dict, Any
from pymysql.cursors import DictCursor
from fastapi.responses import FileResponse

router = APIRouter()
db = ResumeDB()
subscribers: List[asyncio.Queue] = []
host="http://localhost:5000/"

async def event_generator():
    queue: asyncio.Queue[str] = asyncio.Queue()
    subscribers.append(queue)
    try:
        while True:
            data = await queue.get()
            yield f"data: {data}\n\n"
    finally:
        subscribers.remove(queue)

@router.get("/events")
async def sse_events():
    return StreamingResponse(event_generator(), media_type="text/event-stream")

def notify(message: str):
    for q in subscribers:
        q.put_nowait(message)


@router.get("/resumes")
def get_resumes(search: Optional[str] = Query(None)) -> List[Dict[str, Any]]:
    resumes = []
    with db.db_connection.get_connection() as conn:
        with conn.cursor(DictCursor) as cursor:
            if search:
                query = """
                        SELECT r.*
                        FROM resumes r
                                 LEFT JOIN skills s ON r.id = s.resume_id
                        WHERE r.name LIKE %s
                           OR s.skill LIKE %s
                        GROUP BY r.id \
                        """
                cursor.execute(query, (f"%{search}%", f"%{search}%"))
            else:
                cursor.execute("SELECT * FROM resumes")
            rows = cursor.fetchall()
            for row in rows:
                cursor.execute("SELECT skill FROM skills WHERE resume_id=%s", (row["id"],))
                skills = [s["skill"] for s in cursor.fetchall()]
                # Add resume file path or URL
                resume_file = row.get("resume_file")  # If you store file path in DB
                if resume_file:
                    file = row["resume_file"]
                    resume_url = resume_url = f"{host}/resume/{file}"
                else:
                    resume_url = None
                print(f"Resume URL: {resume_url}")

                print(f"Resume File: {file}")
                resumes.append({
                    "id": row["id"],
                    "name": row["name"],
                    "email": row["email"],
                    "phone": row["phone"],
                    "linkedin": row["linkedin"],
                    "career_span": row["career_span"],
                    "skills": skills,
                    "resume_file": resume_url
                })
    return resumes

@router.post("/resumes")
async def add_resume(resume: dict):
    with db.db_connection.get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO resumes (name, email, phone, linkedin, career_span) VALUES (%s, %s, %s, %s, %s)",
                (resume["name"], resume["email"], resume["phone"], resume["linkedin"], resume["career_span"])
            )
            conn.commit()
            new_resume_id = cursor.lastrowid
            for skill in resume.get("skills", []):
                cursor.execute(
                    "INSERT INTO skills (resume_id, skill) VALUES (%s, %s)",
                    (new_resume_id, skill)
                )
            conn.commit()
    notify(str(new_resume_id))
    return {"id": new_resume_id, "message": "Resume added"}



@router.get("/resumes/{resume_id}/download")
def download_resume(resume_id: int):
    with db.db_connection.get_connection() as conn:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT name, resume_file FROM resumes WHERE id=%s", (resume_id,))
            row = cursor.fetchone()
            if not row or not row["resume_file"]:
                return {"error": "Resume not found"}

            file_path = os.path.join("public", row["resume_file"])  # ✅ build path
            download_name = f"{row['name'].replace(' ', '_')}_Resume.pdf"

            return FileResponse(
                path=file_path,
                filename=download_name,
                media_type="application/pdf"
            )

