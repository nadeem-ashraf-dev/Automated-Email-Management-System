import google.generativeai as genai
from config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)

class GeminiClient:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')

    def classify_email(self, subject: str, body: str) -> dict:
        """
        Classify email into one of: high_priority, customer_support, newsletter, spam, other.
        Returns dict with category and confidence (0-100).
        """
        prompt = f"""
        You are an email classifier. Analyze the following email and classify it into exactly one of these categories:
        - high_priority: urgent, critical, executive, account issues, payment failures, etc.
        - customer_support: product questions, help requests, feedback, complaints.
        - newsletter: promotional content, mailing lists, updates.
        - spam: unsolicited, promotional, phishing, irrelevant.
        - other: none of the above.

        Provide your answer as a JSON object with keys: "category" and "confidence" (integer 0-100).
        Only output the JSON, no other text.

        Subject: {subject}
        Body: {body}
        """

        response = self.model.generate_content(prompt)
        try:
            # Attempt to parse JSON from response
            import json
            result = json.loads(response.text)
            category = result.get('category', 'other')
            confidence = result.get('confidence', 50)
            # Ensure category is valid
            valid_categories = ['high_priority', 'customer_support', 'newsletter', 'spam', 'other']
            if category not in valid_categories:
                category = 'other'
            return {'category': category, 'confidence': confidence}
        except:
            return {'category': 'other', 'confidence': 50}