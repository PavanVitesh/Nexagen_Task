import imaplib
import email
from email.header import decode_header
import re
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .models import Email



def fetch_unread_emails(request):
    logs = []

    if request.method == 'POST':
        email_address = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Connect to Gmail's IMAP server
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(email_address, password)
            mail.select("inbox")

            status, messages = mail.search(None, "(UNSEEN)")
            if status != "OK":
                error_msg = "Error searching for unread emails."
                logs.append(error_msg)
                return render(request, "fetch_emails.html", {"logs": logs})

            email_ids = messages[0].split()
            email_count = len(email_ids)
            success_msg = f"Found {email_count} unread emails."
            logs.append(success_msg)

            for email_id in email_ids:
                res, msg = mail.fetch(email_id, "(RFC822)")
                if res != "OK":
                    continue

                for response_part in msg:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or "utf-8")
                        sender = msg.get("From")
                        timestamp = msg.get("Date")

                        # Clean the timestamp
                        cleaned_timestamp = re.sub(r'\s*\(.*?\)', '', timestamp)
                        cleaned_timestamp = cleaned_timestamp.replace("GMT", "+0000")
                        date_object = datetime.strptime(cleaned_timestamp, "%a, %d %b %Y %H:%M:%S %z")

                        # Save email to the database
                        Email.objects.create(
                            sender=sender,
                            subject=subject,
                            timestamp=date_object
                        )
                        email_log_msg = f"Processed email from {sender} with subject '{subject}' at {date_object.strftime('%Y-%m-%d %H:%M:%S')}"
                        logs.append(email_log_msg)

            mail.logout()
            success_msg = "Email fetching process completed successfully."
            logs.append(success_msg)

        except Exception as e:
            error_msg = f"Error in email fetching process: {e}"
            logs.append(error_msg)
    
    return render(request, "fetch_emails.html", {"logs": logs})
