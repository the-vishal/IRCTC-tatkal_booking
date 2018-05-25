from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import keyboard
import time
import sqlite3
import keyring
from win10toast import ToastNotifier



#***********************************************************

#journey details

from_station = 'AMBALA CANT JN - UMB'
to_station ='VARANASI JN - BSB'
date = '26-05-2018'
train_no = '13152'
class_ = '3A'
quota = 'GN'
phone_no = '9115XXXXXX'



#passengers details [Name, age, gender ,birth_choice]
passenger_details = [
    ['VISHAL KUMAR','20','M','LB'],
    ['VIKAS KUMAR','24','M','LB']
    ]




#***********************************************************


def captcha_msg():
    toaster = ToastNotifier()
    toaster.show_toast(title='IRCTC',msg='Enter CAPTCHA value', icon_path='train1.ico')



#***********************************************************
#login details in keyring module
conn = sqlite3.connect('Booking_Details.db')
cursor = conn.cursor()

cursor.execute('''SELECT NAME FROM user''')
user = cursor.fetchall()[0][0]
conn.close()

pasw = keyring.get_password('irctc', user)


#gender xpaths
gender = {
                 'F':'//*[@id="addPassengerForm:psdetail:1:psgnGender"]/option[2]',
                 'M':'//*[@id="addPassengerForm:psdetail:1:psgnGender"]/option[3]',
                 'T':'//*[@id="addPassengerForm:psdetail:1:psgnGender"]/option[4]'}


#births xpaths
birth_pref = {
                        'LB':'//*[@id="addPassengerForm:psdetail:0:berthChoice"]/option[2]',
                        'MB':'//*[@id="addPassengerForm:psdetail:0:berthChoice"]/option[3]',
                        'UP':'//*[@id="addPassengerForm:psdetail:0:berthChoice"]/option[4]',
                        'SL':'//*[@id="addPassengerForm:psdetail:0:berthChoice"]/option[5]',
                        'SU':'//*[@id="addPassengerForm:psdetail:0:berthChoice"]/option[6]'}


#initializing driver
browser = webdriver.Chrome()
url ="https://www.irctc.co.in/eticketing/loginHome.jsf"

#opening url
browser.get(url)

#filling login section
username = browser.find_element_by_name("j_username")
username.send_keys(user)

password = browser.find_element_by_name("j_password")
password.send_keys(pasw)

#presses tab key to goto captcha entry
password.send_keys(Keys.TAB)

captcha_msg()

#for captcha entering, press enter after entering captcha or wait for click
while True:
    if keyboard.is_pressed('enter'):
        browser.find_element_by_xpath('//*[@id="loginbutton"]').click()
        break

    elif  browser.title=='E-Ticketing':
        break
# login complete




#Filling the journey Planner
from_ = browser.find_element_by_name("jpform:fromStation")
from_.send_keys(from_station)


to_ = browser.find_element_by_name("jpform:toStation")
to_.send_keys(to_station)


date_ = browser.find_element_by_name("jpform:journeyDateInputDate")
date_.send_keys(date)



#plan journey form submit
browser.find_element_by_name("jpform:jpsubmit").click()

#Check quota radio button to Tatkal
browser.find_element_by_xpath('//*[@id="qcbd"]/table/tbody/tr/td[6]/input').click()

#select class
cls= []
for i in browser.find_elements_by_link_text(class_):
      cls.append(  i.get_attribute("id"))

class_select =None
for result in cls:
    if train_no in result.split('-'):
        class_select = '//*[@id="'+result+'"]'


browser.find_element_by_xpath(class_select).click()


#Book now
#**************** Boht time lga is section ko krne me :) ***********************
time.sleep(1) #wait for book now link to be generated
# xpath="(//a[contains(text(),'Book Now')])[2]"
# browser.find_element_by_xpath(xpath).click()
browser.find_element_by_link_text('Book Now').click()


#pehle ye kiya tha, click khud karo :
# while True:
#     if browser.title == 'Book Ticket - Passengers Information':
#         break



info_index=0 #name,age,gender,birth in passenger_details list

#fill name of all the passengers
for passg in browser.find_elements_by_xpath("//*[@class='input-style1 psgn-name']"):
           passg.send_keys(passenger_details[info_index][0])
           info_index+=1
           if info_index == len(passenger_details):
               info_index=0
               break


#fill age of all the passengers
for pass_age in  browser.find_elements_by_xpath('//*[@class="input-style1 psgn-age only-numeric"]'):
         pass_age.send_keys(passenger_details[info_index][1])
         info_index += 1
         if info_index == len(passenger_details):
             info_index = 0
             break


#fill gender of all the passengers
for pass_gender in browser.find_elements_by_xpath('//*[@class="input-style1 psgn-gender"]'):
      pass_gender.send_keys(passenger_details[info_index][2])
      info_index += 1
      if info_index == len(passenger_details):
          info_index = 0
          break


#fill birth choice of all the passengers
for pass_birth in browser.find_elements_by_xpath('//*[@class ="input-style1 psgn-berth-choice"]'):
        pass_birth.send_keys(passenger_details[info_index][3])
        info_index += 1
        if info_index == len(passenger_details):
            info_index = 0
            break



#fill phone number on which ticket message is sent
ticket_phone_no = browser.find_element_by_xpath('//*[@class="textfield01 mobile-number only-numeric"]')
ticket_phone_no.clear()
ticket_phone_no.send_keys(phone_no)


captcha_msg()


#take to the captcha input if input captcha else in click captcha pass
try:
    captcha = browser.find_element_by_xpath('//*[@id="nlpAnswer"]')
    captcha.click()
except:
    pass



#ENTER CAPTCHA AND HIT ENTER or wait for a click
while True:
    if keyboard.is_pressed('enter'):
        break

    elif browser.title == 'Book Ticket - Journey Summary':
        break


#Payment Section
browser.find_element_by_id('AGGREGATOR').click()
browser.find_element_by_name('AGGREGATOR').click()
browser.find_element_by_xpath('//*[@id="validate"]').click()
