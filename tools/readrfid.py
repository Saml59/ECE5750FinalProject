# Sam Lee and Shuxian Jiang Final Project ECE 5750
# RFID Authenticated SSH Server

from pynfc import Nfc, Desfire, Timeout
import os, sys, user_util
from selenium.common.exceptions import TimeoutException

n = Nfc("pn532_uart:/dev/ttyS0:115200")

user = os.getenv("USER")
if user == "pi" :
    sys.exit(0)

user_mode = user_util.get_mode(user)
user_mode = user_mode[0][0]

if user_mode is None or user_mode == 'BANNED' :
	print("YOU ARE BANNED")
	exit(1)

rfid_uid = user_util.get_rfid_uid(user)
rfid_uid = rfid_uid[0][0]

print("Scan your RFID card")
for target in n.poll():
	try:
		if (str(target.uid) == rfid_uid) :
			sys.exit(0)
		else :
			sys.exit(1)
		break
	except TimeoutException :
		pass
	except KeyboardInterrupt :
		sys.exit(1)
