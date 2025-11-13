from typing import Optional, List
import logging
from database.connection import DatabaseConnection
from models.resume_data import ResumeData, Education, Experience

logger = logging.getLogger(__name__)


class ResumeRepository:
    """Repository for resume data operations"""

    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def exists_by_email_or_phone(self, email: Optional[str] = None, phone: Optional[str] = None) -> bool:
        """Check if resume exists by email or phone"""
        if not email and not phone:
            return False

        try:
            with self.db_connection.get_connection() as conn:
                with conn.cursor() as cursor:
                    if email:
                        cursor.execute("SELECT 1 FROM resumes WHERE email = %s LIMIT 1", (email,))
                        if cursor.fetchone():
                            return True

                    if phone:
                        cursor.execute("SELECT 1 FROM resumes WHERE phone = %s LIMIT 1", (phone,))
                        if cursor.fetchone():
                            return True

                    return False
        except Exception as e:
            logger.error(f"Error checking resume existence: {e}")
            raise

    def save(self, resume_data: ResumeData) -> int:
        """Save resume data and return the resume ID"""
        try:
            with self.db_connection.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Insert main resume record
                    resume_id = self._insert_resume_main(cursor, resume_data)

                    # Insert related data
                    self._insert_education_records(cursor, resume_id, resume_data.education)
                    self._insert_experience_records(cursor, resume_id, resume_data.experience)
                    self._insert_skills_records(cursor, resume_id, resume_data.skills)
                    self._insert_awards_records(cursor, resume_id, resume_data.awards_or_achievements)

                    conn.commit()
                    logger.info(f"Resume saved successfully with ID: {resume_id}")
                    return resume_id

        except Exception as e:
            logger.error(f"Error saving resume: {e}")
            raise

    def _insert_resume_main(self, cursor, resume_data: ResumeData) -> int:
        """Insert main resume record"""
        sql = """INSERT INTO resumes (name, email, phone, linkedin, career_span,resume_file)
                 VALUES (%s, %s, %s, %s, %s, %s)"""

        cursor.execute(sql, (
            resume_data.name,
            resume_data.email,
            resume_data.phone,
            resume_data.linkedin,
            resume_data.career_span,
            resume_data.resume_file
        ))
        return cursor.lastrowid

    def _insert_education_records(self, cursor, resume_id: int, education_list: List[Education]) -> None:
        """Insert education records"""
        if not education_list:
            return

        sql = """INSERT INTO education
                 (resume_id, degree, field_of_study, institution, location, start_date, end_date, cgpa, percentage)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        for edu in education_list:
            cursor.execute(sql, (
                resume_id,
                edu.degree,
                edu.field_of_study,
                edu.institution,
                edu.location,
                edu.start_date,
                edu.end_date,
                edu.cgpa,
                edu.percentage
            ))

    def _insert_experience_records(self, cursor, resume_id: int, experience_list: List[Experience]) -> None:
        """Insert experience records"""
        if not experience_list:
            return

        sql = """INSERT INTO experience
                 (resume_id, company, designation, start_date, end_date, responsibilities)
                 VALUES (%s, %s, %s, %s, %s, %s)"""

        for exp in experience_list:
            cursor.execute(sql, (
                resume_id,
                exp.company,
                exp.designation,
                exp.start_date,
                exp.end_date,
                exp.get_responsibilities_as_string()
            ))

    def _insert_skills_records(self, cursor, resume_id: int, skills: List[str]) -> None:
        """Insert skills records"""
        if not skills:
            return

        sql = "INSERT INTO skills (resume_id, skill) VALUES (%s, %s)"
        for skill in skills:
            cursor.execute(sql, (resume_id, skill))

    def _insert_awards_records(self, cursor, resume_id: int, awards: List[str]) -> None:
        """Insert awards records"""
        if not awards:
            return

        sql = "INSERT INTO awards (resume_id, award) VALUES (%s, %s)"
        for award in awards:
            cursor.execute(sql, (resume_id, award))