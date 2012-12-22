#!/usr/bin/env python

import argparse, urllib.request, sys, os, re, shutil, pyperclip

class Webfonts:
	def __init__(self, url, dir, css):
		self.url = url
		self.dir = dir
		self.css = css

		self.parselink()
		self.download()

	def parselink(self):
		try:
			req = urllib.request.Request(self.url)
		except ValueError as e:
			print('Ongeldige URL ingegeven: ' + self.url)
			sys.exit(0)

		req.add_header('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.101 Safari/537.11')

		try:
			res = urllib.request.urlopen(req)
		except urllib.request.HTTPError as e:
			print(e)
			sys.exit(0)

		self.ret = res.read()

		names = re.findall(r"local\('([^\)]+)'\), url", self.ret.decode('utf8'))
		self.urls = re.findall(r"url\(([^\)]+)\)", self.ret.decode('utf8'))

		self.result = {}
		i = 0
		for n in names:
			self.result[n] = self.urls[i]
			i += 1

		self.generatecss()

	def generatecss(self):
		stylesheet = self.ret.decode('utf8')
		for i in self.result.items():
			filename = i[0] + ".woff"
			directory = i[1].split('/')[-3]
			stylesheet = stylesheet.replace(i[1], os.path.join(self.dir, directory, filename))

		with open(self.css, 'a') as file_out:
			file_out.write(stylesheet)

		pyperclip.copy(stylesheet)

		print('Stylesheet written and copied to clipboard...')

	def download(self):
		if not os.path.exists(self.dir):
			os.makedirs(self.dir)

		for i in self.result.items():
			parts = i[1].split('/')
			filename = i[0] + '.woff'
			directory = parts[-3]

			target = os.path.join(self.dir, directory)

			if not os.path.exists(target):
				os.makedirs(target)

			with urllib.request.urlopen(i[1]) as response, open(os.path.join(target, filename), 'wb') as out_file:
				shutil.copyfileobj(response, out_file)

			print('Downloaded: ' + filename)

		print('Done!')

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Download Google Web Fonts')
	parser.add_argument('--url', dest='url', help='URL from Google Web Fonts')
	parser.add_argument('--dir', dest='dir', help='Directory where to put the fonts')
	parser.add_argument('--css', dest='css', help='Name of the stylesheet')
	args = parser.parse_args()

	if args.url == None:
		parser.print_help()
		sys.exit(0)

	if args.dir == None:
		args.dir = 'fonts'

	if args.css == None:
		args.css = 'fonts.css'

	Webfonts(args.url, args.dir, args.css)
