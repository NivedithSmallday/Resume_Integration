import httpx
import os
from api.auth import MS_GRAPH_BASE_URL
import base64

def fetch_emails(access_token, top=5):
    endpoint = f"{MS_GRAPH_BASE_URL}/me/messages"
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        '$top': top,
        '$select': 'id,subject,isRead,receivedDateTime,from,isDraft,hasAttachments',
        '$orderby': 'receivedDateTime desc'
    }

    response = httpx.get(endpoint, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get('value', [])
# to download_attachments from the email
def download_attachments(message_id, access_token):
    attach_url = f"{MS_GRAPH_BASE_URL}/me/messages/{message_id}/attachments"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = httpx.get(attach_url, headers=headers)
    response.raise_for_status()

    # Ensure public directory exists
    public_dir = os.path.join(os.path.dirname(__file__), "public")
    os.makedirs(public_dir, exist_ok=True)

    saved_files = []
    for att in response.json().get('value', []):
        if att.get("@odata.type") == "#microsoft.graph.fileAttachment":
            filename = att['name']
            content_bytes = att['contentBytes']
            save_path = os.path.join(public_dir, filename)  # Save in public dir
            with open(save_path, "wb") as f:
                f.write(base64.b64decode(content_bytes))
            saved_files.append({
                "id": att["id"],
                "filename": save_path  # Return full path
            })
    return saved_files
