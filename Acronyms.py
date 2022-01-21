#from urllib.request import urlopen
#from bs4 import BeautifulSoup
#import urllib.request
#import PyPDF2
#from pathlib import Path
import csv
import re
from download import *
from tools import *

#Install:
# pip install beautifulsoup4
# pip install PyPDF2

#Note: https://caralsiseco.jimdofree.com/app/download/10208814770/S3.2.+ieee-thesaurus.pdf?t=1571240081
# is modified to https://caralsiseco.jimdofree.com/app/download/10208814770/S3.2.+ieee-thesaurus.pdf


filenames = ["AGUIndexTerms.csv",
    "Astrophysics and Cosmic Engine Glossary.csv",
    "Beyond Earth_ A Chronicle of Deep Space Exploration, 1958 - 2016_ e-book.csv",
    "Biology Glossary.csv",
    "ESA Space Weather Glossary.csv",
    "Gazetteer of Planetary Nomenclature Feature Terms.csv",
    "Gazetteer of Planetary Nomenclature Planetary Names.csv",
    "Global Change Master Directory (GCMD).csv",
    "IEEE Thesaurus and Taxonomy.csv",
    "ISO 21348.csv",
    "lunarinstrumentlist.csv",
    "NASA CCMC.csv",
    "NASA Heliophysics Vocabulary.csv",
    "NASA Thesaurus.csv",
    "Planetary Science Research Discoveries Glossary.csv",
    "SMD Glossary.csv",
    "Space Weather Glossary.csv",
    "SPASE Dictionary.csv"]

dict_input = {"AGUIndexTerms.csv":"",
    "Astrophysics and Cosmic Engine Glossary.csv":"https://www.atnf.csiro.au/outreach/education/senior/astrophysics/astrophysics_glossary.html#A-spectral-class",
    "Beyond Earth_ A Chronicle of Deep Space Exploration, 1958 - 2016_ e-book.csv":"https://www.nasa.gov/sites/default/files/atoms/files/beyond-earth-tagged.pdf",
    "Biology Glossary.csv":"https://www.boyertownasd.org/site/handlers/filedownload.ashx?moduleinstanceid=4502&dataid=8141&FileName=NEW%20GLOSSARY%20COMBINED.pdf",
    "ESA Space Weather Glossary.csv":"https://swe.ssa.esa.int/glossary",
    "Gazetteer of Planetary Nomenclature Feature Terms.csv":"https://planetarynames.wr.usgs.gov/DescriptorTerms",
    "Gazetteer of Planetary Nomenclature Planetary Names.csv":"https://planetarynames.wr.usgs.gov/Page/Planets",
    "Global Change Master Directory (GCMD).csv":["https://gcmd.earthdata.nasa.gov/static/kms/",
                    "https://earthdata.nasa.gov/earth-observation-data/find-data/idn/gcmd-keywords"],
    "IEEE Thesaurus and Taxonomy.csv":"https://caralsiseco.jimdofree.com/app/download/10208814770/S3.2.+ieee-thesaurus.pdf",
    "ISO 21348.csv":"https://spacewx.net/wp-content/uploads/2020/08/ISO_PRF_21348_e_review.pdf",
    "lunarinstrumentlist.csv":"",
    "NASA CCMC.csv":"https://ccmc.gsfc.nasa.gov/RoR_WWW/presentations/Glossary_of_Space_Weather_terms.pdf",
    "NASA Heliophysics Vocabulary.csv":"https://www.nasa.gov/mission_pages/sunearth/spaceweather/vocabulary.html",
    "NASA Thesaurus.csv":"https://www.sti.nasa.gov/nasa-thesaurus/",
    "Planetary Science Research Discoveries Glossary.csv":"http://www.psrd.hawaii.edu/PSRDglossary.html",
    "SMD Glossary.csv":"https://science.nasa.gov/glossary",
    "Space Weather Glossary.csv":["https://www.swpc.noaa.gov/content/space-weather-glossary",
                    "https://spacewx.com/glossary/"],
    "SPASE Dictionary.csv":"https://spase-group.org/data/model/search/index.html?version=2.4.0"}

dict_input_extracted = {"AGUIndexTerms.csv":"",
    "Astrophysics and Cosmic Engine Glossary.csv":"astrophysics_glossary.html#A-spectral-class.csv",
    "Beyond Earth_ A Chronicle of Deep Space Exploration, 1958 - 2016_ e-book.csv":"beyond-earth-tagged.pdf.csv",
    "Biology Glossary.csv":"filedownload.ashx?moduleinstanceid=4502&dataid=8141&FileName=NEW%20GLOSSARY%20COMBINED.pdf.csv",
    "ESA Space Weather Glossary.csv":"swe.ssa.esa.int_glossary.csv",
    "Gazetteer of Planetary Nomenclature Feature Terms.csv":"DescriptorTerms.csv",
    "Gazetteer of Planetary Nomenclature Planetary Names.csv":"Planets.csv",
    "Global Change Master Directory (GCMD).csv":["kms.csv",
                    "gcmd-keywords.csv"],
    "IEEE Thesaurus and Taxonomy.csv":"S3.2.+ieee-thesaurus.pdf.csv",
    "ISO 21348.csv":"ISO_PRF_21348_e_review.pdf.csv",
    "lunarinstrumentlist.csv":"",
    "NASA CCMC.csv":"Glossary_of_Space_Weather_terms.pdf.csv",
    "NASA Heliophysics Vocabulary.csv":"vocabulary.html.csv",
    "NASA Thesaurus.csv":"nasa-thesaurus.csv",
    "Planetary Science Research Discoveries Glossary.csv":"PSRDglossary.html.csv",
    "SMD Glossary.csv":"science.nasa.gov_glossary.csv",
    "Space Weather Glossary.csv":["space-weather-glossary.csv",
                    "spacewx.com_glossary.csv"],
    "SPASE Dictionary.csv":"index.html?version=2.4.0.csv"}

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
def checkAcronym_addDescription(dict_in = dict_input_extracted):
    return checkAcronym_addDescription_v2(dict_in)
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

def checkAcronym_addDescription_v2(dict_in = dict_input_extracted):
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
                t_c = 0
                row = {}
                for h in header:
                    row['Input ' + h] = line[t_c]
                    t_c += 1
                row['isAcronym'] = str(isAcr)
                row['Extracted Term'] = term
                row['isDescription'] = str(isDec)
                row['Description'] = decs
                row['Context'] = cont
                #row = {'Input Text': line, 'isAcronym': str(isAcr), 
                #    'Extracted Term': term, 'isDescription': str(isDes), 
                #    'Description': decs, 'Context': cont}
                rows.append(row)
            fieldheader = []
            for h in header:
                fieldheader.append('Input ' + h)
            fieldheader.append("isAcronym")
            fieldheader.append("Extracted Term")
            fieldheader.append("isDescription")
            fieldheader.append("Description")
            fieldheader.append("Context")
            #fieldheader = ['Input Text', 'isAcronym', 
            #            'Extracted Term', 'isDescription', 
            #            'Description', 'Context']
            print("Writing output to file: " + "outputFiles/" + key)
            writeRowsToCSV_v2(rows, "outputFiles/" + key, fieldheader)
    return

def writeTextToCSV(file_name):
    rows = []
    file = open(file_name, 'r')
    for line in file:
        words = re.split(' |\(|\)|"|/', line.strip())
        for word in words:
            row = {}
            if(word == ''):
                continue
            row['Input Term'] = str(word)
            rows.append(row)
    file.close()
    fieldheader = ['Input Term']
    writeRowsToCSV_v2(rows, "Input.csv", fieldheader)
    return

def checkAcronymFromFile(file_name):
    rows = []
    with open(file_name, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for line in csvreader:
            #words = line.split(' ')
            term_line = line[0]
            words = re.split(' |\(|\)', term_line)
            isAcr = False
            term = ""
            for word in words:
                if (word == ''):
                    continue
                if(checkAcronym(word)):
                    isAcr = True
                    term = word
                    break
            #Build row
            t_c = 0
            row = {}
            row['Input Term'] = line[0]
            row['isAcronym'] = str(isAcr)
            row['Extracted Term'] = term
            rows.append(row)
    fieldheader = ["Input Term", "isAcronym", "Extracted Term"]
    writeRowsToCSV_v2(rows, "temp1.csv", fieldheader)
    return

def extractAcronymsFromText(file_name):
    output = findAcronymsFromText(file_name)
    fieldheader = ["Acronym"]
    rows = []
    row = {}
    for acr in output:
        row["Acronym"] = acr
        rows.append(row)
    writeRowsToCSV_v2(rows, "temp.csv", fieldheader)
    return

if __name__ == "__main__":
    findAcronymsFromInputLinks(dict_input)
    checkAcronym_addDescription(dict_input_extracted)
    
    #extractAcronymsFromText("Input.csv")

    #writeTextToCSV("Text.txt")
    #checkAcronymFromFile("Input.csv")
    
