# importing libraries

import imaplib

import email
from email.header import decode_header
import os
from email.message import EmailMessage
import smtplib
from datetime import date

# defining username and password variables which correspond to your Account credentials for your Outlook/gmail account

username = os.environ.get('EMAIL_USERNAME')
password = os.environ.get('EMAIL_PSWD')

# if you need it for accessing to a shared email you would then use slashes as follow: 'OWN_USERNAME@outlook.com\\\SHARED_EMAIL_BOX@outlook.com'
# you could set the following environment variables EMAIL_USERNAME and EMAIL_PSWD if you have the possibility to schedule this script for instance with Cloudera Machine Learining

# Connect to your mailbox

imap_server = "imap.COMPANY_NAME.COUNTRY_DOMAIN"
imap = imaplib.IMAP4_SSL(imap_server)
imap.login(username, password)
status, messages = imap.select("INBOX") #replace Inbox with the folder that you prefer

# Total number of emails
n_messages = int(messages[0])

# Set number of emails that you would read

current_date = date.today()
N = 50 if current_date.weekday() == 0 else 35 #where weekday = 0 is Monday.. Sunday = 6


# ----- Retrieve Emails Information -----

message_received = []
message_sender = []
message_body = []

for i in range(n_messages, n_messages-N, -1):
    # fetch the email message by ID protocol
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # parse a bytes email into a message object
            msg = email.message_from_string(response[1].decode('utf-8'))
            email_subject = msg['subject']
            email_body = msg.get_payload(decode=True)
            message_body.append(email_body)
            message_received.append(email_subject)
            email_from = msg['from']
            message_sender.append(email_from) 
            date = decode_header(msg["Date"])[0][0]

print('First message recieved: \n', message_received[0])
print('First message sender: \n', message_sender[0])
print('First message body: \n', message_body[0])


# ----- Check for the Files Received including all the expected combination under files -----

keys = ['FR_BANK', 'DE_BANK', 'XS_BANK','NL_BANK', 'IT_BANK', 'PT_BANK']
values = ['NI', 'OA', 'STQ', 'STM', 'STX', 'DT', 'DO', 'NA']
files = ['XS_BANK_OA', 'XS_BANK_NI', 'FR_BANK_STM', 'IT_BANK_DT', 'IT_BANK_DO',
         'PT_BANK_OA', 'PT_BANK_NI','FR_BANK_STX', 'FR_BANK_STQ',
         'FR_BANK_OA', 'DE_BANK_OA', 'DE_BANK_NI', 'XS_BANK_OA', 'XS_BANK_NI']
    
files_NA = ['XS_BANK_NA', 'XS_BANK_NA', 'NL_BANK_NA', 'FR_BANK_NA', 'DE_BANK_NA'] #these banks sometimes send NA email
files_received = []
files_NA = []

#iterating over the message_received which corresponds to the subject

for m in message_received:
    for k in keys:
        for value in values:
            if str(value) in m and str(k) in m:
                print(f"File {value} received from {k}")
                files_received.append(f"{k}_{value}")
                if 'NA' in m:
                    files_NA.append(f"{k}_{value}")

print('Num. Files received: \n', len(files_received))
files_received = list(set(files_received))  # ?
print('Num. Files received: \n', len(files_received))

res = list(map(lambda st: str.replace(st, "NA", "NI"), files_NA))
files_missing = list(set(files)-set(files_received)-set(res))
print("The missing files are: \n", '\n'.join(map(str, files_missing)))

if len(files_NA) > 1:
    print("The NA files of the day are: \n", '\n'.join(map(str, files_NA)))
else:
    print("Maybe NA files are still missing")


# ----- Send Email within your team -----

msg = EmailMessage()
msg['From'] = "SENDER@outlook.com"
msg['To'] = "RECEPIENT_EMAIL@outlook.com"
msg['Cc'] = "TEAM_EMAIL@outlook.com"


string_files_missing = "\n".join(f"{element}" for element in files_missing)
string_files_NA = "\n".join(f"{element}" for element in files_NA)
if len(files_missing) != 0:
    msg['Subject'] = 'Email daily check'
    msg.set_content(f'''Dear Team,

We would inform you that we are missing the following files:

{string_files_missing}

The NA files of the day are:

{string_files_NA}

Could you please check the mail inbox?

Kind regards,
Your Team''')
else:
    msg['Subject'] = 'Email daily check'
    msg.set_content(f'''Dear Team,

We received every files from the data providers.

The NA files of the day are:

{string_files_NA}

Kind regards,
Your Team''')

send_message(msg)
print("Email Sent!")
