import requests
import re
import win32com.client


# make sure that the path exists, program won't create that automatically!
# (file will be created anyways)
csv_path = "dataset/ips.csv"
# creates an empty file if doesn't exist at given path
open(csv_path, mode='a+', encoding='utf-8').close()
old_ips = []

# function to open existing file into memory for duplicate checking


def loadPreviousFile():
    global old_ips
    file_data = open(csv_path, mode='a+', encoding='utf-8').read().split('\n')
    for line in file_data:
        if line.strip() != '':
            old_ips.append(line.strip())

# function to check if the entry is a duplicate


def is_duplicate(address):
    global old_ips
    if address in old_ips:
        return True
    else:
        return False

# function to check if the ip format is a ipv4 format


def is_ipv4(address):
    return len(re.findall(r'[\d]+\.[\d]+\.[\d]+\.[\d]+', address)) > 0


# function to check latest update on the website


def getTodaysUpdate():
    link = "https://www.dan.me.uk/torlist/?exit"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    resp = requests.get(link, headers=headers).text
    resp = resp.split('\n')
    with open(csv_path, mode='a+', encoding='utf-8') as final_file:
        for line in resp:
            if is_ipv4(line) and not is_duplicate(line):
                final_file.write(line + "\n")
                print("Wrote {} into file".format(line))


# function to send email
def sendEmail(filenames):
    outlook = win32com.client.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = ''
    mail.Subject = ''
    mail.Body = ''
#   mail.HTMLBody = '<h2>HTML Message body</h2>' #this field is optional

    # To attach file to the email (optional):
    for filename in filenames:
        attachment = filename
        mail.Attachments.Add(attachment)

    mail.SentOnBehalfOfName = ''
    mail.Send()
    print("Email sent ...")


if __name__ == "__main__":
    loadPreviousFile()  # reads previous data into memory so that duplicates can be removed
    getTodaysUpdate()  # checks and saves the update to csv file
    # since our file is appended with new IP addresses, let's send the email
    sendEmail(csv_path)
