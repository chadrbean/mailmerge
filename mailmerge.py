import csv
import smtplib
import easyimap
import sys
import random
import time
from email.message import EmailMessage #https://docs.python.org/3/library/email.message.html or https://realpython.com/python-send-email/ or http://blog.magiksys.net/generate-and-send-mail-with-python-tutorial or https://alysivji.github.io/sending-emails-from-python.html
from email.header import Header  #Needed to format the From Address
from email.utils import formataddr #Needed to format the from address
from email.mime.text import MIMEText 

def open_csv():
    with open("imports/import.csv", "r") as fr:
        email_file = fr.readlines()
        header = ["firstname", "lastname", "email"]
        csvr = csv.reader(email_file, delimiter = ",",)
        #skip header
        next(csvr)
        return csvr

def email_login(): 
    email_server = smtplib.SMTP("smtp.gmail.com", 587)
    email_server.ehlo()
    email_server.starttls()
    email_server.login("username", "password")

    
    return email_server
    



email_files = open_csv()
email_server = email_login()

init_bdy_1_file = "merge_templates/initial_email/initial_body_1.txt"
init_sub_file = "merge_templates/initial_email/initial_subject.txt"
already_contacted_file = "database/already_contacted.txt"
already_contacted = []
with open(init_bdy_1_file, "r") as init_bdy_1_read, open(init_sub_file, "r") as init_sub_read, open(already_contacted_file, "r") as already_contacted_read:
    init_bdy_1 = init_bdy_1_read.readlines()
    init_sub = init_sub_read.readlines()
    for email in already_contacted_read:
        already_contacted.append(email.strip("\n"))

first_count_catch = 1
for email in email_files:   
    with open(already_contacted_file.strip(".txt")+"_failed.txt", "r") as already_contacted_failed_read:
        already_contacted_failed = []
        [already_contacted_failed.append(email.strip("\n")) for email in already_contacted_failed_read]
    with open(already_contacted_file.strip(".txt")+"_failed.txt", "a") as already_connected_failed_append:
        if email[2] not in already_contacted or email[2] == "crb4u@yahoo.com":
            try:
                generate_init_body_1 = init_bdy_1[random.randint(0,len(init_bdy_1)-1)].strip("\n")
                msg_text = f"""Hi {email[0]},\n\n{generate_init_body_1}\n\nOur product database consists of 10mil contacts. Each record in our dataset is validated, and current work experience verified on a monthly cycle. If an email address comes back in-valid we remove the record until we can locate and validate a new email for the user.\n\nData can be accessed through our API for on-demand record retrieval. Each profile will come with a "Precise Profile" id which we can use to deliver regular profile updates and email validation changes. The other method, typically used for lower volume requests, would be to send us a set of criteria you would like us to pull, and we can deliver the profiles in a flat-file format of your choosing.\n\nOur pricing depends on volume and is done on a quote basis. We do give volume-based discounts for customers with larger data requirements.\n\nI have some great metrics put together that gives a break down of our data by country, industry, and c-level. Can I send this more detailed information over for your review?\n\n\nRegards,\n\nChad Bean - CEO\nPrecise Profile LLC\nTel: 541-887-0108\n """   
                # msg_html = MIMEText("""""") # Still trying to figure this out.
                msg = EmailMessage()
                generate_subj = init_sub[random.randint(0,len(init_sub)-1)].strip("\n") #f-string below cannot include a backslash which i need to clean up new line
                msg['Subject'] = f'{generate_subj}'
                msg['To'] = f'{email[2]}'
                msg['From'] = str(Header('Chad Bean <chad@preciseprofile.com>'))
                msg.set_content(msg_text)   #attached the message content
                # if msg_html is not None:  #Working on this html part
                #     msg.add_alternative(msg_html, subtype='html')
                print(email)
                print(msg)
                email_server.send_message(msg)
                if first_count_catch == 1:
                    input("Check message first before sending. Press Enter to continue and control+z to exit")
                first_count_catch +=1
                #save emailed contacts to database
                with open(already_contacted_file, "a") as fa:
                    fa.write("\n"+email[2])
                time.sleep(random.randint(180, 300))
            except:
                if email[2] not in already_contacted_failed:
                    already_connected_failed_append.write("\n"+email[2])
                    break
        else:
            if email[2] not in already_contacted_failed:
                already_connected_failed_append.write("\n"+email[2])
