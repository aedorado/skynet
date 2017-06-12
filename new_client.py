# 172.19.17.189:10611

import argparse
from Client import Client

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--upload', type=str, help='Upload the specifired file')
parser.add_argument(
    '-s',
    '--search',
    type=str,
    help='Search for the specified file.')
parser.add_argument(
    '-d',
    '--download',
    type=str,
    help='Download the specified file.')

args = parser.parse_args()

print args.upload

if args.upload:
	c = Client()
	c.upload_file(args.upload)

if args.download:
    c = Client()
    c.download_file('10.0.0.4', '1.mp3')