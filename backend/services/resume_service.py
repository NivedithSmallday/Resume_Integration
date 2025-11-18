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
