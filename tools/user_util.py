# Sam Lee and Shuxian Jiang Final Project ECE 5750
# RFID Authenticated SSH Server

import mariadb, subprocess, re, os

modes = ["ADMIN", "MODERATOR", "USER", "BANNED"]

def connect_server() :
    return mariadb.connect(
        host="localhost",
        user="root",
        password="",
        database="userDB"

    )
def add_user(username, mode="USER", uid='') :
    assert mode in modes
    userDB = connect_server()
    mycursor = userDB.cursor()

    values = (username, mode, uid)
    mycursor.execute("INSERT INTO users (userid, status, rfid) VALUES (%s, %s, %s)", values)
    userDB.commit()
    userDB.close()

def create_table() :
    userDB = connect_server()
    mycursor = userDB.cursor()
    mycursor.execute("CREATE TABLE users (userid VARCHAR(255), status VARCHAR(255), rfid VARCHAR(255))")
    userDB.commit()
    values = ("pi", "ADMIN", str(b'9bc9ee34'))
    mycursor.execute("INSERT INTO users (userid, status, rfid) VALUES (%s, %s, %s)", values)
    userDB.commit()
    userDB.close()

def get_users():
    userDB = connect_server()

    mycursor = userDB.cursor()

    mycursor.execute("SELECT id, userid, status, rfid FROM users")

    result = mycursor.fetchall()

    userDB.close()
    return result

def get_mode(username) :
    userDB = connect_server()

    mycursor = userDB.cursor()

    mycursor.execute(f"SELECT status FROM users WHERE userid=%s", (username,))
    result = mycursor.fetchall()
    userDB.close()
    return result

def get_rfid_uid(username) :
    userDB = connect_server()

    mycursor = userDB.cursor()

    mycursor.execute(f"SELECT rfid FROM users WHERE userid=%s", (username,))
    result = mycursor.fetchall()
    userDB.close()
    return result

def set_mode(username, mode) :
    userDB = connect_server()

    mycursor = userDB.cursor()
    old_mode = get_mode(username)
    old_mode = old_mode[0][0]

    if mode == 'ADMIN' :
        os.system(f'usermod -G sudo -a {username}')
    elif old_mode == 'ADMIN' :
        os.system(f'gpasswd --delete {username} sudo')

    mycursor.execute(f"UPDATE users SET status=%s WHERE userid=%s", (mode, username))
    userDB.commit()
    userDB.close()

def show_tables() :
    userDB = connect_server()

    mycursor = userDB.cursor()

    mycursor.execute("SHOW TABLES")
    result = mycursor.fetchall()
    userDB.close()

def get_active_users() :
    who_result = subprocess.run(['who'], stdout=subprocess.PIPE)
    regex = "^(\w+)"
    users = re.findall(regex, who_result.stdout.decode('utf-8'), flags=re.MULTILINE)
    users = "'" + "', '".join(users) + "'"
    userDB = connect_server()

    mycursor = userDB.cursor()
    mycursor.execute(f"SELECT id, userid, status, rfid FROM users WHERE userid IN ({users})")

    result = mycursor.fetchall()
    userDB.close()

    return result
