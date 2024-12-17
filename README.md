This project allows you to connect to a Gmail account using IMAP, fetch unread emails, extract key details (sender, subject, timestamp), and save them in a database. The logs of the process are displayed on the frontend and stored for debugging purposes. The project is built using Django and integrates with Gmail's IMAP server to retrieve emails.

Features:
1. Connects to Gmail's IMAP server using user-provided credentials (email and password).
2. Fetches unread emails and marks them as read.
3. Extracts key details from the email (sender, subject, timestamp).
4. Saves the extracted data in a local SQLite database.
5. Displays logs of the email fetching process in the frontend.
6. Logs are also stored in a log file for further review.

Tech Stack:
Backend: Django (Python)
Database: SQLite (or other database options if configured)
Frontend: HTML, CSS, JavaScript (Django Template Language)
Email Handling: IMAP (using Python's imaplib library)
