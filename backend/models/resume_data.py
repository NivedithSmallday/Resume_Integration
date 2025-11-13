from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
import json


@dataclass
class Education:
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    institution: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    cgpa: Optional[float] = None
    percentage: Optional[float] = None


@dataclass
class Experience:
    company: Optional[str] = None
    designation: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    responsibilities: Optional[Union[str, List[str]]] = None

    def get_responsibilities_as_string(self) -> str:
        """Convert responsibilities to string format"""
        if isinstance(self.responsibilities, list):
            return ", ".join(self.responsibilities)
        return self.responsibilities or ""


@dataclass
class ResumeData:
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    career_span: Optional[str] = None
    education: List[Education] = field(default_factory=list)
    experience: List[Experience] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    awards_or_achievements: List[str] = field(default_factory=list)
    resume_file: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ResumeData':
        """Create ResumeData instance from dictionary"""
        # Handle education
        education_data = data.get("education", [])
        if isinstance(education_data, dict):
            education_data = [education_data]

        education_list = []
        for edu in education_data:
            if isinstance(edu, dict):
                education_list.append(Education(**edu))

        # Handle experience
        experience_data = data.get("experience", [])
        experience_list = []
        for exp in experience_data:
            if isinstance(exp, dict):
                experience_list.append(Experience(**exp))

        # Handle skills and awards (normalize to list of strings)
        skills = cls._normalize_to_string_list(data.get("skills", []))
        awards = cls._normalize_to_string_list(data.get("awards_or_achievements", []))

        return cls(
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            linkedin=data.get("linkedin"),
            career_span=data.get("career_span"),
            resume_file=data.get("resume_file"),
            education=education_list,
            experience=experience_list,
            skills=skills,
            awards_or_achievements=awards
        )

    @staticmethod
    def _normalize_to_string_list(items: List[Any]) -> List[str]:
        """Normalize items to list of strings"""
        normalized = []
        for item in items:
            if isinstance(item, (dict, list)):
                normalized.append(json.dumps(item))
            else:
                normalized.append(str(item))
        return normalized