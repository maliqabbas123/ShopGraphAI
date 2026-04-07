"""
Gemini API service wrapper.

Centralizes all interactions with Google's Gemini API.
Provides clean interface for different types of LLM calls.
"""

import json
import logging
from typing import Dict, Any, Optional, List
import google.generativeai as genai

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class GeminiService:
    """
    Service class for interacting with Gemini API.

    Handles all LLM calls with proper error handling and response parsing.
    """

    def __init__(self):
        """Initialize Gemini API configuration."""
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)
        logger.info(f"Initialized Gemini service with model: {settings.gemini_model}")

    async def classify_intent(self, user_input: str, conversation_history: Optional[List[str]] = None) -> str:
        """
        Classify user's intent from their message.

        Args:
            user_input: User's current message
            conversation_history: Optional previous messages for context

        Returns:
            Intent string: "search", "compare", "order", "cart", or "chat"
        """
        try:
            # Build context from conversation history
            context = ""
            if conversation_history:
                recent_messages = conversation_history[-4:]  # Last 2 exchanges
                context = "Previous conversation:\n" + "\n".join(recent_messages) + "\n\n"

            prompt = f"""{context}Classify the intent of this user message into ONE of these categories:

User message: "{user_input}"

Categories:
- "search": User wants to find/search for products (e.g., "find laptops", "show me phones")
- "compare": User wants to compare products (e.g., "compare the first two", "which is better")
- "order": User wants to order/buy a product (e.g., "order the first one", "buy it", "add to cart")
- "cart": User wants to manage their cart (e.g., "show my cart", "remove item")
- "chat": General conversation or question (e.g., "hello", "what can you do")

Respond with ONLY ONE WORD - the category name. No explanation, just the category."""

            response = self.model.generate_content(prompt)
            intent = response.text.strip().lower()

            # Validate response
            valid_intents = ["search", "compare", "order", "cart", "chat"]
            if intent not in valid_intents:
                logger.warning(f"Invalid intent '{intent}', defaulting to 'chat'")
                intent = "chat"

            logger.info(f"Classified intent: {intent}")
            return intent

        except Exception as e:
            logger.error(f"Error classifying intent: {e}")
            return "chat"  # Default fallback

    async def extract_search_filters(self, user_input: str) -> Dict[str, Any]:
        """
        Extract structured search filters from natural language query.

        Args:
            user_input: User's search query

        Returns:
            Dictionary of filters (category, brand, price range, rating, etc.)
        """
        try:
            prompt = f"""Extract search filters from this product search query.

User query: "{user_input}"

Extract these fields if mentioned:
- category: Product category (laptop, phone, headphones, tablet, smartwatch, etc.)
- brand: Brand name (Apple, Samsung, Dell, HP, Sony, etc.)
- min_price: Minimum price (number only)
- max_price: Maximum price (number only)
- min_rating: Minimum rating (number only, 1-5)
- tags: Relevant search tags as array (gaming, wireless, professional, budget, premium, etc.)

Respond with a JSON object containing only the fields that were mentioned.
If a field is not mentioned, do not include it in the JSON.

Example:
User: "Find gaming laptops under $1500"
Response: {{"category": "laptop", "max_price": 1500, "tags": ["gaming"]}}

Respond with ONLY valid JSON, no other text."""

            response = self.model.generate_content(prompt)
            filters_text = response.text.strip()

            # Clean response (remove markdown code blocks if present)
            if "```json" in filters_text:
                filters_text = filters_text.split("```json")[1].split("```")[0].strip()
            elif "```" in filters_text:
                filters_text = filters_text.split("```")[1].split("```")[0].strip()

            filters = json.loads(filters_text)
            logger.info(f"Extracted filters: {filters}")
            return filters

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse filters JSON: {e}, response: {filters_text}")
            return {}
        except Exception as e:
            logger.error(f"Error extracting filters: {e}")
            return {}

    async def generate_comparison_explanation(
        self,
        products: List[Dict[str, Any]],
        comparison_data: Dict[str, Any]
    ) -> str:
        """
        Generate natural language explanation of product comparison.

        Args:
            products: List of products being compared
            comparison_data: Structured comparison data

        Returns:
            Natural language comparison explanation
        """
        try:
            products_summary = "\n".join([
                f"{i+1}. {p['title']} - {p['brand']} - ${p['price']}"
                for i, p in enumerate(products)
            ])

            prompt = f"""Generate a helpful comparison summary for these products:

{products_summary}

Comparison data:
{json.dumps(comparison_data, indent=2)}

Provide a concise, helpful comparison highlighting:
1. Key differences
2. Best value
3. Best for specific use cases

Keep it under 150 words and user-friendly."""

            response = self.model.generate_content(prompt)
            explanation = response.text.strip()
            logger.info("Generated comparison explanation")
            return explanation

        except Exception as e:
            logger.error(f"Error generating comparison: {e}")
            return "I compared the products. Check the detailed comparison above."

    async def generate_chat_response(self, user_input: str, context: Optional[str] = None) -> str:
        """
        Generate conversational response for general chat.

        Args:
            user_input: User's message
            context: Optional context about the conversation

        Returns:
            Friendly conversational response
        """
        try:
            context_str = f"\n\nContext: {context}" if context else ""

            prompt = f"""You are a helpful shopping assistant AI. Respond to this user message in a friendly, concise way.

User message: "{user_input}"{context_str}

Provide a helpful response. Keep it under 100 words."""

            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            logger.error(f"Error generating chat response: {e}")
            return "I'm here to help you find products. Try asking me to search for something!"


# Singleton instance
_gemini_service: Optional[GeminiService] = None


def get_gemini_service() -> GeminiService:
    """Get or create Gemini service singleton."""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service
