import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import json
import base64
import argparse
import hashlib

#Encrypt data using AES-CBC-128
def encrypt(secret, data, IV):
	cipher = AES.new(hashlib.md5(secret.encode("utf-8")).digest(), AES.MODE_CBC, IV)
	return cipher.encrypt(pad(data.encode("utf-8"), AES.block_size))

#Decrypt data using AES-CBC-128
def decrypt(secret, data, IV):
	cipher = AES.new(hashlib.md5(secret.encode("utf-8")).digest(), AES.MODE_CBC, IV)
	try:
		retour = unpad(cipher.decrypt(data), AES.block_size)
	except (ValueError):
		retour = "ACCES DENIED\t"
	return retour


def makeJSONSerializable(data):
	return str(base64.b64encode(data))


def ReadJSONSerialized(data):
	return base64.b64decode(data[2:-1].encode('utf-8'))

#Function to be called on 'a' subcommand usage
def add_entry(LocalArgs):
	localUrl = LocalArgs.url
	localUser = LocalArgs.user
	localPwd = LocalArgs.pwd
	IV = get_random_bytes(16)

	if(os.path.exists("trousse.json")):
		with open("trousse.json", 'r') as f:
			entries = json.load(f)
	else:
		entries = list()
	entry = {
		'IV': makeJSONSerializable(IV),
		'data': {
				'url':makeJSONSerializable(encrypt(LocalArgs.secret, localUrl, IV)), 
				'user':makeJSONSerializable(encrypt(LocalArgs.secret, localUser, IV)),
				'pwd':makeJSONSerializable(encrypt(LocalArgs.secret, localPwd, IV))
			}
	}
	entries.append(entry)
	with open("trousse.json", 'w') as f:
		json.dump(entries, f)

def formatList(i, url, usr, pwd):
	print("{0}\t{1}\t{2}\t{3}".format(i, url, usr, pwd))

#Function to be called on 'l' subcommand usage
def list_entries(LocalArgs):
	with open("trousse.json", 'rb') as f:
		entries = json.load(f)
	ctr = 0
	formatList("index", "url", "\t\tuser", "\tpwd")

	for e in entries:
		formatList(ctr, decrypt(LocalArgs.secret, ReadJSONSerialized(e['data']['url']), ReadJSONSerialized(e['IV'])), "*****", "\t*****")
		ctr+=1

#Function to be called on 'd' subcommand usage
def discover_entry(LocalArgs):
	with open("trousse.json", 'rb') as f:
		entries = json.load(f)
	formatList("index", "url", "\t\tuser", "\tpwd")

	entry = entries[LocalArgs.i]
	IV = ReadJSONSerialized(entry['IV'])
	url = decrypt(LocalArgs.secret, ReadJSONSerialized(entry['data']['url']), IV)
	user = decrypt(LocalArgs.secret, ReadJSONSerialized(entry['data']['user']), IV) if LocalArgs.user else "*****"
	pwd = decrypt(LocalArgs.secret, ReadJSONSerialized(entry['data']['pwd']), IV) if LocalArgs.pwd else "\t*****"

	formatList(LocalArgs.i, url, user, pwd)

#Parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

#Parser for the a subcommand
a_parser = subparsers.add_parser('a', help="Add a new entry to your kit", usage='ex2.py a [-h] SECRET -url URL -user USER -pwd PASSWORD')

#Arguments for the a subcommand
a_parser.add_argument(dest="secret", help="Enter secret key")
a_parser.add_argument("-url", dest="url", help="Specify the url of a new entry", required=True)
a_parser.add_argument("-user", dest="user", help="Specify user of new entry", required=True)
a_parser.add_argument("-pwd", dest="pwd", help="Specify password of new entry", required=True)

#Function to call when a subcommand is used
a_parser.set_defaults(function=add_entry)

#Parser for the l subcommand
l_parser = subparsers.add_parser('l', help="Show all information in kit. Hides user and pwd", usage='ex2.py l [-h] SECRET')

#Argument for the l subcommand
l_parser.add_argument(dest="secret", help="Enter secret key")

#Function to call when l subcommand is used
l_parser.set_defaults(function=list_entries)

#Parser for the d subcommand
d_parser = subparsers.add_parser('d', help="Show information from specific line in kit", usage='ex2.py d [-h] SECRET -i LINE_NUMBER [-user] [-pwd]')

#Arguments for the d subcommand
d_parser.add_argument(dest="secret", help="Enter secret key")
d_parser.add_argument("-i", type=int, help="Sepcify line number to show", required=True, action='store')
d_parser.add_argument("-user", help="Flag used to show user information", required=False, action='store_true')
d_parser.add_argument("-pwd", help="Flag used to show password information", required=False, action='store_true')

#Function to call when d subcommand is used
d_parser.set_defaults(function=discover_entry)

args = parser.parse_args()
args.function(args)