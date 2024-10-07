import json
import logging

from openai import OpenAI
from config import OPENAI_KEY

logger = logging.getLogger("Main")

client = OpenAI(api_key=OPENAI_KEY,)


async def get_chatgpt_response(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o-mini",
        )
        content = chat_completion.choices[0].message.content
        logger.info("Request from openai successful")
        return content
    except Exception as e:
        logger.error(f"Error occurred while calling OpenAI API: {e}")


