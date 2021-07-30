#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 10:44:58 2021

@author: zachbailey
"""

import requests
from bs4 import BeautifulSoup
import smtplib
import time

# Define local functions

def check_price(URL,header,targetprice,recipient):
    """Checks if current price is less than or equal to target price"""
    
    page = requests.get(URL, headers=header) # connect to the webpage
    soup = BeautifulSoup(page.content, 'lxml') # get the html
    
    title = soup.find(id="title").get_text(strip=True) # find the product title
    price = soup.find(id="priceblock_ourprice").get_text(strip=True) # find the price

    convert_price = int(price[1:-3]) # remove the dollar sign and change

    if convert_price <= targetprice: # when target price is hit, send mail
        send_mail(URL,recipient,title)

def send_mail(URL,recipient,title):
    """Sends email with link to purchase product"""
    
    server = smtplib.SMTP('smtp.gmail.com',587) # connect to gmail servers
    server.ehlo() # say good morning to Lady Google
    server.starttls() # establish a secure connection
    server.ehlo() # say good morning to Lady Google again
    
    server.login("email", "password") # login to email, use app password if 2 factor authentication is on
    subject = f'Target price hit for: {title}' # subject content
    
    body = f'Follow the Link to Buy!: {URL}' # body content
    
    msg = f"Subject: {subject}\n\n{body}" # put it all together in msg format
    
    server.sendmail('boatschoooldropout@gmail.com',recipient,msg) # send email
    print("Email Sent") # alert user 
    
    server.quit() # end server connection
    
# declare function variables
URL = 'https://www.amazon.com/Eureka-Midori-Person-Season-Backpacking/dp/B08QRZ4YDT?ref_=ast_sto_dp&th=1&psc=1'

header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15", "Accept-Language": "en-US,en;q=0.5"}

recipient = "zachary_bailey6@icloud.com"

targetPrice = 200


while(True): # run check price every 10 minutes until targetPrice is found
    check_price(URL,header,targetPrice,recipient)
    time.sleep(600)

