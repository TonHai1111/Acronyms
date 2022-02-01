import csv
import re
from download import *
from tools import *
from variables import *

#Install:
# pip install beautifulsoup4
# pip install PyPDF2
# pip install wikipedia

#Note: https://caralsiseco.jimdofree.com/app/download/10208814770/S3.2.+ieee-thesaurus.pdf?t=1571240081
# is modified to https://caralsiseco.jimdofree.com/app/download/10208814770/S3.2.+ieee-thesaurus.pdf

def findAcronymsFromInputLinks(dict_in = dict_input):
    for key,value in dict_in.items():
        if (value == ''):
            continue
        if(isinstance(value, str)): #single link
            print('Get text from: ' + str(value))
            if(value[len(value) - 4:] == '.pdf'): #pdf file
                download_file(value)
                textFile = getTextfromPdf(processFileName(value))
            else:
                textFile = getTextfromHTML(value)
            list_acronyms = acronymFromFile(textFile)
            writeRowsToCSV(list_acronyms, "extractedAcronyms/" + processFileName(value) + ".csv")
            #write data
        else: # list of links
            for item in value:
                print('Get text from: ' + str(item))
                if(item[len(item)-4:] == '.pdf'): #pdf file
                    download_file(item)
                    textFile = getTextfromPdf(processFileName(item))
                else:
                    textFile = getTextfromHTML(item)
                list_acronyms = acronymFromFile(textFile)
                writeRowsToCSV(list_acronyms, "extractedAcronyms/" + processFileName(item) + ".csv")
    return

def checkAcronym_addDescription(dict_in = dict_input_extracted_json):
    return checkAcronym_addDescription_v3(dict_in)
    #return checkAcronym_addDescription_v1(dict_in)

def checkAcronym_addDescription_v1(dict_in = dict_input_extracted):
    for key,value in dict_in.items():
        if(value == ''):
            continue
        rows = []
        acronyms = []
        print ('Loading extracted acronyms...')
        if(isinstance(value, str)): #single file
            with open("extractedAcronyms/" + value, 'r') as f:
                csvreader = csv.reader(f)
                header = next(csvreader)
                for r in csvreader:
                    ro = {'Term': r[0], 'Description': r[1], 'Context': r[2]}
                    acronyms.append(ro)
        else: # many files
            for item in value:
                with open("extractedAcronyms/" + item, 'r') as f:
                    csvreader = csv.reader(f)
                    header = next(csvreader)
                    for r in csvreader:
                        ro = {'Term': r[0], 'Description': r[1], 'Context': r[2]}
                        acronyms.append(ro)

        print('Reading input from file: ' + str(key))
        file = open("InputFiles/terms/" + key, 'r')
        for line in file:
            #words = line.split(' ')
            words = re.split(' |\(|\)', line)
            isAcr = False
            isDec = False
            term = ""
            decs = ""
            cont = ""
            for word in words:
                if (word == ''):
                    continue
                if(checkAcronym(word)):
                    isAcr = True
                    term = word
                    break
            if(isAcr): #Find description
                for ac in acronyms:
                    if(ac['Term'] == term):
                        isDec = True
                        decs = ac['Description']
                        cont = ac['Context']
                        break
            row = {'Input Text': line, 'isAcronym': str(isAcr), 
                'Extracted Term': term, 'isDescription': str(isDec), 
                'Description': decs, 'Context': cont}
            rows.append(row)
        file.close()
        fieldheader = ['Input Text', 'isAcronym', 
                    'Extracted Term', 'isDescription', 
                    'Description', 'Context']
        print("Writing output to file: " + "outputFiles/" + key)
        writeRowsToCSV_v2(rows, "outputFiles/" + key, fieldheader)
    return

#Read from the csv files
def checkAcronym_addDescription_v2(dict_in = dict_input_extracted):
    #Load AcronymDefinition from file...
    GivenDescriptions = loadAcronymDefinition()

    for key,value in dict_in.items():
        if(value == ''):
            continue
        rows = []
        acronyms = []
        print ('Loading extracted acronyms...')
        if(isinstance(value, str)): #single file
            with open("extractedAcronyms/" + value, 'r') as f:
                csvreader = csv.reader(f)
                header = next(csvreader)
                for r in csvreader:
                    ro = {'Term': r[0], 'Description': r[1], 'Context': r[2]}
                    acronyms.append(ro)
        else: # many files
            for item in value:
                with open("extractedAcronyms/" + item, 'r') as f:
                    csvreader = csv.reader(f)
                    header = next(csvreader)
                    for r in csvreader:
                        ro = {'Term': r[0], 'Description': r[1], 'Context': r[2]}
                        acronyms.append(ro)

        print('Reading input from file: ' + str(key))
        file = open("InputFiles/terms/" + key, 'r')
        with open("InputFiles/terms/" + key, 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for line in csvreader:
                #words = line.split(' ')
                term_line = line[0]
                words = re.split(' |\(|\)', term_line)
                isAcr = False
                isDec = False
                term = ""
                decs = ""
                cont = ""
                for word in words:
                    if (word == ''):
                        continue
                    if(checkAcronym(word)):
                        isAcr = True
                        term = word
                        break
                if(isAcr): #Find description
                    for ac in acronyms:
                        if(ac['Term'] == term):
                            isDec = True
                            decs = ac['Description']
                            cont = ac['Context']
                            break
                #Build row
                row = buildRow(GivenDescriptions, header, line, term, isAcr, isDec, decs, cont)
                rows.append(row)
            fieldheader = []
            for h in header:
                fieldheader.append('Input ' + h)
            fieldheader.extend(["isAcronym", "Extracted Term", "isDescription", "Description", "Context"])
            print("Writing output to file: " + "outputFiles/" + key)
            writeRowsToCSV_v2(rows, "outputFiles/" + key, fieldheader)
    return

#Read from json files
def checkAcronym_addDescription_v3(dict_in = dict_input_extracted_json):
    #Load AcronymDefinition from file...
    GivenDescriptions = loadAcronymDefinition()
    all_acronyms = {}
    for key,value in dict_in.items():
        if(value == ''):
            continue
        print ('Loading extracted acronyms...')
        if(isinstance(value, str)): #single file
            with open("extractedAcronyms/" + value, 'r') as f:
                csvreader = csv.reader(f)
                header = next(csvreader)
                for r in csvreader:
                    ro = { 'Description': r[1], 'Context': r[2]}
                    all_acronyms[r[0]] = ro
                    #all_acronyms.append(ro)
        else: # many files
            for item in value:
                with open("extractedAcronyms/" + item, 'r') as f:
                    csvreader = csv.reader(f)
                    header = next(csvreader)
                    for r in csvreader:
                        ro = { 'Description': r[1], 'Context': r[2]}
                        all_acronyms[r[0]] = ro

    for key,value in dict_in.items():
        if(value == ''):
            continue
        rows = []
        acronyms = {}
        print ('Loading extracted acronyms...')
        if(isinstance(value, str)): #single file
            with open("extractedAcronyms/" + value, 'r') as f:
                csvreader = csv.reader(f)
                header = next(csvreader)
                for r in csvreader:
                    ro = {'Description': r[1], 'Context': r[2]}
                    acronyms[r[0]]=ro
        else: # many files
            for item in value:
                with open("extractedAcronyms/" + item, 'r') as f:
                    csvreader = csv.reader(f)
                    header = next(csvreader)
                    for r in csvreader:
                        ro = {'Description': r[1], 'Context': r[2]}
                        acronyms[r[0]]=ro

        print('Reading input from file: ' + str(key))
        file = open("InputFiles_v2/" + key, 'r')
        json_data = json.load(file)
        for item in json_data["Terms"]:
            words = re.split(' |\(|\)', str(item["Term"]))
            isAcr = False
            isDec = False
            term = ""
            decs = ""
            cont = ""
            for word in words:
                if (word == ''):
                    continue
                if(checkAcronym(word)):
                    isAcr = True
                    term = word
                    break
            if(isAcr): #Find description
                if(term in acronyms):
                    isDec = True
                    decs = acronyms[term]['Description']
                    cont = acronyms[term]['Context']
                else:
                    if(term in all_acronyms):
                        isDec = True
                        decs = all_acronyms[term]['Description']
                        cont = all_acronyms[term]['Context'] 
                   
                #Build row
                row = buildRow(GivenDescriptions, ["Term"], [item["Term"]], term, isAcr, isDec, decs, cont)
                rows.append(row)
        file.close()
        fieldheader = ["Input Term", "isAcronym", "Extracted Term", "isDescription", "Description", "Context"]
        print("Writing output to file: " + "outputFiles/" + key[:key.find('.json')] + ".csv")
        writeRowsToCSV_v2(rows, "outputFiles/" + key[:key.find('.json')] + ".csv", fieldheader)

    return

def buildRow(GivenDescriptions, header, line, term, isAcr, isDec, decs, cont):
    row = {}
    t_c = 0
    for h in header:
        row['Input ' + h] = line[t_c]
        t_c += 1
    row['isAcronym'] = str(isAcr)
    row['Extracted Term'] = term
    if(isDec or (not isAcr)):
        row['isDescription'] = str(isDec)
        row['Description'] = decs
        row['Context'] = cont
    else:
        if(term in GivenDescriptions):
            row['isDescription'] = str(isDec)
            row['Description'] = GivenDescriptions[term]
            row['Context'] = "From Acronym definition config file."
        else:
            row['isDescription'] = str(isDec)
            wiki_data = getAcronymDefinitionWiki(term)
            #wiki_data = "" #For testing
            if(wiki_data):
                row['Description'] = wiki_data[0]
                row['Context'] = "From Wikipedia/Google: " + str(wiki_data)
            else:
                row['Description'] = ""
                row['Context'] = ""
    return row

if __name__ == "__main__":
    #findAcronymsFromInputLinks(dict_input_json)
    checkAcronym_addDescription(dict_input_extracted_json)
    
    #extractAcronymsFromText("Input.csv")

    #writeTextToCSV("Text.txt")
    #checkAcronymFromFile("Input.csv")
    
