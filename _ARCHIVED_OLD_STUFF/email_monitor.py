
import imaplib
import email
from email.header import decode_header
import time
import os
import json
import requests
from datetime import datetime

# --- CONFIGURATION (Load from Env Vars) ---
IMAP_SERVER = os.getenv('SMTP_HOST', 'imap.gmail.com') # Default to Gmail for now, but changeable
IMAP_PORT = 993
EMAIL_USER = os.getenv('SMTP_USER')
EMAIL_PASS = os.getenv('SMTP_PASS')
WEBHOOK_API_URL = "http://127.0.0.1:8080/api/contact" # Send to local API to unify with admin panel

def connect_and_check():
    if not EMAIL_USER or not EMAIL_PASS:
        print("❌ EMAIL_MONITOR: No credentials found. Sleeping...")
        return

    try:
        # Connect to the server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        # Search for unseen emails
        status, messages = mail.search(None, "(UNSEEN)")
        email_ids = messages[0].split()

        if not email_ids:
            print("📭 EMAIL_MONITOR: No new emails.")
            return

        print(f"📬 EMAIL_MONITOR: Found {len(email_ids)} new email(s)!")

        for e_id in email_ids:
            # Fetch the email
            res, msg = mail.fetch(e_id, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    
                    # Decode Subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    
                    # Decode Sender
                    from_ = msg.get("From")
                    
                    # Get Body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                    else:
                        body = msg.get_payload(decode=True).decode()

                    # INTELLIGENT ROUTING logic
                    # We repackage this email as a "Contact Message" and send it to our own system
                    # So it appears in the Admin Dashboard
                    
                    payload = {
                        "name": from_,
                        "email": from_, # Simplified
                        "subject": f"📧 [EMAIL] {subject}",
                        "message": body[:500] + "...", # Truncate for dashboard view
                        "userLanguage": "en",
                        "romanianMessage": ""
                    }
                    
                    # Send to our own API
                    try:
                        requests.post(WEBHOOK_API_URL, json=payload)
                        print(f"✅ Forwarded email '{subject}' to Admin Console.")
                    except Exception as api_err:
                        print(f"⚠️ Failed to forward to API: {api_err}")

    except Exception as e:
        print(f"❌ EMAIL_MONITOR ERROR: {e}")
    finally:
        try:
            mail.logout()
        except:
            pass

if __name__ == "__main__":
    print("🕵️ EMAIL SENTINEL STARTED...")
    while True:
        connect_and_check()
        time.sleep(300) # Check every 5 minutes
