import os
import argparse
from shutil import copyfile
import shutil


def run(logFile,fileDir):
    texts = []
    for fileName in os.listdir(fileDir):
        if not fileName[-3:]=='xml':
            continue
        with open(os.path.join(fileDir,fileName),'r',encoding='utf-8') as file:
            fileContent=file.read()
            texts+=[(fileName,fileContent)]
    with open(logFile,"r",encoding='utf-8') as logFile:
        logContent = logFile.read()
        files=[]
        for line in logContent.split('\n'):
            if (line=="No match found for:"
                or line=="--------------------------------------"
                or len(line) < 1):
                continue
            for text in list(texts):
                if (text[1].find(line) != -1):
                    print(text[0])
                    texts.remove(text)
                    break

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
        required=True,
        help='Core SpRL log file')
    args=parser.parse_args()
    run(args.file,args.path)
