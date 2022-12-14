# Sam Lee and Shuxian Jiang Final Project ECE 5750
# RFID Authenticated SSH Server

import os, sys, user_util

if (len(sys.argv) < 3) :
	exit("Username input not found")

user_to_change = sys.argv[1]
new_mode = sys.argv[2]

user_mode = user_util.get_mode(os.getenv("USER"))
user_mode = user_mode[0]
user_to_change_mode = user_util.get_mode(user_to_change)
user_to_change_mode = user_to_change_mode[0]

if user_mode == "ADMIN" or (user_mode == "MODERATOR" and (user_to_change_mode != "ADMIN" and new_mode != "ADMIN"))	:
    user_util.set_mode(user_to_change, new_mode)
