def create_email_template(name: str, verify_url: str) -> str:
    """
    Create HTML email template for email verification
    """
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verify Your Blinkit Account</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background-color: #f9f9f9;
                border-radius: 10px;
                padding: 30px;
                text-align: center;
            }}
            .logo {{
                font-size: 28px;
                font-weight: bold;
                color: #ff6b35;
                margin-bottom: 20px;
            }}
            .button {{
                display: inline-block;
                background-color: #ff6b35;
                color: white;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                margin: 20px 0;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 12px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">Blinkit</div>
            <h1>Welcome, {name}!</h1>
            <p>Thank you for joining Blinkit. Please verify your email address to complete your registration.</p>
            <a href="{verify_url}" class="button">Verify Email Address</a>
            <p>If the button doesn't work, copy and paste this link into your browser:</p>
            <p style="word-break: break-all; color: #666;">{verify_url}</p>
            <div class="footer">
                <p>This verification link will expire in 24 hours.</p>
                <p>If you didn't create an account with Blinkit, please ignore this email.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_template

