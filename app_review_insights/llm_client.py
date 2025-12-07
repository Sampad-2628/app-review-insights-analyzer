import random
from typing import List
from . import config

class LLMClient:
    def __init__(self, provider=config.LLM_PROVIDER):
        self.provider = provider

    def categorize_review(self, text: str, themes: List[str]) -> str:
        """
        Categorizes a review text into one of the provided themes.
        Uses a mock keyword-based approach if provider is 'mock'.
        """
        if self.provider == "mock":
            return self._mock_categorize(text, themes)
        else:
            # Implement actual LLM call here (e.g., OpenAI API)
            return self._mock_categorize(text, themes)

    def _mock_categorize(self, text: str, themes: List[str]) -> str:
        text_lower = text.lower()
        
        # Simple keyword matching for mock implementation
        if any(w in text_lower for w in ['support', 'customer', 'service', 'reply']):
            return "Customer Support"
        if any(w in text_lower for w in ['charge', 'fee', 'money', 'cost', 'brokerage']):
            return "Pricing & Charges"
        if any(w in text_lower for w in ['bug', 'crash', 'slow', 'lag', 'install', 'error']):
            return "App Performance & Bugs"
        if any(w in text_lower for w in ['feature', 'option', 'trade', 'stock', 'f&o', 'ipo']):
            return "Trading & Features"
        
        # Default fallback
        return "User Experience"

    def generate_summary(self, reviews: List[dict]) -> str:
        """Generates a summary of the reviews."""
        return f"Analyzed {len(reviews)} reviews. Users are discussing various topics ranging from performance to pricing."
