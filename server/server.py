#!/bin/python3
import socket, time, random, sys, os

#ADDRESS = ('localhost', 8880)
ADDRESS = ('', 8880)
TEAM_NAME = "team-name.txt"
TEAM_RESULT = "team-result.txt"
TIME_FORMAT = '%X %x %Z'
BACKUP_FOLDER = "backup"
BACKUP_FORMAT = '%X %Z'


if not os.path.exists(BACKUP_FOLDER):
    os.mkdir(BACKUP_FOLDER)

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(ADDRESS)
s.listen(0)

while True:
    team_name = open(TEAM_NAME)
    team_name_lines = team_name.readlines()
    team_result = open(TEAM_RESULT)
    team_result_lines = team_result.readlines()

    b = open((BACKUP_FOLDER + '/' + time.strftime(BACKUP_FORMAT)).replace(':', '-'), 'w')
    for i in team_name_lines:
        b.write(i)
    b.write('--------------')
    for i in team_result_lines:
        b.write(i)
    b.close()
    
    print(time.strftime(TIME_FORMAT) + " => " + str(team_name_lines))
    print(time.strftime(TIME_FORMAT) + " => " + str(team_result_lines))

    conn, address = s.accept()
    for i in team_name_lines:
        conn.send(str.encode(i))
    conn.close()
    conn, address = s.accept()
    for i in team_result_lines:
        conn.send(str.encode(i))

    conn.close()
    team_name.close()
    team_result.close()
