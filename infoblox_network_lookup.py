#!/usr/bin/python
import requests, json, os
from getpass import getpass

infoblox_hostname = ""

user = raw_input("Enter username to auth as: ")
passwd = getpass()

'''
print("Type or paste the subnets list. Ctrl-D to save.")
subnets = []
while True:
	try:
		subnet = raw_input("")
	except EOFError:
		break
	subnets.append(subnet)
subnets = [line.strip() for line in subnets if line]
'''

file_path = raw_input("Subnets filename:")
if os.path.exists(file_path):
	subnets = open(file_path, "r").read().splitlines()
	subnets = [line.strip() for line in subnets if line]

print("\n%s\n\tResults\n%s\n" % ("*"*20, "*"*20))
for subnet in subnets:
	req = requests.get("https://%s/wapi/v2.0/network?_return_type=json&network~=%s" % (infoblox_hostname,subnet), auth=(user, passwd), verify=False)
	if len(req.content)>2:
		req_list = json.loads(req.content)
		for network_object in req_list:
			if subnet in network_object["network"]:
				if network_object.has_key("comment"):
					print("%s\t%s" % (network_object["network"], network_object["comment"]))
				else:
					print("%s\tNo Comment" % network_object["network"])
	else:
		print("%s lookup failed." % subnet)

				



