import imaplib
import email
mail = imaplib.IMAP4_SSL('imap.gmail.com')
# imaplib module implements connection based on IMAPv4 protocol
mail.login('username at gmail.com', 'password')
# >> ('OK', [username at gmail.com Saksham authenticated (Success)'])
Selecting a Label
Your GMail inbox has multiple labels like ‘Inbox’ and many more custom defined by you. Lets say you want to search / download all emails labeled as ‘Inbox’, so we choose Inbox.

?
1
2
mail.list() # Lists all labels in GMail
mail.select('inbox') # Connected to inbox.
Searching Through Inbox
We’ll search through the label and retrieve all the emails. Refer imaplib documentation for more usage.

?
1
2
3
4
5
6
7
8
result, data = mail.uid('search', None, "ALL")
# search and return uids instead
i = len(data[0].split()) # data[0] is a space separate string
for x in range(i):
 latest_email_uid = data[0].split()[x] # unique ids wrt label selected
 result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
 # fetch the email body (RFC822) for the given ID
 raw_email = email_data[0][1]
Parsing Raw Email
 raw_email is NOT string but a byte literal. Lets say raw_email = b'<email-contents>’ , now str() will simply convert entire literal as string. So we need to use decode(‘utf-8’) to keep the <email-contents> only.
In a multi-part email Content-Type: multipart/mixed; It will contain several parts Content-Type: text/plain or Content-Type: application/octet-stream etc. Right now i’m extracting the text part of main body only, without any attachments.
?
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
#continue inside the same for loop as above
raw_email_string = raw_email.decode('utf-8')
# converts byte literal to string removing b''
email_message = email.message_from_string(raw_email_string)
# this will loop through all the available multiparts in mail
for part in email_message.walk():
 if part.get_content_type() == "text/plain": # ignore attachments/html
  body = part.get_payload(decode=True)
  save_string = str("D:Dumpgmailemail_" + str(x) + ".eml")
  # location on disk
  myfile = open(save_string, 'a')
  myfile.write(body.decode('utf-8'))
  # body is again a byte literal
  myfile.close()
 else:
  continue