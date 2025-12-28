import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

class GoogleWorkspaceIntegration:
    """
    Google Workspace Integration
    Handles interactions with Google Workspace APIs (e.g., Gmail, Drive).
    """

    def __init__(self, credentials=None):
        # Accept injected credentials (for tests) or defer authentication until needed
        self._injected_credentials = credentials
        self.credentials = credentials

    def authenticate(self):
        """Authenticate using the service account key."""
        if self._injected_credentials:
            return self._injected_credentials
        key_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY_PATH")
        # Call from_service_account_file directly. Tests patch this function so
        # calling it allows the test to supply a mock even when no real file exists.
        try:
            return service_account.Credentials.from_service_account_file(key_path or '', scopes=[
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/gmail.send"
        ])
        except FileNotFoundError:
            # Real runtime: no key file found
            raise FileNotFoundError("Service account key file not found.")

    def send_email(self, to_email: str, subject: str, body: str):
        """Send an email using Gmail API."""
        if not self.credentials:
            self.credentials = self.authenticate()
        service = build("gmail", "v1", credentials=self.credentials)
        message = {
            "raw": self.create_email_message(to_email, subject, body)
        }
        service.users().messages().send(userId="me", body=message).execute()

    def create_email_message(self, to_email: str, subject: str, body: str) -> str:
        """Create a raw email message."""
        from email.mime.text import MIMEText
        import base64

        message = MIMEText(body)
        message["to"] = to_email
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return raw

# Example usage
if __name__ == "__main__":
    integration = GoogleWorkspaceIntegration()
    integration.send_email("example@example.com", "Test Subject", "Test Body")