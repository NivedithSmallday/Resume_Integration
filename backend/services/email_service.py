import os
# from auth import get_access_token
from api.auth import get_access_token
from mail_fetcher import fetch_emails, download_attachments

class EmailService:
    def __init__(self):
        self.application_id = os.getenv("APPLICATION_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.scopes = ["User.Read", "Mail.Read", "Mail.ReadWrite"]
        self.access_token = get_access_token(self.application_id, self.client_secret, self.scopes)

        # track processed attachment IDs
        self.processed_attachments = set()

    def fetch_emails(self, top=5):
        return fetch_emails(self.access_token, top=top)

    def download_attachments(self, message_id):
        attachments = download_attachments(message_id, self.access_token)
        new_files = []

        for att in attachments:
            att_id = att["id"]  # attachment unique ID
            if att_id in self.processed_attachments:
                continue  # skip already processed

            self.processed_attachments.add(att_id)
            new_files.append(att)

        return new_files
