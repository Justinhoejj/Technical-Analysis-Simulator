from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv


load_dotenv()

def send_mail(email_addresses, subject, message):
  message = Mail(from_email='hoejj05@gmail.com',
          to_emails=email_addresses,
          subject=f'TA Simulator: {subject}',
          html_content=message)
  try:
    sg = SendGridAPIClient(os.environ["SEND_GRID_API_KEY"])
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
  except Exception as e:
    print(e.message)