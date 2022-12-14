# Sam Lee and Shuxian Jiang Final Project ECE 5750
# RFID Authenticated SSH Server

import RPi.GPIO as GPIO
import time, os
import sys, pygame
from pygame.locals import *
import user_util, ban_user_util

start = time.time()
run_for = 3000 #seconds
keep_running = True
started = 1

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()


GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) #button inputs to control motors
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Preferences
size = width, height = 320, 240
pygame.mouse.set_visible(True)

#Fonts
font = pygame.font.Font(None, 32)
user_font = pygame.font.Font(None, 20)
options_font = pygame.font.Font(None, 22)

#Colors
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
purple = 106, 13, 173
screen = pygame.display.set_mode(size)


#Title
user_title = (160, 10)


#User list
user_top = (80, 40)
user_list = []
user_info = {}
first = 0
user_rects = [0]*8
listed_ids = [0]*8
selected = False
selected_user_id = -1
selected_pos = (0, 0, 0, 0)

#Options list level 1
options_top = (220, 40)
options_list1 = ["Info", "Change Permissions", "Kick", "Ban"]
options_surfaces = [options_font.render(option, True, white) for option in options_list1]
options_rects = [options_surfaces[i].get_rect(center=(options_top[0], options_top[1] + (i * 30))) for i in range(len(options_list1))]
selected_option = 0
on_options_list = False

#Change permissions options
perm_list = ["ADMIN", "MODERATOR", "USER", "BANNED"]
colors = [green, blue, white, purple]
perm_surfaces = []
perm_rects = []
selected_perm = 0
on_perm_list = False
def render_permissions(perm) :
	global perm_surfaces, perm_rects
	color = colors[perm_list.index(perm)]
	perm_surfaces = [options_font.render(permission, True, color if permission == perm else white) for permission in perm_list]
	perm_rects = [perm_surfaces[i].get_rect(center=(options_top[0], options_top[1] + (i * 30))) for i in range(len(perm_list))]

#Information List

info_surfaces = []
info_rects = []
on_info_list = False
def render_info(userinf) :
	global info_surfaces, info_rects
	info_surfaces = [options_font.render(key + ": " + str(userinf[key]), True, white) for key in userinf]
	info_rects = [info_surfaces[i].get_rect(center=(options_top[0], options_top[1] + (i * 30))) for i in range(len(userinf))]

def increment_pointer() :
	global on_options_list, on_perm_list
	global selected_option, selected_perm, selected_user_id
	if not on_options_list and not on_perm_list :
		selected_user_id = min(max(listed_ids), selected_user_id + 1)
	elif not on_perm_list and on_options_list :
		selected_option = min(3, selected_option + 1)
	elif on_perm_list :
		selected_perm = min(3, selected_perm + 1)

def decrement_pointer() :
	global on_options_list, on_perm_list
	global selected_option, selected_perm, selected_user_id
	if not on_options_list and not on_perm_list :
		selected_user_id = max(min(listed_ids), selected_user_id - 1)
	elif not on_perm_list and on_options_list :
		selected_option = max(0, selected_option - 1)
	elif on_perm_list :
		selected_perm = max(0, selected_perm - 1)

# start_stop_button = (160, 90)
# left_history = (100, 60)
# right_history = (260, 60)
# lhList = [(90, 90), (90, 130), (90, 170)]
# rhList = [(250, 90), (250, 130), (250, 170)]



user_title_surface = font.render("USERS", True, white)
# stop_surface = font.render("STOP", True, black)
# start_surface = font.render("START", True, black)
# left_history_surface = font.render("Left History", True, white)
# right_history_surface = font.render("Right History", True, white)

user_title_rect = user_title_surface.get_rect(center=user_title)
red_bar = pygame.Rect(0, 20, 320, 5)
# stop_rect = stop_surface.get_rect(center=start_stop_button)
# start_rect = start_surface.get_rect(center=start_stop_button)
# left_history_rect = right_history_surface.get_rect(center=left_history)
# right_history_rect = right_history_surface.get_rect(center=right_history)

screen.blit(user_title_surface, user_title_rect)
pygame.draw.rect(screen, red, red_bar)
# screen.blit(left_history_surface, left_history_rect)
# screen.blit(right_history_surface, right_history_rect)

def get_users() :
	actives = user_util.get_active_users()
	global user_list, user_info, listed_ids
	tmp_lst, tmp_info = [], {}

	for usr in actives :
		tmp_lst.append(usr[1])
		tmp_info[usr[1]] =  {"id": usr[0], "perm": usr[2]}
	if tmp_lst != user_list or tmp_info != tmp_info :
		user_list = tmp_lst
		user_info = tmp_info
	for i in range(min(8, len(tmp_lst))) :
		listed_ids[i] = actives[i][0]

def do_selected_option(user_id, option_id) :
	global user_info, on_info_list, on_perm_list, user_list
	userinf = user_info[get_user_from_id(user_id)]
	usr = usr = get_user_from_id(user_id)
	if (options_list1[option_id] == "Info") :
		render_info(userinf)
		on_info_list = True
		on_perm_list = False
	if (options_list1[option_id] == "Change Permissions") :
		on_perm_list = True
		on_info_list = False
		render_permissions(userinf["perm"])
	if (options_list1[option_id] == "Kick") :
		user_list.remove(usr)
		os.system(f"killall -u {usr}")
		back_to_users()
	if (options_list1[option_id] == "Ban") :
		user_list.remove(usr)
		#DONE: Also kick user from server
		os.system(f"killall -u {usr}")
		#DONE: Also ban the user from the system
		user_util.set_mode(usr, "BANNED")
		back_to_users()
	pass

def back_to_options() :
	global on_info_list, on_perm_list, on_options_list
	on_info_list = False
	on_perm_list = False
	on_options_list = True

def back_to_users() :
	global on_info_list, on_perm_list, on_options_list, selected
	on_info_list = False
	on_perm_list = False
	on_options_list = False
	selected = False

def get_user_from_id(user_id) :
	for user in user_info:
		if user_info[user]["id"] == user_id:
			return user

def GPIO17_callback(channel):
    decrement_pointer()
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback)
def GPIO22_callback(channel):
    increment_pointer()
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback)
def GPIO23_callback(channel):
    sys.exit()
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback)
def GPIO27_callback(channel):
	global selected
	selected = False
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback)


while time.time() - start < run_for and keep_running :
	screen.fill(black)
	buttonPress = False
	for event in pygame.event.get():
		pos = 0, 0
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			buttonPress = True

		if (event.type == KEYUP and event.key == K_BACKSPACE) :
			if (on_perm_list or on_info_list) :
				back_to_options()
			else :
				back_to_users()

		x,y = pos
		colliding = False
		for idx, rect in enumerate(user_rects) :
			if rect == 0 :
				break
			if rect.collidepoint(pos) : #tapped a user
				selected = True
				on_options_list = True
				colliding = True
				selected_option = 0
				selected_user_id = listed_ids[idx]
				select_pos = (rect.left - 3, rect.top - 3, rect.width + 5, rect.height + 4)
		if on_options_list :
			for idx, rect in enumerate(options_rects) :
				if rect.collidepoint(pos):
					if (selected_option == idx):
						do_selected_option(selected_user_id, selected_option)
						on_options_list = False
						pass
					selected_option = idx
		if on_perm_list :
			for idx, rect in enumerate(perm_rects) :
				if rect.collidepoint(pos) :
					if (selected_perm == idx) :
						new_perm = perm_list[idx]
						sel_usr = get_user_from_id(selected_user_id)
						user_util.set_mode(sel_usr, new_perm)
						user_info[sel_usr]["perm"] = new_perm
						render_permissions(perm_list[idx])
					selected_perm = idx

		if buttonPress and not colliding and pos[0] < 100 and pos[0] != 0 :
			selected = False

		# if quit_rect.collidepoint(pos) : #in quit button territory
		# 	keep_running = False
		# 	print("touchscreen quit")
		# elif start_rect.collidepoint(pos) : #in start/stop button territory
		# 	started = started*-1

	#update user lists
	get_users()


	screen.blit(user_title_surface, user_title_rect)
	pygame.draw.rect(screen, red, red_bar)
	if selected :
		pygame.draw.rect(screen, green, select_pos, 2)
		if on_options_list :
			option_rect = options_rects[selected_option]
			option_select_pos = (option_rect.left - 3, option_rect.top - 3, option_rect.width + 5, option_rect.height + 4)
			for option_idx in range(len(options_list1)):
				screen.blit(options_surfaces[option_idx], options_rects[option_idx])
			pygame.draw.rect(screen, blue, option_select_pos, 2)
		elif on_perm_list :
			perm_rect = perm_rects[selected_perm]
			perm_select_pos = (perm_rect.left - 3, perm_rect.top - 3, perm_rect.width + 5, perm_rect.height + 4)
			pygame.draw.rect(screen, blue, perm_select_pos, 2)
			for perm_idx in range(len(perm_list)) :
				screen.blit(perm_surfaces[perm_idx], perm_rects[perm_idx])
		elif on_info_list :
			for info_idx in range(len(info_surfaces)) :
				screen.blit(info_surfaces[info_idx], info_rects[info_idx])


	for i in range(first, min(len(user_list), first + 8)) :
		usr = get_user_from_id(listed_ids[i])
		usr_perm = user_info[usr]["perm"]
		color = colors[perm_list.index(usr_perm)]
		user_surface = user_font.render(user_list[i], True, color)
		user_id = user_info[user_list[i]]["id"]
		user_rect = user_surface.get_rect(center=(user_top[0], user_top[1] + (i * 25)))
		listed_ids[i - first] = user_id
		user_rects[i - first] = user_rect
		screen.blit(user_surface, user_rect)

	pygame.display.flip()




GPIO.cleanup()
