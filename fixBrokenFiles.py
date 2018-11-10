import os
import argparse
import xml.etree.ElementTree as ET
from copy import deepcopy


def run(fileDir):
    for file in os.listdir(fileDir):
        if not file[-3:]=='xml':
            continue
        tree = ET.parse(os.path.join(fileDir,file))
        root = tree.getroot()
        if (len(root.findall('SENTENCE'))<=1):
            continue
        theSentence=deepcopy(root.findall('SENTENCE')[0])
        textElem = theSentence.find('TEXT')
        for element in list(theSentence):
            #if element.tag!='TEXT':
            theSentence.remove(element)
        theSentence.append(textElem)
        end = -1
        text = ""
        elements=[]
        for sentence in list(root.findall('SENTENCE')):
            for element in list(sentence):
                if element.tag=='TEXT':
                    if (len(text)>0):
                        if text[-1]==element.text[0]:
                            text+=element.text[1:]
                        else:
                            text+=element.text
                    else:
                        text=element.text
                    end = sentence.get('end')
                else:
                    elements+=[element]
            root.remove(sentence)
        theSentence.set('end',end)
        theSentence.find('TEXT').text=text
        elements[:]=sorted(elements,key=lambda child: (child.tag,child.get('id')))
        for elem in elements:
            theSentence.append(elem)
        root.clear()
        root.append(theSentence)
        tree.write(os.path.join(os.path.join(fileDir,"out"),file))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This is a script to find SpRL file data that did not find its way into a core file.')
    parser.add_argument(
        "--path",
        dest="path",
        required=True,
        help='Path to the input files')
    args=parser.parse_args()
    run(args.path)
