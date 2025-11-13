from dotenv import load_dotenv
import time
import os

from models.resume_data import ResumeData
from services.email_service import EmailService
from services.resume_service import ResumeService
from core.db import ResumeDB
from repositories.resume_repository import ResumeRepository
from api.routes import notify
from core.extractor import extract_text_from_file, ResumeExtractor

POLL_INTERVAL = 60  # check mails every 60s
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")

def ensure_public_dir():
    if not os.path.exists(PUBLIC_DIR):
        os.makedirs(PUBLIC_DIR)

def main():
    load_dotenv()
    ensure_public_dir()
    db = ResumeDB()
    resume_repo = ResumeRepository(db.db_connection)
    email_service = EmailService()
    extract = ResumeExtractor()
    resume_service = ResumeService(resume_repo)

    while True:
        print("🔄 Checking for new emails...")
        try:
            emails = email_service.fetch_emails()
            for email in emails:
                try:
                    if email.get("hasAttachments"):
                        attachments = email_service.download_attachments(email["id"])
                        for file in attachments:
                            # Save the file to the public directory
                            src_path = file['filename']
                            dest_path = os.path.join(PUBLIC_DIR, os.path.basename(src_path))
                            if not os.path.exists(dest_path):
                                # If file is not already in public, copy/move it
                                try:
                                    os.rename(src_path, dest_path)
                                except Exception:
                                    import shutil
                                    shutil.copy(src_path, dest_path)
                            file_path = dest_path
                            text = extract_text_from_file(file_path)
                            resume_dict = extract.extract(text)
                            resume_dict["resume_file"] =  os.path.basename(file_path)  # Add file path to dict
                            resume_data = ResumeData.from_dict(resume_dict)
                            if not resume_repo.exists_by_email_or_phone(resume_data.email, resume_data.phone):
                                new_resume_id = resume_repo.save(resume_data)
                                if new_resume_id:
                                    notify(str(new_resume_id))
                except Exception as e:
                    print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()