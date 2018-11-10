import os
import argparse
from shutil import copyfile
import shutil


def run(logFile,fileDir):
    inDir = os.path.join(fileDir,"input")
    outDir = os.path.join(fileDir,"output")
    badDir = os.path.join(fileDir,"bad")
    with open(logFile,'r') as file:
        for line in file.read().split('\n'):
            try:
                copyfile(os.path.join(inDir,line),os.path.join(badDir,line))
                copyfile(os.path.join(inDir,line+".clean"),os.path.join(badDir,line+".clean"))
                copyfile(os.path.join(outDir,line),os.path.join(badDir,line[:-4]+"_merged.xml"))
            except IsADirectoryError:
                continue
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
        required=True,
        help='Core SpRL log file')
    args=parser.parse_args()
    run(args.file,args.path)
