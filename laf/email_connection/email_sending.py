import smtplib

smtp_server = "smtp.gmail.com"
port = 465
username = "lostandfound.webapp@gmail.com"
password = "elspfqqqtfwflwzu"
sender = "Lost and Found <lostandfound.webapp@gmail.com>"
receiver = "Lucie le Blanc <lucieleblanc425@gmail.com>"

message = f"""\
Subject: Hi Lucie
To: {receiver}
From: {sender}

please recieve this."""

try:
    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(username, password)
        server.ehlo()
        server.sendmail(sender, receiver, message)
except(OSError):
    print("Something went wrong, sorry.")