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



# import resend

# resend.api_key = "re_xxxxxxxxx"

# params: resend.Emails.SendParams = {
#   "from": "Acme <onboarding@resend.dev>",
#   "to": ["delivered@resend.dev"],
#   "subject": "hello world",
#   "html": "<p>it works!</p>"
# }

# email = resend.Emails.send(params)
# print(email)