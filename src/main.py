#!/usr/bin/python
import sys
import os

tagsForHeader = ('<h1>', '</h1>')

def findAllOccurences(string, subString):
    start = 0
    indexes = []
    while 1:
        start = string.find(subString, start)
        if start == -1: 
        	return indexes
        indexes.append(start + len(subString))
        start += len(subString)

def generateTableOfContensts(fileName, tableOfContentsName):
	with open(fileName) as myFile:
		data = myFile.read()

	index = data.find(tagsForHeader[0]) if data.find(tagsForHeader[0]) >= 0 else 0

	if data.find('<!--ts-->') >= 0:
		data = data[:data.find('<!--ts-->') + len('<!--ts-->')] + data[data.find('<!--te-->'):]

	else:
		contestTableStructure = tableOfContentsName + '\n=================\n\n<!--ts-->\n\n<!--te-->\n\n'
		
		data = data[:index] + contestTableStructure + data[index:]

	index = data.find('<!--ts-->') + len('<!--ts-->')
	
	headers = []
	
	for i in findAllOccurences(data, tagsForHeader[0]):
	
		header = ''
		j = 0
		while data[i + j: i + j + len(tagsForHeader[1])] != tagsForHeader[1] and i + j < len(data):
			header += data[i+j]
			j += 1
		
		header.replace(',', '|')
		headers.append(header)

	for header in headers:
		line = '\n   * [' + header + '](#' + header.replace(' ', '-') + ')' 
		data = data[:index] + line + data[index:]	
		index += len(line)
		
	with open(fileName, 'w') as myFile:
		myFile.write(data)
			
if __name__ == '__main__':
	
	fileName = str(sys.argv[1]) if len(sys.argv) > 1 else 'README.md'
	tableOfContentsName = str(sys.argv[2]) if len(sys.argv) > 2 else 'Table of Contents'
	
	if (os.path.isfile(fileName)):
		generateTableOfContensts(fileName, tableOfContentsName)
	
	else:
		print('File ' + fileName + ' does not exist!')
