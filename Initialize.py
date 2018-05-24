import keyring
import getpass

print("It is only one time initialization to secure you Login credentials.\n")

username = input('Enter your USERNAME : ')
password = getpass.getpass('Enter you PASSWORD (Hidden) : ')


keyring.set_password('irctc',username,password)