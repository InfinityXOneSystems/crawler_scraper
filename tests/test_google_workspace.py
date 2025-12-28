import unittest
from unittest.mock import patch, MagicMock
from crawler_scraper.app.google_workspace import GoogleWorkspaceIntegration

class TestGoogleWorkspaceIntegration(unittest.TestCase):

    @patch("crawler_scraper.app.google_workspace.service_account.Credentials.from_service_account_file")
    @patch("crawler_scraper.app.google_workspace.build")
    def test_send_email(self, mock_build, mock_credentials):
        """Test sending an email using the Gmail API."""
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        integration = GoogleWorkspaceIntegration()
        integration.send_email("test@example.com", "Test Subject", "Test Body")

        mock_service.users().messages().send.assert_called_once()

if __name__ == "__main__":
    unittest.main()