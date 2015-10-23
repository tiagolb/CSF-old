#!/usr/bin/env python
import argparse
import sys
import re

def main():
	#Argument Parsing & Program Info
	parser = argparse.ArgumentParser(prog='strings')
	parser.add_argument('--version', action='version', version='%(prog)s 1')
	parser.add_argument('-f', '--file', nargs=1, required=True, help='Raw memory dump file.')
	args = parser.parse_args()
	
	processDump(args.file[0])


def processDump(dumpFile):
	rawDump = open(dumpFile)
	f = open('stringDump', 'w')
	
	for found_str in re.findall("[^\x00-\x1F\x7F-\xFF]{50,}", rawDump.read()):
		f.write(found_str + "\n")

	f.close()
	rawDump.close()	


if __name__ == "__main__":
	main()