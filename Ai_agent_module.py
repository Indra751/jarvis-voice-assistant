import os
import logging
from typing import Optional, Dict, Any
from google import genai
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIClient:
    """Enhanced AI client with better error handling and response optimization."""
    
    def __init__(self):
        """Initialize the AI client with environment configuration."""
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        try:
            self.client = genai.Client(api_key=self.api_key)
            logger.info("Gemini AI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            raise
    
    def generate_response(
        self, 
        prompt: str, 
        model: str = "gemini-2.0-flash-exp",
        context: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate AI response with enhanced prompting and error handling.
        
        Args:
            prompt: The user's input prompt
            model: Gemini model to use
            context: Optional context for better responses
            max_tokens: Maximum tokens in response
            
        Returns:
            AI-generated response string
        """
        try:
            # Enhance prompt with context if provided
            if context:
                enhanced_prompt = f"{context}\n\nUser: {prompt}"
            else:
                enhanced_prompt = prompt
            
            # Generate content
            response = self.client.models.generate_content(
                model=model,
                contents=enhanced_prompt
            )
            
            # Clean and return response
            cleaned_response = self._clean_response(response.text)
            logger.info(f"Generated response: {cleaned_response[:100]}...")
            
            return cleaned_response
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return f"I apologize, but I'm having trouble processing your request right now."
    
    def _clean_response(self, text: str) -> str:
        """Clean up AI response for better voice output."""
        if not text:
            return "I'm sorry, I couldn't generate a response."
            
        # Remove markdown formatting
        cleaned = text.replace("*", "").replace("#", "").replace("`", "")
        
        # Remove excessive whitespace
        cleaned = " ".join(cleaned.split())
        
        # Ensure response ends with proper punctuation
        if cleaned and not cleaned.endswith(('.', '!', '?')):
            cleaned += '.'
            
        return cleaned.strip()
    
    def get_contextual_response(self, query: str, assistant_context: str = None) -> str:
        """
        Get a contextual response optimized for voice assistant interaction.
        
        Args:
            query: User's query
            assistant_context: Context about the assistant's capabilities
            
        Returns:
            Contextual AI response
        """
        default_context = """
        You are Jarvis, a helpful voice assistant. You should:
        - Respond naturally and conversationally
        - Keep responses concise but informative
        - Be friendly and professional
        - Provide practical, actionable information when possible
        - If you can't help with something, suggest alternatives
        """
        
        context = assistant_context or default_context
        return self.generate_response(query, context=context)

def main():
    """Test the AI client functionality."""
    try:
        client = AIClient()
        
        # Test basic functionality
        test_queries = [
            "Explain how AI works in simple terms",
            "What's the weather like today?",
            "Tell me a joke",
            "How do I improve my productivity?"
        ]
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            response = client.get_contextual_response(query)
            print(f"Response: {response}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error testing AI client: {e}")

if __name__ == "__main__":
    main()