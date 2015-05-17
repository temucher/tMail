#Main python script for getting emails and texting them to your phone
#First real python script, so stick with me


import sys
import imaplib
import getpass
import email
import email.header
import datetime
import os

user = raw_input("Gmail username:")
pswd = getpass.getpass("Enter your password:")

def processMailbox(M):
	rv, data = M.search(None, "ALL")
	if rv != "Ok":
		print "No messages found!"
		return
	for num in data[0].split():
		rv, data = M.fetch(num, '(RFC822)')
		if rv != "Ok":
			print "Could not fetch message"
			return

        msg = email.message_from_string(data[0][1])
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = unicode(decode[0])
        print 'Message %s: %s' % (num, subject)
        print msg.get_payload()
        print 'Raw Date:', msg['Date']

        #convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print "Local Date:", \
                local_date.strftime("%a, %d %b %Y %H:%M:%S")

M = imaplib.IMAP4_SSL('imap.gmail.com')

#attempt a login
try:
	M.login(user, pswd)
except imaplib.IMAP4.error:
	print "Login failed"

#listing all the available mailboxes, i.e. Inbox, Spam, etc.
"""rv, mailboxes = M.list()
if rv == "Ok":
	print "Mailboxes:"
	print mailboxes"""

#opening the Inbox mailbox
rv, data = M.select("INBOX")
if rv == "Ok":
	processMailbox(M)
	M.close()
else:
	print "Error opening mailbox ", rv

M.logout()
