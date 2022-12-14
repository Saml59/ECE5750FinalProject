# Sam Lee and Shuxian Jiang Final Project ECE 5750
# RFID Authenticated SSH Server

import os
import sys
import user_util

if (len(sys.argv) < 2) :
	exit("Username input not found")

user_to_kick = sys.argv[1]
calling_user = os.getenv("USER")

if (user_util.get_mode(calling_user) != "USER" and user_util.get_mode(user_to_kick) != "ADMIN")	:
	os.system(f"sudo killall -u {user_to_kick}")
else :
	print("Cannot kick this user")
