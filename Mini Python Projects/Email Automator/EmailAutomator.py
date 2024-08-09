import smtplib
from email.mime.text import MIMEText
import json


class Auto:
    def __init__(self, port=587):
        """
        Initialize the EmailAutomator with SMTP server details and credentials.

        :param port: The port number used by the SMTP server (e.g., 587).
        """

        def __read_email_credentials():
            """
            Reads email and password from a JSON file.

            :return: Dictionary with email and password.
            """
            try:
                with open("Credentials.json", 'r') as file:
                    data = json.load(file)
                    return {
                        "email": data.get("email"),
                        "password": data.get("password"),
                        "domain": data.get("domain")
                    }
            except FileNotFoundError:
                print(f"The JSON file does not exist.")
                return None
            except json.JSONDecodeError:
                print(f"There was an error decoding the JSON file.")
                return None

        credentials = __read_email_credentials()
        if not credentials:
            raise FileNotFoundError("Credentials.json does not exist.")
        elif len(credentials['email']) == 0 or len(credentials['password']) == 0:
            raise ValueError("Email and password are required.")
        if credentials['domain'] == 'outlook':
            self.smtp_server = 'smtp.office365.com'
        elif credentials['domain'] == 'gmail':
            self.smtp_server = 'smtp.gmail.com'
        else:
            raise ValueError(f"Invalid domain given: {credentials['domain']}")
        self.port = port
        self.username = credentials['email']
        self.password = credentials['password']

    def send_email(self, recipient, subject, body):
        """
        Send an email with the specified recipient, subject, and body.

        :param recipient: The recipient's email address.
        :param subject: The subject of the email.
        :param body: The body of the email.
        """
        # Create the email message
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = recipient

        # Connect to the SMTP server
        server = smtplib.SMTP(self.smtp_server, self.port)
        server.starttls()
        server.login(self.username, self.password)

        # Send the email
        text = msg.as_string()
        server.sendmail(self.username, recipient, text)
        server.quit()


"""
# This is a full example usage of the EmailAutomator class in another file
# Specify the recipient, subject, and body of the email
from EmailAutomator import Auto
auto = Auto()
recipient = 'Nirt_12023@outlook.com'
subject = 'Test Email'
body = 'This is a test email sent using automation.'
auto.send_email(recipient, subject, body)
"""
