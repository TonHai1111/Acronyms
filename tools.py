#from urllib.request import urlopen
#from bs4 import BeautifulSoup
#import urllib.request
#import PyPDF2
#from pathlib import Path
import csv
import re
import json

def processFileName(filename):
    if(filename.rfind('/') == len(filename) - 1):
        filename = filename[:filename.rfind('/')]
    # Some exceptions
    if(filename == "https://swe.ssa.esa.int/glossary"):
        filename = "swe.ssa.esa.int_glossary"
    elif(filename == "https://science.nasa.gov/glossary"):
        filename = "science.nasa.gov_glossary"
    elif(filename == "https://spacewx.com/glossary"):
        filename = "spacewx.com_glossary"
    
    result = filename[filename.rfind('/') + 1:]
    return result

def checkAcronym(value): 
    return checkAcronym_v2(value, "config.json")
    #return checkAcronym_v1(value)

def checkAcronym_v1(value): #All upper case, no space in between, no number, not a Roman number
    value = value.lstrip()
    if(value.find(' ') >= 0): #no space
        return False
    for character in value:
        if character.isdigit():#no digit
            return False
    if(bool(re.search(r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$",value))): # not a Roman number
        return False
    if(value.isupper()):
        return True
    else:
        return False

'''
An example:
{
    "upperCase": 100,
    "number of Spaces": 0,
    "number of Digits": 0,
    "number of minus characters": 1,
    "number of dash characters": 0,
    "roman number": false,
    "min length": 1,
    "max length": 10,
    "exception":["NASA-IMPACT-MAAP", "mRNA"]
}
'''

def checkAcronym_v2(value, config="config.json"):
    #Load rules from config file
    file = open(config, 'r')
    data = json.load(file)
    uppercase = int(data["upperCase"])
    num_spaces = int(data["number of Spaces"])
    num_digits = int(data["number of Digits"])
    num_minus = int(data["number of minus characters"])
    num_dashs = int(data["number of dash characters"])
    isRoman = bool(data["roman number"])
    min_len = int(data["min length"])
    max_len = int(data["max length"])
    exceptions = data["exception"]
    exclusions = data["exclusion"]
    file.close()
    value = value.lstrip()
    v_len = len(value)

    if(value in exceptions): #an instance in exception list
        return True
    if(value in exclusions): #an instance in exclusion list
        return False
    if(value.count(' ') > num_spaces): #number of spaces
        return False
    if ((v_len < min_len) or (v_len > max_len)):# min_len and max_len
        return False
    if(not isRoman):#Roman number
        #if(bool(re.search(r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$",value))): # not a Roman number
        #    return False
        if(bool(re.search(r"^(X{1,3})(I[XV]|V?I{0,3})$|^(I[XV]|V?I{1,3})$|^V$", value))): #Only from 1-39
            return False
    if(value.count('-') > num_minus):#number of minus characters
        return False
    if(value.count('_') > num_dashs):#number of dashs characters
        return False
    
    digit_count = 0
    up_count = 0
    for character in value:
        if character.isdigit():#no digit
            digit_count += 1
            if(digit_count > num_digits):
                return False
        if character.isupper(): #uppercase
            up_count += 1

    percentage = float(up_count)/float(v_len) * 100.0
    if(float(percentage) < float(uppercase)):
        return False
    return True

def acronymFromLine(line): #Return all acronyms in a line
    result = []
    first_open = line.find('(')
    first_close = line.find(')', first_open)
    if (first_open == -1) or (first_close == -1):
        return result
    first_open = line[:first_close].rfind('(') #many opens before the first close
    selected = line[first_open + 1:first_close]
    if (checkAcronym(selected)):
        result.append(selected)
    line = line[first_close + 1:]
    res = acronymFromLine(line)
    if(res):
        for item in res:
            result.append(item)
    return result

def acronymFromFile(textFile):
    result = [] # array of dictionary{'Term':'', 'Description':'', 'Context':''}
    context = ""
    line_1 = ""
    file = open(textFile, 'r')
    for line in file:
        res = acronymFromLine(line)
        if(res):
            context = line_1 + line
            context = context.replace('\n', ' ')
            for item in res:
                des = descriptionFromContext(item, context) # Get the description from the context
                row = {'Term': item, 'Description': des, 'Context': context}
                result.append(row) #allow duplicated acronyms
        line_1 = line
    file.close()
    return result

def descriptionFromContext(term, context):
    description = ""
    pos = context.find('('+ term + ')') - 1
    if(pos < 0):
        print("ERROR: No term in the context! term: " + str(term) + "; context: " + str(context))
        return description
    context = context[:pos]
    # - Go from right to left 
    # - count the length of acronym (say 'n')
    # - Take at least 'n' words in the context that have the first letter capitalized. 
    # - And no more than n+2 words
    list_words = re.split('-| ', context)
    length = len(list_words)
    len_term = len(term)
    description = list_words[length - 1].strip() #at least take one word that is closest to the term
    count_term = 1
    count = 1
    for i in range(1, length - 1):
        word = list_words[length - 1 - i]
        if(count_term < len_term):
            description = word.strip() + " " + description.strip()
        else:
            break
        count += 1
        if (count > len_term + 1):
            break
        if(word == ""):
            continue
        if(word[0].isupper()):
            count_term += 1
    return description.strip()

def acronymFromLine_v2(line):
    output = []
    words = re.split(' |\(|\)', line)
    for word in words:
        if(checkAcronym(word)):
            output.append(word)
    return output

def findAcronymsFromText(text_file):
    output = []
    file = open(text_file, 'r')
    for line in file:
        print(line.strip())
        words = re.split(' |\(|\)|-|"|,|.', line.strip())
        for word in words:
            print(word)
            if(checkAcronym(word)):
                output.append(word)
    file.close()
    return output

def writeRowsToCSV(rows, csv_file):
    fieldheader = ['Term', 'Description', 'Context']
    with open(csv_file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldheader)
        writer.writeheader()
        writer.writerows(rows)
    return

def writeRowsToCSV_v2(rows, csv_file, fieldheader):
    with open(csv_file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldheader)
        writer.writeheader()
        writer.writerows(rows)
    return
