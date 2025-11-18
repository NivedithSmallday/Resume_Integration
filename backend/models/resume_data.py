from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any, Union
import json
import logging

# -------------------------------------------------------------------
# Logger Setup
# -------------------------------------------------------------------
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


# -------------------------------------------------------------------
# Education Dataclass
# -------------------------------------------------------------------
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


# -------------------------------------------------------------------
# Experience Dataclass
# -------------------------------------------------------------------
@dataclass
class Experience:
    company: Optional[str] = None
    designation: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    responsibilities: Optional[Union[str, List[str]]] = None

    def get_responsibilities_as_string(self) -> str:
        """Convert responsibilities to string format."""
        if isinstance(self.responsibilities, list):
            return ", ".join(self.responsibilities)
        return self.responsibilities or ""


# -------------------------------------------------------------------
# ResumeData Dataclass
# -------------------------------------------------------------------
@dataclass
class ResumeData:
    """Structured data model representing a parsed resume."""
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

    # -------------------------------------------------------------------
    # Factory method: from_dict
    # -------------------------------------------------------------------
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ResumeData':
        """Create ResumeData instance from dictionary."""
        logger.debug("Initializing ResumeData from dict...")

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
        if isinstance(experience_data, dict):
            experience_data = [experience_data]

        experience_list = []
        for exp in experience_data:
            if isinstance(exp, dict):
                experience_list.append(Experience(**exp))

        # Normalize skills & awards
        skills = cls._normalize_to_string_list(data.get("skills", []))
        awards = cls._normalize_to_string_list(data.get("awards_or_achievements", []))

        instance = cls(
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

        logger.info(f"ResumeData created for: {instance.name or 'Unknown Candidate'}")
        return instance

    # -------------------------------------------------------------------
    # Normalization Helper
    # -------------------------------------------------------------------
    @staticmethod
    def _normalize_to_string_list(items: List[Any]) -> List[str]:
        """Normalize items to list of strings."""
        normalized = []
        for item in items:
            if isinstance(item, (dict, list)):
                normalized.append(json.dumps(item))
            else:
                normalized.append(str(item))
        return normalized

    # -------------------------------------------------------------------
    # Utility: Convert to JSON
    # -------------------------------------------------------------------
    def to_json(self, indent: int = 2) -> str:
        """Convert ResumeData object to a JSON string."""
        try:
            json_str = json.dumps(asdict(self), indent=indent, ensure_ascii=False)
            logger.debug(f"Serialized ResumeData to JSON for {self.name or 'Unknown'}")
            return json_str
        except Exception as e:
            logger.error(f"Failed to serialize ResumeData to JSON: {e}")
            raise

    # -------------------------------------------------------------------
    # Utility: Validation
    # -------------------------------------------------------------------
    def validate(self) -> bool:
        """Basic validation for required fields."""
        required = ["name", "email", "phone"]
        missing = [f for f in required if not getattr(self, f)]
        if missing:
            logger.warning(f"Missing required resume fields: {', '.join(missing)}")
            return False
        logger.info(f"ResumeData for {self.name} validated successfully.")
        return True
