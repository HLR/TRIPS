import os
import argparse
from shutil import copyfile
import shutil
import xml.etree.ElementTree as ET


def run(logFile,fileDir):
    inDir = os.path.join(fileDir,"input")
    outDir = os.path.join(fileDir,"output")
    badDir = os.path.join(fileDir,"bad")
    with open(logFile,'r') as file:
        for line in file.read().split('\n'):
            try:
                if (len(line)<1):
                    continue
                if (line[-3:]!='xml'):
                    continue
                sourceTree = ET.parse(os.path.join(inDir,line))
                genTree = ET.parse(os.path.join(outDir,line))
                sourceText=sourceTree.getroot().attrib['input']
                while sourceText[-1]==' ':
                    sourceText=sourceText[:-1]
                if len(genTree.getroot().findall('SCENE'))>0:
                    genTree.getroot().find('SCENE').find('SENTENCE').find('TEXT').text=sourceText
                else:
                    genTree.getroot().find('SENTENCE').find('TEXT').text=sourceText
                genTree.write(os.path.join(outDir,line))
            except Exception as e:
                print(e)
    return
def runWithoutLogFile(fileDir):
    inDir = os.path.join(fileDir,"input")
    outDir = os.path.join(fileDir,"output")
    badDir = os.path.join(fileDir,"bad")
    for fileName in os.listdir(outDir):
        try:
            if (len(fileName)<1):
                continue
            if (fileName[-3:]!='xml'):
                continue
            sourceTree = ET.parse(os.path.join(inDir,fileName))
            genTree = ET.parse(os.path.join(outDir,fileName))
            sourceText=sourceTree.getroot().attrib['input']
            if len(genTree.getroot().findall('SCENE'))>0:
                genTree.getroot().find('SCENE').find('SENTENCE').find('TEXT').text=sourceText
            else:
                genTree.getroot().find('SENTENCE').find('TEXT').text=sourceText
            genTree.write(os.path.join(outDir,fileName))
        except Exception as e:
            print(e)
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This is a script to find SpRL file data that did not find its way into a core file.')
    parser.add_argument(
        "--path",
        dest="path",
        required=True,
        help='Path to the input files')
    parser.add_argument(
        "--file",
        dest="file",
        required=False,
        help='Core SpRL log file')
    args=parser.parse_args()
    if args.file==None:
        runWithoutLogFile(args.path)
    else:
        run(args.file,args.path)
