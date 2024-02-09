## How to check incoming Outlook/Gmail emails
By using [**Python’s IMAP library** ](https://docs.python.org/3/library/imaplib.html), it is possible to access your email inbox. This library works with both Outlook and Gmail.

During one of my working experiences, I had to check if all the files were sent overnight from the different data providers to my email inbox before starting the daily tasks. Therefore I developed the script <span style="color: green">check_outlook_emails.py</span> that aims to read my last received emails by sending me a checking report every morning. In particular, the script reads the subject of the emails and matches them with a list of expected files *files* that I was expecting to receive on a regular daily basis.

Finally, the code automatically sends the report email to my team as a sort of notification about the files received, missing or the one not available (NA). The script has been scheduled on Clouder Machine Learning licence (CML) which set its running in the early morning by producing the mentioned outcome. It has been crucial for saving working time, and being aware of the available data. Indeed, in case of a missing file, it was possible to immediately notify the related data provider.

## Structure
The following paragraph explains how the code has been developed:
- importing libraries
- setting username and password variables which correspond to your Outlook credentials (if you need to access a shared email box then you would set your username variable as follows with three back slashes: *'OWN_USERNAME@outlook.com\\\SHARED_EMAIL_BOX@outlook.com'*)
- logging-in to the server and your Outlook account
- select the folder that you prefer to access such as "INBOX"
- specify the amount of email that you would iterate (depending on the needed amount of emails)
- for-loop that retrieves the email information such as subject, body, sender... With *imap.fetch* sets to *'RFC822'* is possible to retrieve the email's metadata
- iterating over the message_received which corresponds to the subject by checking all the expected combinations of files that we should receive
- storing lists according to the daily files received, missing or NA
- sending the final report by email with *EmailMessage*

In conclusion, the Python script <span style="color: gray">check_outlook_emails.py</span> demonstrates how to use Python’s IMAP library to retrieve emails from Outlook. There are many possibilities that you could implement based on different criteria and your business needs. With this code, you can automate the process of retrieving emails and save time on manual email retrieval.

## Author
Marco Monini 2024
