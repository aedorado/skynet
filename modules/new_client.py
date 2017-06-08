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
    help='Search for the specified file.')

args = parser.parse_args()

if args.upload:
	c = Client()
	c.upload_file(args.upload)

if args.search:
    c = Client()
    c.query_file(args.search)
	# c.download_file('172.19.17.187', 'new_client.py')
	# c.download_file('172.19.17.188', '1.mp3')