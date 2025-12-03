import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

def send_password_email(to_email: str, password: str) -> bool:
    """
    Send password recovery email via Gmail SMTP.
    
    Args:
        to_email: Recipient email address
        password: User's password to send
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from_email = os.getenv("SMTP_FROM_EMAIL", smtp_username)
    
    # Validate SMTP configuration
    if not smtp_username or not smtp_password:
        print("ERROR: SMTP credentials not configured in environment variables")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "MindTrace - Password Recovery"
        msg["From"] = smtp_from_email
        msg["To"] = to_email
        
        # Create email body
        text_content = f"""
Hello,

You requested to recover your password for MindTrace.

Your password is: {password}

For security reasons, we recommend changing your password after logging in.

If you didn't request this, please ignore this email.

Best regards,
MindTrace Team
"""
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #1f2937; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ background-color: #f9fafb; padding: 30px; border-radius: 0 0 8px 8px; }}
        .password-box {{ background-color: white; border: 2px solid #4f46e5; padding: 15px; margin: 20px 0; border-radius: 8px; text-align: center; }}
        .password {{ font-size: 24px; font-weight: bold; color: #4f46e5; letter-spacing: 2px; }}
        .footer {{ margin-top: 20px; font-size: 12px; color: #6b7280; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>MindTrace</h1>
            <p>Password Recovery</p>
        </div>
        <div class="content">
            <p>Hello,</p>
            <p>You requested to recover your password for MindTrace.</p>
            <div class="password-box">
                <p style="margin: 0; font-size: 14px; color: #6b7280;">Your password is:</p>
                <p class="password">{password}</p>
            </div>
            <p><strong>Important:</strong> For security reasons, we recommend changing your password after logging in.</p>
            <p>If you didn't request this, please ignore this email.</p>
            <div class="footer">
                <p>Best regards,<br>MindTrace Team</p>
            </div>
        </div>
    </div>
</body>
</html>
"""
        
        # Attach both plain text and HTML versions
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        
        print(f"Password recovery email sent successfully to {to_email}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("ERROR: SMTP authentication failed. Check your Gmail credentials.")
        return False
    except smtplib.SMTPException as e:
        print(f"ERROR: SMTP error occurred: {str(e)}")
        return False
    except Exception as e:
        print(f"ERROR: Failed to send email: {str(e)}")
        return False
