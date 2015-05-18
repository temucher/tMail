#Main python script for getting emails and texting them to your phone
#First real python script, so stick with me


import sys
import imaplib
import getpass
import email
import email.header
import datetime
import os
from twilio.rest import TwilioRestClient
from bs4 import BeautifulSoup

#twilio stuff
ACCOUNT_SID = "ACf705535b7e3903d62feb8e7a4363959a"
AUTH_TOKEN = "0a1bb44c792d5d5c4d05ea5692cb6d95"
MY_TWILIO_NUMBER = "+16508521029"
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
def send_sms(phone, message):
	client.messages.create(
		body = message,
		to = phone,
		from_ = MY_TWILIO_NUMBER)

user = raw_input("Enter your email:")
pswd = getpass.getpass("Enter your password:")

def processMailbox(M):

	rv, data = M.search(None, "ALL")
	if rv != 'OK':
		print "No messages found!"
		return

	for num in data[0].split():
		rv, data = M.fetch(num, '(RFC822)')
		if rv != 'OK':
			print "Could not fetch message"
			return

        msg = email.message_from_string(data[0][1])
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = unicode(decode[0])
        mailSubject = 'Message subject: %s' % (subject)
        plain = msg.get_payload(True)
        print plain
        #running the HTML through BeautifulSoup
        plain = plain.as_string()
        #plain.br.replace_with("\n")
        soup = BeautifulSoup(plain)
        new = soup.get_text()

        fullMessage = new

        print mailSubject
        print fullMessage
        
        #sending the text
        send_sms("14154307313", mailSubject+fullMessage)
        print "Message sent!"
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
	sys.exit(1)

#listing all the available mailboxes, i.e. Inbox, Spam, etc.
"""rv, mailboxes = M.list()
if rv == "OK":
	print "Mailboxes:"
	print mailboxes"""

#opening the Inbox mailbox
rv, data = M.select("Inbox")
if rv == "OK":
	print "Processing mailbox..."
	processMailbox(M)
	M.close()
else:
	print "Error opening mailbox ", rv

M.logout()
