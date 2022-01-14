from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import PyPDF2
from pathlib import Path
#import csv
#import re
from tools import *

def getTextfromHTML(download_url):
    filename = "textFiles/" + str(processFileName(download_url))
    path_filename = Path(filename)
    if(path_filename.is_file()):
        print("\tFile " + str (filename) + " was already downloaded!")
        return filename
    
    file = open(filename, 'w')
    html = urlopen(download_url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    file.write(text)
    file.close()
    return filename

def getTextfromPdf(pdf_file):
    # creating a pdf file object 
    pdfFileObj = open("downloadFiles/" + str(pdf_file), 'rb') 
        
    # creating a pdf reader object 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
        
    # printing number of pages in pdf file 
    print("\tTotal number of pages: " + str(pdfReader.numPages))
    
    print("\tConvert pdf to txt...")
    textFile = "textFiles/" + str(pdf_file) + ".txt"
    path_textFile = Path(textFile)
    if(path_textFile.is_file()):
        print("\tFile already existes!")
        return textFile
    file_out = open(textFile, 'w')
    result = ""
    for i in range(0, pdfReader.numPages):    
        # creating a page object 
        pageObj = pdfReader.getPage(i)
        if('/Contents' in pageObj):
            result += pageObj.extractText()
            if (i % 40 == 0):
                print("\t" + str(i) + " pages")
                file_out.write(result)
                result = ""
    
    # closing the pdf file object 
    pdfFileObj.close() 
    file_out.close()
    return textFile
    
def download_file(download_url):
    filename = "downloadFiles/" + str(processFileName(download_url))
    path_filename = Path(filename)
    if(path_filename.is_file()):
        print("\tFile " + str(filename) + " was already downloaded!")
        return
    response = urllib.request.urlopen(download_url)
    file = open(filename, 'wb')
    file.write(response.read())
    file.close()
    print("\tDownload " + str(download_url) + " Completed!\nWrote to" + str(filename) + "\n")