#Michael Furst
#February 4, 2018
#Read SPRL XML file and parse matching data from other files into new file

import os
import xml.etree.ElementTree as ET
import re
import argparse
class File:
    def __init__(self):
        self.text=""
        self.fileName=""
        return
    def __str__(self):
        s = ""
        s+=self.fileName+"\n"
        s+=self.text+"\n"
        return s

def cleanString(string):
    string = re.sub('[^a-zA-Z]',"",string)
    charPairs = [('A','a'),('B','b'),('C','c'),('D','d'),('E','e'),('F','f'),
                 ('G','g'),('H','h'),('I','i'),('J','j'),('K','k'),('L','l'),
                 ('M','m'),('N','n'),('O','o'),('P','p'),('Q','q'),('R','r'),
                 ('S','s'),('T','t'),('U','u'),('V','v'),('W','w'),('X','x'),
                 ('Y','y'),('Z','z')]
    for pair in charPairs:
        string=string.replace(pair[0],pair[1])
    return string

def findMatch(text,files):
    for file in files:
        t1 = cleanString(file.text)
        t2 = cleanString(text)
        if (t1==t2):
            return file.fileName
    return ""

def indexFiles(dirPath):
    files=[]
    #for i in range(0,774):
    dirName = dirPath#"/Users/michaelfurst/Desktop/TRIPSCleaned/"
    for name in os.listdir(dirName):
        name = os.path.join(dirName,name)
        try:
            _tree = ET.parse(name)
        except (FileNotFoundError,ET.ParseError) as e:
            print(e)
            continue
        if (_tree.getroot().tag=='SpRL'):
            for scene in _tree.getroot():
                for element in scene:
                    if element.tag=='SENTENCE':
                        text = element.find('TEXT').text
                        file = File()
                        file.fileName=name
                        file.text=text
                        files+=[file]
        elif (_tree.getroot().tag=='SENTENCE'):
            text = _tree.getroot().find('TEXT').text
            file = File()
            file.fileName=name
            file.text=text
            files+=[file]
    return files

def _pullElements(root):
    elements=[]
    #Have to navigate to/find Sentence
    for scene in root:
        for element in scene:
            if element.tag=='SENTENCE':
                for elem in element:
                    if elem.tag!='TEXT':
                        elements+=[elem]
    return elements
def pullElements(fileName):
    tree=ET.parse(fileName)
    root=tree.getroot()
    if root.tag=='SpRL':
        #If is using older format call specialized function
        return _pullElements(root)
    elements=[]
    for elem in root:
        #Pull all non-'TEXT' elements
        if elem.tag!='TEXT':
            elements+=[elem]
    return elements
        
def run(xmlName,pathToCleanedXMLS):
    files = indexFiles(pathToCleanedXMLS)
    try:
        tree = ET.parse(xmlName)
    except (FileNotFoundError,ET.ParseError):
        print("Could not load \'"+xmlName)
        return
    log=""
    root = tree.getroot()
    for scene in list(root):
        for element in list(scene):
            if element.tag=='SENTENCE':
                text = element.find('TEXT').text
                #find matching text file
                match=findMatch(text,files)
                #if there is no match remove scentence and add to log
                if match=="":
                    log+="No match found for:\n"
                    log+=text+"\n"
                    log+="--------------------------------------\n"
                    root.remove(scene)
                    break
                else:
                    #Remove non-'TEXT' elements
                    for sub in list(element):
                        if sub.tag!='TEXT':
                            element.remove(sub)
                    #Update with new non-'TEXT' elements
                    for elem in list(pullElements(match)):
                        element.append(elem)
    #write tree to output file
    tree.write(xmlName[:-4]+"-output.xml")
    print(xmlName[:-4]+"-output.xml successfully created")
    #write log
    if log!="":
        logFile = open(xmlName[:-4]+"-log.txt",'a')
        logFile.write(log)
        logFile.close()
        print("An error log (\'"+xmlName[:-4]+"-log.txt\') has been generated.")
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This is a script to join SpRL file data into a core file.')
    parser.add_argument(
        "--path",
        dest="path",
        required=True,
        help='Path to the cleaned files')
    parser.add_argument(
        "--file",
        dest="file",
        required=True,
        help='Core SpRL file')
    args=parser.parse_args()
    run(args.file,args.path)

