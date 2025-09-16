def create_forgot_password_template(name: str, otp: str) -> str:
    """
    Creates an HTML email template for the forgot password OTP.
    """
    return f"""
    <html>
      <head></head>
      <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
          <h2 style="color: #333;">Blinkit Password Reset Request</h2>
          <p>Hi {name},</p>
          <p>We received a request to reset the password for your account. Please use the following One-Time Password (OTP) to proceed.</p>
          <p style="font-size: 24px; font-weight: bold; color: #000; text-align: center; letter-spacing: 5px; margin: 30px 0; padding: 15px; background-color: #f5f5f5; border-radius: 5px;">
            {otp}
          </p>
          <p>This OTP is valid for <strong>1 hour</strong>. If you did not request a password reset, please ignore this email or contact our support if you have concerns.</p>
          <p>Thanks,<br/>The Blinkit Team</p>
        </div>
      </body>
    </html>
    """