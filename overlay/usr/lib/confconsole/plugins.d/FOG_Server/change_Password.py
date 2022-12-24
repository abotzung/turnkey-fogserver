'''Change FOG web password '''
# Alexandre Botzung <alexandre.botzung@grandest.fr> - dec. 2022

import re
import sys
import time
import getopt
import hashlib
import signal
from libinithooks.dialog_wrapper import Dialog
from os import system
import pymysql
import pymysql.cursors

DEBIAN_CNF = "/etc/mysql/debian.cnf"

class Error(Exception):
    pass

class MySQL:
    def __init__(self):
        system("mkdir -p /var/run/mysqld")
        system("chown mysql:root /var/run/mysqld")

        self.selfstarted = False
        if not self._is_alive():
            self._start()
            self.selfstarted = True

        self.connect()

    def connect(self):
        self.connection = pymysql.connect(
            unix_socket='/run/mysqld/mysqld.sock',
            user='root',
            cursorclass=pymysql.cursors.DictCursor)
        self.connected = True

    def _is_alive(self):
        return system('mysqladmin -s ping >/dev/null 2>&1') == 0

    def _start(self):
        system("mysqld --skip-networking >/dev/null 2>&1 &")
        for i in range(6):
            if self._is_alive():
                return

            time.sleep(1)

        raise Error("could not start mysqld")

    def _stop(self):
        if self.selfstarted:
            system("mysqladmin --defaults-file=%s shutdown" % DEBIAN_CNF)

    def __del__(self):
        self._stop()

    def execute(self, query, interp=None):
        if not self.connected:
            self.connect()

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, interp)
            self.connection.commit()
        finally:
            self.connection.close()
            self.connected = False

def usage(s=None):
    if s:
        print("Error:", s, file=sys.stderr)
    print("Syntax: %s [options]" % sys.argv[0], file=sys.stderr)
    print(__doc__, file=sys.stderr)
    sys.exit(1)

def main():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hu:p:",
                     ['help', 'user='])

    except getopt.GetoptError as e:
        usage(e)

    username="fog"
    password=""
    hostname="localhost"
    queries=[]

    if not password:
        d = Dialog('TurnKey Linux - FOG Configuration')
        password = d.get_password(
            "FOG Password",
            "Please enter new password for FOG Webservice '%s' account." % username)

    m = MySQL()

    pwdresult = hashlib.md5(password.encode())
    # The password are automatically changer after the 1st login
    # set password
    m.execute("update fog.users set uPass='"+pwdresult.hexdigest()+"' where uName='"+username+"';")

def run():
    main()
