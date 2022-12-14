# Sam Lee and Shuxian Jiang Final Project ECE 5750
# RFID Authenticated SSH Server


import os, sys, select, subprocess
import threading

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

def deletePrevline() :
    sys.stdout.write(CURSOR_UP_ONE)
    sys.stdout.write(ERASE_LINE)

class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, name='user-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            inp = input()
            if (inp == "QUIT") :
                os._exit(0)
            self.input_cbk(inp) #waits to get input + Return
            cmd = f'echo "{inp}" > {sendpath}'
            subprocess.check_output(cmd, shell=True)

class ReceieveThread(threading.Thread):

    def __init__(self, input_cbk = None, name='user-receieve-thread'):
        self.input_cbk = input_cbk
        super(ReceieveThread, self).__init__(name=name)
        self.start()

    def run(self):
        with open(receivepath, 'r') as inputFIFO :
            while True:
                i, _, _ = select.select([inputFIFO], [], [inputFIFO])
                if i :
                    data = inputFIFO.read()
                    if (data != "") :
                        self.input_cbk(data)


def print_user1_input(inp):
    deletePrevline()
    print(f'{user1}: {inp}')

def print_user2_input(inp) :
    print(f'{user2}: {inp}')

if (len(sys.argv) < 2) :
	exit("Username input not found")

user2 = sys.argv[1]
user1 = os.getenv('USER')
sendpath = f'chatfiles/{user1}_{user2}.fifo'
receivepath = f'chatfiles/{user2}_{user1}.fifo'

os.system("umask 0")

print("opening write")
if not os.path.exists(sendpath) :
    sendfile = os.mkfifo(sendpath)

print("opening read")
if not os.path.exists(receivepath) :
    receivefile = os.mkfifo(receivepath)

os.system("clear")
print(f"Chat between {user1} and {user2}")

user1Thread = KeyboardThread(print_user1_input)
user2Thread = ReceieveThread(print_user2_input)

while True :
    pass
