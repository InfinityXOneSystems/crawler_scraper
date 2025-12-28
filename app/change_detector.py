import logging

from typing import List

class ChangeDetector:
    """
    Change Detector
    This class detects changes in documents.
    """

    def __init__(self):
        self.previous_states = {}

    def detect_changes(self, documents: List[str]) -> List[str]:
        """
        Detect changes in the given documents.

        Args:
            documents (List[str]): List of document paths to check for changes.

        Returns:
            List[str]: List of documents that have changed.
        """
        changed_documents = []
        for doc in documents:
            if self.has_changed(doc):
                changed_documents.append(doc)
        return changed_documents

    def has_changed(self, document: str) -> bool:
        """Check if a single document has changed."""
        # Placeholder for actual change detection logic
        current_state = self.get_document_state(document)
        previous_state = self.previous_states.get(document)
        self.previous_states[document] = current_state
        return current_state != previous_state

    def get_document_state(self, document: str) -> str:
        """Get the current state of a document."""
        # Placeholder for actual state retrieval logic
        return f"state_of_{document}"

# Example usage
if __name__ == "__main__":
    logging.info(f"Changed documents: {changes}")
    changes = detector.detect_changes(["doc1.txt", "doc2.txt"])
    logging.info(f"Changed documents: {changes}")