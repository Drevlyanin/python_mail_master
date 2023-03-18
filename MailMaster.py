import imaplib
import email
import os
import telebot
import time
import shutil

# set up your bot using the bot token provided by BotFather
bot = telebot.TeleBot('')

# set up your email credentials
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('', '')
mail.select('inbox')

# set up a list to keep track of processed message IDs
processed_ids = []

# function to check for new mail and send a message to the bot
def check_mail():
    global processed_ids

    mail.select('inbox')
    _, search_data = mail.search(None, 'UNSEEN')
    mail_ids = search_data[0].split()

    for id in mail_ids:
        if id in processed_ids:
            continue

        _, data = mail.fetch(id, '(RFC822)')
        _, b = data[0]
        msg = email.message_from_bytes(b)

        # extract the sender and subject of the email
        sender = msg['From']
        subject = ''.join([text.encode(encoding or 'utf-8').decode('utf-8') for text, encoding in email.header.decode_header(msg['Subject'])]) if msg['Subject'] else ''



        # send a message to the bot with the email subject
        print("sender:", sender)
        print("subject:", subject)
        if subject:
            bot.send_message(chat_id='', text="Hello, you've got mail from {} with the subject '{}'!".format(sender, subject))
        else:
            bot.send_message(chat_id='', text="Hello, you've got mail from {} with no subject.".format(sender))

        # add the ID of the processed message to the list
        processed_ids.append(id)

# run the check_mail function every 10 minutes
while True:
    check_mail()
    time.sleep(600)

# remove the 'temp' directory and its contents
shutil.rmtree('temp')
