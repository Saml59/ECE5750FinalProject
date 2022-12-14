# Sam Lee and Shuxian Jiang Final Project ECE 5750
# RFID Authenticated SSH Server

import sys, os

SSH_CONFIG = "/etc/ssh/sshd_config"

def ban(user) :
    content = ""

    with open(SSH_CONFIG, "r", encoding='utf-8') as fread:
        content = fread.read()
        fread.seek(0)
        for line in fread:
            if line.startswith("AllowUsers") and user in line:
                newline = line.replace(f" {user}", "")
                content = content.replace(line, newline)

    with open(SSH_CONFIG, 'w', encoding='utf-8') as fwrite:
        fwrite.write(content)
