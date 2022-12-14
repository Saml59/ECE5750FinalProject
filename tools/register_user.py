# Sam Lee and Shuxian Jiang Final Project ECE 5750
# RFID Authenticated SSH Server

import os, sys, user_util
from pynfc import Nfc, Desfire, Timeout
from selenium.common.exceptions import TimeoutException

if (len(sys.argv) < 2) :
	exit("Username input not found")

user_to_add = sys.argv[1]

SSH_CONFIG = "/etc/ssh/sshd_config"
content = ""

os.system(f"usermod -G dialout -a {user_to_add}")
os.system(f"usermod -G students -a {user_to_add}")


# with open(SSH_CONFIG, "r", encoding='utf-8') as fread:
    # content = fread.read()
    # fread.seek(0)
    # for line in fread :
        # if line.startswith("AllowUsers") and user_to_add not in line:
            # newline = line[0:len(line) - 1] + f" {user_to_add}\n"
            # content = content.replace(line, newline)
# with open(SSH_CONFIG, 'w', encoding='utf-8') as fwrite:
    # fwrite.write(content)

n = Nfc("pn532_uart:/dev/ttyS0:115200")

print("Scan your RFID card")
rfiduid = ''
for target in n.poll():
	try:
		rfiduid = str(target.uid)
		break
	except TimeoutException :
		pass


user_util.add_user(user_to_add, uid=rfiduid)
