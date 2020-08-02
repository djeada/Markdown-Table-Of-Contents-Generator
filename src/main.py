#!/usr/bin/python
import sys

contestTableStructure = 'Spis Treści \n=================\n\n<!--ts-->\n\n<!--te-->\n'

def findAllOccurences(a_str, sub):
    start = 0
    indexes = []
    while 1:
        start = a_str.find(sub, start)
        if start == -1: 
        	return indexes
        indexes.append(start + len(sub))
        start += len(sub)

def generateTableOfContensts(fileName):
	with open(fileName) as myFile:
		data = myFile.read()

	if data.find("<!--ts-->") >= 0:
		print('Table of contents is already there')

	else:
		index = data.find("<h1>")

		if index >= 0:
		
			data = data[:index] + contestTableStructure + data[index:]

			index = data.find('<!--ts-->') + len('<!--ts-->')
			
			headers = []
			
			for i in findAllOccurences(data, '<h1>'):
			
				header = ''
				j = 0
				while data[i + j: i + j + len('</h1>')] != '</h1>' and i + j < len(data):
					header += data[i+j]
					j += 1
					
				headers.append(header)
		
			for header in headers:
				line = '\n\t* [' + header + '](#' + header.replace(' ', '-') + ')' 
				data = data[:index] + line + data[index:]	
				index += len(line)
				
			with open("README.md", "w") as myFile:
				myFile.write(data)
			
if __name__ == "__main__":
	fileName = str(sys.argv[1]) if len(sys.argv) > 1 else "README.md"
	generateTableOfContensts(fileName)
