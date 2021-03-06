#!/usr/bin/env python
#-*-coding: utf-8 -*-

import argparse
import os
import re
import xml.etree.ElementTree as ET
import time
import pandas as pd

d = {}

def get_clean_parse(fileName):
    try:
        new_rdf_pattern = ""
        relevant_rdf_pattern = a.split("<rdf:Description")[1:]
        for item in relevant_rdf_pattern:
            individual_rdf = item.split("</rdf:Description>")[0]
            new_rdf_pattern += "  <rdf:Description" \
                               + individual_rdf + "</rdf:Description>\n"
        root_pattern = a.split("<rdf:RDF")[1].split("<rdf:Description")[0]
        rdf_pattern = "<rdf:RDF  " + root_pattern \
                      + new_rdf_pattern + "</rdf:RDF>"
    except IndexError:
        out = "---------------------------------------\n"
        out += fileName.split("/")[-1] + "\n"
        out += "Error type: \n"
        out += "\tIndexError\n"
        error.write(out)
        return

    pattern = re.compile(r' input=".+\n')
    if pattern.search(a):
        TEXT = '\n     <TEXT> "' \
               + a.split("input=\"")[1].split('\n"')[0] + '"</TEXT>'

    #fromstring takes the string and makes a root node
    root = ET.fromstring(rdf_pattern)

    relation_id = 0

    # GET NUMBER OF CHUNKS/WORDS EXPRESSED BY <rdf> TAG IN TRIPS XML
    i = 0
    for child in root:
        i += 1

    greatestEnd = 0
    for rootchunkitem in range(len(root[0])):
        if root[0][rootchunkitem].tag.split("}")[1] == 'start':
            startval = 'start="' + root[0][rootchunkitem].text + '"'
        elif root[0][rootchunkitem].tag.split("}")[1] == 'end':
            greatestEnd = int(root[0][rootchunkitem].text)
            endval = 'end="' + root[0][rootchunkitem].text + '"'

    myparse = '\n<SENTENCE id="' \
              + list(root[0].attrib.values())[0] \
              + '" ' \
              + startval \
              + " " \
              + endval \
              + ">" \
              + TEXT

    chunk_id = {}

    for n in range(0,i):
        k = len(root[n])  # NUMBER OF INFO LINES IN EACH <rdf> CHUNK
        chunk_id[n] = list(root[n].attrib.values())[0]

        dic_tag = {}
        dic_text = {}

        #adds PHRASE,RElATION, etc. tags
        #start p at 2
        for p in range(2,k):
            dic_tag[str(p)] = str(root[n][p].tag.split("}")[1])

            if root[n][p].tag.split("}")[1] == 'start' or root[n][p].tag.split("}")[
                1] == 'end' or root[n][p].tag.split("}")[1] == 'word':
                dic_text[str(p)] = str(p)
            else:
                if root[n][p].text is None:
                    mylist = (list(root[n][p].attrib.values()))
                    dic_text[str(p)] = str(str(mylist).strip("'[").strip("]'"))
                else:
                    dic_text[str(p)] = str(root[n][p].text)

        lf_list = []
        role_list = []

        for key, value in list(dic_text.items()):
            if "#" not in value:
                lf_list.append(key)
            else:
                role_list.append(key)

        myparse += '\n     <PHRASE id="' + chunk_id[n] + '" type="' \
                   + root[n][1].text + '" ' + root[n][0].tag.split("}")[1] \
                   + '="' + root[n][0].text + '"'

        for lf in lf_list:
            if root[n][int(lf)].tag.split("}")[1] == 'start':
                startval = 'start="' + root[n][int(lf)].text + '"'
            elif root[n][int(lf)].tag.split("}")[1] == 'end':
                endtemp = int(root[n][int(lf)].text)
                if endtemp > greatestEnd:
                    greatestEnd = endtemp
                endval = 'end="' + root[n][int(lf)].text + '"'
            elif root[n][int(lf)].tag.split("}")[1] == 'word':
                textval = 'text="' + root[n][int(lf)].text + '"'
                #print "textval: ", textval
            if (root[n][int(lf)].tag.split("}")[1] != 'start') and (
                    root[n][int(lf)].tag.split("}")[1] != 'end') and(
                    root[n][int(lf)].tag.split("}")[1] != 'word'):
                myparse += " " + \
                           root[n][int(lf)].tag.split("}")[1] + '="' \
                           + root[n][int(lf)].text + '"'

        try:
            textval
            myparse += " " + textval + " " + startval + " " + endval + "/>"
        except NameError:
            myparse += " " + startval + " " + endval + "/>"

        for role in role_list:
            relation_id += 1
            myparse += '\n     <RELATION id="' + str(relation_id) \
                       + '" head="' + chunk_id[n] + '" res="' \
                       + dic_text[role].split("#")[1] + '" label="' \
                       + dic_tag[role] + '"/>'

    myparse += "\n</SENTENCE>\n\n"

    newTree = ET.ElementTree(ET.fromstring(myparse))
    newRoot = newTree.getroot()
    newRoot.attrib['end']=str(greatestEnd)
    newTree.write(fileName+'.clean')
    #with open(fileName + '.clean', 'w') as new:
        #new.write(myparse)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This is a script to create cleaner/simpler XMLs from the TRIPS XML output.')
    parser.add_argument(
        "--path",
        dest="path",
        required=True,
        help='path to the input directory containing all TRIPS XML parses')
    args = parser.parse_args()

    with open(time.strftime("%Y%m%d-%H%M") + '.err', 'a') as error:
     error.write("The following files did not have a parse.\n\n")
     for dirName in os.listdir(args.path):
        if dirName.startswith("batch"):
            dirName = os.path.join(args.path, dirName)
            for fileName in os.listdir(dirName):
                if fileName.endswith(".xml"):
                    with open(os.path.join(args.path, dirName, fileName), 'r') as f:
                        a = f.read()
                        get_clean_parse(os.path.join(dirName, fileName))
    print("********************\nCleaned parses are in the same directory as the original parse files.\n\nfileName %s in the current directory contains the list of files that did not have parses to be cleaned.\n********************\n" % str(error).split("'")[1])
