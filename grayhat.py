#!/usr/bin/env python3
#
# 
#
# grayhat.py - Obtain Google Docs and Sheets for a specified domain that have been found in short urls.
#
# By @RandomRobbieBF
# 
#

import requests
import sys
import argparse
import os.path
import re
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", required=False ,default="",help="URL to test")
parser.add_argument("-f", "--file", default="",required=False, help="File of urls")
parser.add_argument("-p", "--proxy", default="",required=False, help="Proxy for debugging")
parser.add_argument("-o", "--output", default="",required=False, help="Output File to Save Results")

args = parser.parse_args()
url = args.url
urls = args.file
output = args.output


access_token = ""

if args.proxy:
	http_proxy = args.proxy
	os.environ['HTTP_PROXY'] = http_proxy
	os.environ['HTTPS_PROXY'] = http_proxy

	
	
def get_docs(access_token,domain,subdomain):
	print("\n")
	paramsGet = {"access_token":access_token,"keywords":"-forms "+domain+""}
	headers = {"Te":"trailers","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0","Sec-Fetch-Dest":"document","Sec-Fetch-Site":"none","Sec-Fetch-User":"?1","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate","Sec-Fetch-Mode":"navigate"}
	for i in range(0, 50000, 1000):
		r = session.get("https://shorteners.grayhatwarfare.com/api/v1/subdomain/"+subdomain+"/files/"+str(i)+"/1000", params=paramsGet, headers=headers)
		if r.status_code == 404:
			return True
		else:
			rj = json.loads(r.text)
			print("[*] Found "+str(rj['urlsCount'])+" Results for "+subdomain+" [*]")
			for ff in rj['urls']:
				print("[*] Filtering Results [*]\n")
				if domain in ff['url']:
					lin = ("Short URL: "+ff['shortUrl']+"  Long URL: "+ff['url']+"")
					if output:
						text_file = open(output, "a+")
						text_file.write(""+lin+"\n")
						text_file.close()
						print(lin)
					else:
						print(lin)
					


service = ["storage.googleapis.com","firebasestorage.googleapis.com","groups.google.com","spreadsheets.google.com","services.google.com","sites.google.com","docs.google.com","drive.google.com","calendar.google.com","script.google.com","lh3.googleusercontent.com"]


if urls:
	if os.path.exists(urls):
		with open(urls, 'r') as f:
			for line in f:
				url = line.replace("\n","")
				try:
					print("Testing "+url+"")
					for subdomain in service:
						get_docs(access_token,url,subdomain)
				except KeyboardInterrupt:
					print ("Ctrl-c pressed ...")
					sys.exit(1)
				except Exception as e:
					print('Error: %s' % e)
					pass
		f.close()
	

else:
	for subdomain in service:
		get_docs(access_token,url,subdomain)
