#!/usr/bin/env python

import argparse, urllib.request, sys, os, re, shutil, pyperclip

def parselink(url):
	req = urllib.request.Request(url)
	req.add_header('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.101 Safari/537.11')
	res = urllib.request.urlopen(req)
	ret = res.read()

	names = re.findall(r", local\('([^\)]+)'\)", ret.decode('utf8'))
	urls = re.findall(r"url\(([^\)]+)\)", ret.decode('utf8'))

	result = {}
	i = 0
	for n in names:
		result[n] = urls[i]
		i += 1

	generatecss(result, ret.decode('utf8'))

	return result

def generatecss(urls, stylesheet):
	for i in urls.items():
		filename = i[0] + ".woff"
		directory = i[1].split('/')[-3]
		stylesheet = stylesheet.replace(i[1], 'fonts/'+directory+'/'+filename)

	with open('fonts.css', 'a') as file_out:
		file_out.write(stylesheet)

	pyperclip.copy(stylesheet)

	print('Stylesheet written and copied to clipboard...')

def download(urls):
	if not os.path.exists('fonts'):
		os.makedirs('fonts')

	for i in urls.items():
		parts = i[1].split('/')
		filename = i[0] + '.woff'
		directory = parts[-3]

		if not os.path.exists('fonts/' + directory):
			os.makedirs('fonts/' + directory)

		with urllib.request.urlopen(i[1]) as response, open('fonts/' + directory + '/' + filename, 'wb') as out_file:
			shutil.copyfileobj(response, out_file)

		print('Downloaded: ' + filename)

	print('Done!')

def main():
	parser = argparse.ArgumentParser(description='Download Google Web-fonts')
	parser.add_argument('--url', dest='url', help='URL from Google Web-fonts')
	args = parser.parse_args()

	if args.url == None:
		parser.print_help()
		sys.exit(0)

	urls = parselink(args.url)
	download(urls)

if __name__ == '__main__':
	main()
