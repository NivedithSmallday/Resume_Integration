import os
import time
from dotenv import load_dotenv

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
    """Ensure the public directory exists."""
    if not os.path.exists(PUBLIC_DIR):
        os.makedirs(PUBLIC_DIR)
        print(f"📁 Created public directory at {PUBLIC_DIR}")


def process_attachment(file_info, extract, resume_repo):
    """Extract text from a resume file and save structured data to DB."""
    try:
        src_path = file_info["filename"]
        dest_path = os.path.join(PUBLIC_DIR, os.path.basename(src_path))

        # Move or copy the file to public/
        if not os.path.exists(dest_path):
            try:
                os.rename(src_path, dest_path)
            except Exception:
                import shutil
                shutil.copy(src_path, dest_path)

        file_path = dest_path
        text = extract_text_from_file(file_path)

        if not text.strip():
            print(f"⚠️ No readable text found in {file_path}")
            return

        resume_dict = extract.extract(text)
        resume_dict["resume_file"] = os.path.basename(file_path)

        resume_data = ResumeData.from_dict(resume_dict)

        if not resume_repo.exists_by_email_or_phone(resume_data.email, resume_data.phone):
            new_resume_id = resume_repo.save(resume_data)
            if new_resume_id:
                print(f"✅ New resume saved with ID: {new_resume_id}")
                notify(str(new_resume_id))
        else:
            print(f"ℹ️ Resume already exists for: {resume_data.email or resume_data.phone}")

    except Exception as e:
        print(f"❌ Error processing attachment: {e}")


def main():
    load_dotenv()
    ensure_public_dir()

    db = ResumeDB()
    resume_repo = ResumeRepository(db.db_connection)
    email_service = EmailService()
    extract = ResumeExtractor()
    resume_service = ResumeService(resume_repo)

    print("🚀 Resume Extractor Service Started")

    while True:
        print("\n🔄 Checking for new emails...")
        try:
            emails = email_service.fetch_emails()
            for email in emails:
                try:
                    if email.get("hasAttachments"):
                        attachments = email_service.download_attachments(email["id"])
                        for file_info in attachments:
                            process_attachment(file_info, extract, resume_repo)
                    else:
                        print(f"📭 No attachments found in email: {email.get('subject', 'N/A')}")
                except Exception as e:
                    print(f"⚠️ Error while handling email: {e}")
        except Exception as e:
            print(f"⚠️ Error fetching emails: {e}")

        print(f"⏳ Sleeping for {POLL_INTERVAL} seconds...\n")
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
