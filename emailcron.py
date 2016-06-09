#! /usr/bin/python2.7
import smtplib, imaplib, email, sys

imap_host = "mail.example.com"
smtp_host = "mail.example.com"
smtp_port = 587
user = "alert"
passwd = “xxxxxxxx”
from_addr = "from@example.com"
to_addr = "to@example.com"

# open IMAP connection
client = imaplib.IMAP4(imap_host)
client.login(user, passwd)
client.select('INBOX')

try:
    status, response = client.search(None, '(UNSEEN)' '(SUBJECT "MODETWO")')
    email_ids = [e_id for e_id in response[0].split()]
    print email_ids
    if not email_ids:
        print "Failed: No unread messages found on the server"
        sys.exit()
    else:
        pass
except:
    print "Failed: No unread messages found on the server 2"
    client.close()
    client.logout()
    sys.exit()

print "Authenticating SMTP Server"
smtp = smtplib.SMTP(smtp_host, smtp_port)
smtp.starttls()
smtp.login(user, passwd)

for response in email_ids:
    status, data = client.fetch(response, "(RFC822)")
    email_data = data[0][1]
    message = email.message_from_string(email_data)
    message.replace_header("From", from_addr)
    message.replace_header("To", to_addr)
    smtp.sendmail(from_addr, to_addr, message.as_string())
#    client.store(response, '+FLAGS', '\\Deleted') 
#    client.expunge()

client.close()
client.logout()
smtp.quit()


