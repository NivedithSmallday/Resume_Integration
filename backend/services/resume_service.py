# from resume_parser import extract_text_from_file
# from utils import is_resume
# from core.extractor import ResumeExtractor
# from api import notify
#
# class ResumeService:
#     def __init__(self, db):
#         self.db = db
#         self.extractor = ResumeExtractor()
#
#     def process_resume(self, file_info: dict):
#         file_path = file_info["filename"]
#
#         if not is_resume(file_path):
#             print(f"📎 Skipped non-resume file: {file_path}")
#             return
#
#         print(f"📄 Processing resume: {file_path}")
#         text = extract_text_from_file(file_path)
#         extracted_data = self.extractor.extract(text)
#
#         # 🚫 Check if resume already exists in DB by email/phone
#         email = extracted_data.get("email")
#         phone = extracted_data.get("phone")
#
#         if self.db.resume_exists(email=email, phone=phone):
#             print(f"⚠️ Duplicate resume skipped (email: {email}, phone: {phone})")
#             return
#
#         resume_id  = self.db.insert_resume(extracted_data)
#         notify(str(resume_id))
#         print("✅ Resume data inserted into DB.")


from typing import Dict, Any
import logging
from repositories.resume_repository import ResumeRepository
from models.resume_data import ResumeData

logger = logging.getLogger(__name__)


class ResumeAlreadyExistsError(Exception):
    """Exception raised when resume already exists"""
    pass


class ResumeService:
    """Service layer for resume operations"""

    def __init__(self, resume_repository: ResumeRepository):
        self.resume_repository = resume_repository

    def create_resume(self, resume_dict: Dict[str, Any], check_duplicates: bool = True) -> int:
        """Create a new resume from dictionary data"""
        resume_data = ResumeData.from_dict(resume_dict)
        #
        # if check_duplicates and self._resume_exists(resume_data):
        #     raise ResumeAlreadyExistsError("Resume with this email or phone already exists")

        return self.resume_repository.save(resume_data)

    def _resume_exists(self, resume_data: ResumeData) -> bool:
        """Check if resume already exists"""
        return self.resume_repository.exists_by_email_or_phone(
            email=resume_data.email,
            phone=resume_data.phone
        )
