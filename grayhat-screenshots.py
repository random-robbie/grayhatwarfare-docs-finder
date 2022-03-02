#!/usr/bin/env python3
#
# 
#
# grayhat-screenshot.py - Grab Screenshots from the short urls 
#
# By @Random-Robbie
# 
#


import sys
import argparse
import os.path
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="",required=False, help="File of urls")
parser.add_argument("-p", "--proxy", default="",required=False, help="Proxy for debugging")


args = parser.parse_args()
urls = args.file



access_token = ""
options = webdriver.ChromeOptions()
options.headless = True




if args.proxy:
	http_proxy = args.proxy
	os.environ['HTTP_PROXY'] = http_proxy
	os.environ['HTTPS_PROXY'] = http_proxy



if urls:
	if os.path.exists(urls):
		with open(urls, 'r') as f:
			for line in f:
				url = line.replace("\n","")
				try:
					driver = webdriver.Chrome(options=options)
					URL = url.split(" ")
					longurl = URL[5].replace("URL:","")
					shorturl = URL[2].split("/")
					print(shorturl[3])
					driver.get(longurl)
					driver.implicitly_wait(20)
					driver.save_screenshot('screenshots/'+shorturl[3]+'.png')
					driver.quit()
				except KeyboardInterrupt:
					print ("Ctrl-c pressed ...")
					sys.exit(1)
				except Exception as e:
					print('Error: %s' % e)
					pass
		f.close()
