# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import requests
import os
import sys
import re
import argparse
from openpyxl import load_workbook
users=[]
def getUser(path):
    wb=load_workbook(path)
    sheet = wb.worksheets[0]
    rows = sheet.rows
    for row in rows:
        line = [col.value for col in row]
        users.append(line)
    return users
def check(user):
    if user[0]!=None and user[1]!=None:
        global url 
        options=webdriver.ChromeOptions()
        options.set_headless()
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(options=options)
        browser.get(url)
        browser.refresh()
        username = browser.find_element_by_id("username")
        password = browser.find_element_by_id('password')
        username.send_keys(str(user[0]))
        password.send_keys(str(user[0])[-6:])
        sys.stdout.flush()
        browser.find_element_by_id("submitButton").click()
        div = browser.find_element_by_tag_name("div")
        x = div.find_element_by_class_name("login-box-body")
        a = x.find_element_by_tag_name("a")
        if user[1] == a.get_attribute('href'):
            print "%s is OK" %(user[0])
        elif regux(user[1]) == regux(a.get_attribute('href')):
            print "%s is OK ,expected: %s ,but: %s" %(user[0],user[1],a.get_attribute('href'))
        else:
            print "%s is not OK !!!!! %s is not equal to %s" %(user[0],user[1],a.get_attribute('href'))
        sys.stdout.flush()
        browser.close()
    else:
        pass
def regux(filed): 
    ans = re.findall(".*github.com/([^ /])",filed)
    return ans
def main(argv):
    parser = argparse.ArgumentParser(description='Test github Id')
    
    print '\n'
    print('----------Test github Id-------------')
    print('|       ------          ||          |')
    print('|         ||            ||          |')
    print('|         ||            ||          |')
    print('|         ||      /-----||          |')
    print('|         ||      |     ||          |')
    print('|         ||      |     ||          |')
    print('|       ------    \------/          |')
    print('----------Test github Id--------wyz--')
    print '\n'
    sys.stdout.flush()
    parser.add_argument('-f', help='Specify absolute or relative filepath. Usage: -f \'<filepath>\'')
	
    parser.add_argument('-u', help='Specify url. default url is https://psych.liebes.top/st. Usage: -u \'<url>\'', default="https://psych.liebes.top/st")
	
    parser.add_argument('-i', help='Specify single data. Usage: -i \'<number>\' default  1st',type=int)
	
    parser.add_argument('-w', help='Specify data from which row,default 1st', default=1,type=int)
	
    args = parser.parse_args()
    global url
    if len(sys.argv) < 2 or args.f==None:
		parser.print_help()
    else:
        path = args.f
        url = args.u
        payload = getUser(path)
        try:
            if args.i:
                check(payload[args.i-1]) 
            elif args.w:
                for user in payload[args.w-1:]:
                    check(user)
            else :
                for user in payload:
                    check(user)
        except:
			pass
            
if __name__ == '__main__':

    main(sys.argv[1:])
