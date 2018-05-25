import sqlite3
import keyring
import getpass


#sql file for username only
conn = sqlite3.connect('Booking_Details.db')


conn.execute('''CREATE TABLE IF NOT EXISTS user
         (NAME           TEXT    NOT NULL);''')



print("It is only one time initialization to secure you Login credentials.\n")

user_name = input('Enter your USERNAME : ')
password = getpass.getpass('Enter you PASSWORD (Hidden) : ')


conn.execute("INSERT INTO user (NAME) \
      VALUES ('{}')".format(user_name))

conn.commit()
print ("User created successfully")
conn.close()
#password is safe with windows vault


#setting to windows vault
keyring.set_password('irctc',user_name,password)