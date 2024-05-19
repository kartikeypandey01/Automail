import os
import base64
import email
import logging
import shutil
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

log_file = f'email_fetch_{datetime.now().strftime("%Y-%m-%d")}.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json',SCOPES)
            creds = flow.run_local_server(host='localhost',port=8080,open_browser=True)
        with open('token.json','w') as token:
            token.write(creds.to_json())
    return creds

def fetch_emails():
    try:
        remove_previous()
        creds = get_credentials()
        service = build('gmail','v1', credentials=creds)
        results = service.users().messages().list(userId = 'me', q = 'is:unread -category:social -category:promotions').execute()
        messages = results.get('messages',[])
        logging.info(f'Fetched {len(messages)} new messages')

        for message in messages:
            msg =service.users().messages().get(userId='me', id= message['id'],format = 'raw').execute()
            raw_email = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
            mime_msg = email.message_from_bytes(raw_email)
            save_email(mime_msg)
            service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()
            
    except Exception as e:
        logging.error(f'Error fetching emails: {e}')

def remove_previous():
    try:
        yesterday = datetime.now() - timedelta(1)
        yesterday_folder = yesterday.strftime('%Y-%m-%d')
        if os.path.exists(yesterday_folder):
            try:
                shutil.rmtree(yesterday_folder)
                logging.info(f'Removed previous mail folder successfully')
            except Exception as err:
                logging.error(f'Error removing previous folder: {err}')

            try:
                os.remove(f'email_fetch_{yesterday_folder}.log')
                logging.info(f'Removed previous log file successfully')
            except Exception as e:
                logging.error(f'Error removing previous log file: {e}')
    except Exception as e:
        logging.error(f'Error removing previous files: {e}')

def save_email(msg):
    try:
        
        today_folder = datetime.now().strftime('%Y-%m-%d')
        if not os.path.exists(today_folder):
            os.makedirs(today_folder)
        with open(os.path.join(today_folder,f'email_{datetime.now().strftime("%H-%M-%S")}.eml'),'wb') as f:
            f.write(msg.as_bytes())
        logging.info(f'Email saved in {today_folder}.')
    except Exception as e:
        logging.error(f'Error saving email:{e}')

if __name__ == '__main__':
    logging.info('Script Started')

    fetch_emails()




        
