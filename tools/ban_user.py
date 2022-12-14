# Sam Lee and Shuxian Jiang Final Project ECE 5750
# RFID Authenticated SSH Server

import sys, os
import user_util, ban_user_util
SSH_CONFIG = "/etc/ssh/sshd_config"


if (len(sys.argv) < 2) :
	exit("Username input not found")

user_to_remove = sys.argv[1]

user_mode = user_util.get_mode(user_to_remove)
user_mode = user_mode[0]

if (user_mode == "ADMIN")	:
    print("You do not have permission to ban this user")
    quit()

#ban_user_util.ban(user_to_remove)

user_util.set_mode(user_to_remove, "BANNED")
