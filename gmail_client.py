import base64
import pickle
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import Config

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailClient:
    def __init__(self):
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        creds = None
        if os.path.exists(Config.GMAIL_TOKEN_FILE):
            with open(Config.GMAIL_TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    Config.GMAIL_CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            with open(Config.GMAIL_TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)

        self.creds = creds
        self.service = build('gmail', 'v1', credentials=creds)

    def get_unread_messages(self, max_results=10):
        """Retrieve unread messages from inbox."""
        result = self.service.users().messages().list(
            userId='me', labelIds=['INBOX'], q='is:unread', maxResults=max_results
        ).execute()
        messages = result.get('messages', [])
        return messages

    def get_message(self, msg_id):
        """Get full message details."""
        msg = self.service.users().messages().get(
            userId='me', id=msg_id, format='full'
        ).execute()
        return msg

    def extract_email_data(self, msg):
        """Extract subject, sender, body from message."""
        headers = msg['payload'].get('headers', [])
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown')
        body = self._get_body(msg)
        return {
            'gmail_message_id': msg['id'],
            'subject': subject,
            'sender': sender,
            'body': body
        }

    def _get_body(self, msg):
        """Extract plain text body from message."""
        parts = [msg['payload']]
        while parts:
            part = parts.pop()
            if part.get('mimeType') == 'text/plain':
                data = part.get('body', {}).get('data')
                if data:
                    return base64.urlsafe_b64decode(data).decode('utf-8')
            if part.get('parts'):
                parts.extend(part['parts'])
        return ''

    def send_reply(self, msg_id, reply_body):
        """Send a reply to the original email."""
        original = self.service.users().messages().get(
            userId='me', id=msg_id, format='metadata',
            metadataHeaders=['Message-ID', 'References']
        ).execute()
        headers = original['payload'].get('headers', [])
        msg_id_header = next((h['value'] for h in headers if h['name'].lower() == 'message-id'), None)
        references = next((h['value'] for h in headers if h['name'].lower() == 'references'), '')

        if msg_id_header:
            references = f"{references} {msg_id_header}".strip()

        # Build reply message
        from_email = Config.GMAIL_USER_EMAIL
        to = self.get_message(msg_id)['payload']['headers'].get('From')
        subject = self.get_message(msg_id)['payload']['headers'].get('Subject', '')
        if not subject.startswith('Re:'):
            subject = f"Re: {subject}"

        raw_message = (
            f"From: {from_email}\r\n"
            f"To: {to}\r\n"
            f"Subject: {subject}\r\n"
            f"In-Reply-To: {msg_id_header}\r\n"
            f"References: {references}\r\n"
            "\r\n"
            f"{reply_body}"
        )

        encoded_message = base64.urlsafe_b64encode(raw_message.encode('utf-8')).decode('utf-8')
        message = {
            'raw': encoded_message,
            'threadId': original.get('threadId')
        }
        self.service.users().messages().send(userId='me', body=message).execute()

    def archive_message(self, msg_id):
        """Remove INBOX label (archive)."""
        self.service.users().messages().modify(
            userId='me', id=msg_id,
            body={'removeLabelIds': ['INBOX']}
        ).execute()

    def add_label(self, msg_id, label_name):
        """Add a label to the message."""
        # Get label id by name, or create it
        labels = self.service.users().labels().list(userId='me').execute().get('labels', [])
        label_id = None
        for label in labels:
            if label['name'] == label_name:
                label_id = label['id']
                break
        if not label_id:
            # Create label
            label_body = {'name': label_name, 'labelListVisibility': 'labelShow', 'messageListVisibility': 'show'}
            created = self.service.users().labels().create(userId='me', body=label_body).execute()
            label_id = created['id']
        self.service.users().messages().modify(
            userId='me', id=msg_id,
            body={'addLabelIds': [label_id]}
        ).execute()

    def delete_message(self, msg_id):
        """Permanently delete a message (spam)."""
        self.service.users().messages().delete(userId='me', id=msg_id).execute()