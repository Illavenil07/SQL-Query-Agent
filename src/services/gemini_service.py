""" Service for building prompts and querying Gemini LLM API. """

import google.generativeai as genai
import logging
from config import Config


class GeminiService:
    """Handles prompt creation and LLM API calls."""

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-pro")

    def build_prompt(self, schema_context, user_query):
        """Compose the final prompt for the LLM."""
        prompt = f"""
        Database Schema:
        {schema_context}

        User Request:
        {user_query}

        Assume that your are a SQL expert. Write a valid MS SQL query using the above schema. 
        Also make sure that the output is just the SQL query (no other text or title) and not any other text.
        """
        return prompt

    def generate_sql_query(self, prompt):
        """Send prompt to Gemini and retrieve generated SQL query."""
        try:
            response = self.model.generate_content(
                contents=prompt
            )
            # The generated text is usually under `response.candidates[0].content`
           
            logging.info(f"Gemini response: {response}")
            sql_query = response.text.strip()
            cleaned_sql = self.clean_sql_string(sql_query)
            return cleaned_sql
        except Exception as e:
            raise Exception(f"Failed to generate SQL query: {str(e)}")

    def clean_sql_string(self, sql_string):
        clean_sql = sql_string.replace("```sql\n", "").replace("\n```", "").strip()
        return clean_sql
