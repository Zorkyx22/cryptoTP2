import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import json
import base64
import argparse

def add_entry(args):
	print(args)
	print('ADD_FUNCTION')

def list_entries(args):
	print(args)
	print('LIST_FUNCTION')

def discover_entry(args):
	print(args)
	print('DISC_FUNCTION')

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
d_parser.add_argument("-i", help="Sepcify line number to show", required=True, action='store')
d_parser.add_argument("-user", help="Flag used to show user information", required=False, action='store_true')
d_parser.add_argument("-pwd", help="Flag used to show password information", required=False, action='store_true')

#Function to call when d subcommand is used
d_parser.set_defaults(function=discover_entry)

args = parser.parse_args()
args.function(args)