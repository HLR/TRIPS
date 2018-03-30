# trips
processing TRIPS

checkFiles.py - Takes the log file from the combine_scene and a path to the folder containing the input files and lists the corresponding files instead of doing copying. Useful for compareBad and copyfiles

checkXML.py - Checks number of scenes and sentences in an SpRL xml file.
checkXMLforWords.py - Checks number of sentences in original xml file against cleaned xml file.

combine_trips_xml_into_scene.py - Takes path to output folder and gold/train xml and merges the outputed files into the gold/train/other xml.

compareBadFiles.py - Compares text in original input file to text in outputed files to check if they match. Takes path to input/output containing folder and file listing bad files.

copyFiles.py - Takes list of bad files and path to directory containing input, output, and bad folders and copies them to the bad folder for quicker checking.

fixBrokenFiles.py - Fixes files with fractured sentences restructuring into one sentence, takes path to a folder containing the outputed xmls.

fixBrokenText.py - Fixes broken text in outputed files by replacing it 
with that in the original input file. Should use compareBadFiles.py first to make sure you want to do this.

pullSentenceTextFromXML.py - Pulls all sentence texts from a singular xml file

formatXMLs - Unix bash script to format all xmls in a current directory to make them more readable

xmlParse - Runs translate.xsl on all xml files in the input folder, 

translate.xsl and the input folder need to be in the directory where you run xmlParse 
