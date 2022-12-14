# Sam Lee and Shuxian Jiang Final Project ECE 5750
# RFID Authenticated SSH Server

import mariadb

userDB = mariadb.connect(
    host="localhost",
    user="root",
    password=""
)

mycursor = userDB.cursor()

mycursor.execute("CREATE DATABASE userDB")

userDB.close()

userDB = mariadb.connect(
    host="localhost",
    user="root",
    password="rootuser",
    database="userDB"

)

mycursor = userDB.cursor()
mycursor.execute("CREATE TABLE users (userid VARCHAR(255), status VARCHAR(255))")
mycursor.execute("INSERT INTO users VALUES (pi, ADMIN)")

userDB.close()
