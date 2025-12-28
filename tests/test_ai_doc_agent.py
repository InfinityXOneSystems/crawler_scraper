import unittest
from unittest.mock import patch
from crawler_scraper.app.ai_doc_agent import AIDocAgent

class TestAIDocAgent(unittest.TestCase):

    def setUp(self):
        with patch.object(AIDocAgent, 'load_model', return_value="Mocked model"):
            self.agent = AIDocAgent(model_path="/path/to/mock_model")

    def test_load_model(self):
        """Test loading the AI model."""
        self.assertEqual(self.agent.model, "Mocked model")

    def test_process_document(self):
        """Test processing a document."""
        document = "Sample document content."
        result = self.agent.process_document(document)
        self.assertIn("document_length", result)
        self.assertIn("analysis", result)
        self.assertEqual(result["document_length"], len(document))

if __name__ == "__main__":
    unittest.main()