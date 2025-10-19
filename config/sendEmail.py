import os
import resend
from dotenv import load_dotenv


load_dotenv()

# Set API key
resend.api_key = os.getenv("RESEND_API")

import asyncio

async def send_mail(receiver_mail: str, subject: str, html: str):
    try:
        params = {
            "from": "Blinkit <onboarding@resend.dev>",
            "to": [receiver_mail],
            "subject": subject,
            "html": html,
        }

        # Run the blocking call in a separate thread to avoid blocking FastAPI
        email = await asyncio.to_thread(resend.Emails.send(params))
        

    except Exception as e:
        return {"error": True, "message": str(e)}


