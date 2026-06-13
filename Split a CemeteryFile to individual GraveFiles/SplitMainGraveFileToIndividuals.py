# PRODUCTION PATHS stored here
'''
# for Waldzell
FileInPath = Path.home() / r"Genealogy\GeneDB\RM_LinkedFiles\Sources\Grave\DE, Bayern, Main-Spessart\Waldzell"
FileInName = r"Friedhof Waldzell - Grave List.txt"
FileOutFldrName = "Generated files"

# for Oberschwarzach
FileInPath = Path.home() / r"Genealogy\GeneDB\RM_LinkedFiles\Sources\Grave\DE, Bayern, Schweinfurt\Oberschwarzach"
FileInName = r"Friedhof Oberschwarzach - Grave List.txt"
FileOutFldrName = "Generated Files"

TODO  create a shared function to accept a path to a folder. confirm it is a folder,
if folder exists- rename it with a timestamp
if not try to create folder
'''

import os
from pathlib import Path

FileInFldrPath = Path.home() / r"folder" 
FileInName = r"test input.txt"
FileOutFldrName = "Generated files"

EntrySeperator = "="*70 + "===DIV80==\n"
tempFileName = "trashFile"
FileOutExt = ".txt"
FileOutPath= Path(FileInFldrPath) / FileOutFldrName

fileIn = open(FileInFldrPath / FileInName, 'r', encoding='utf-8')
prevFileOut = open(FileOutPath / (tempFileName + FileOutExt), 'w', encoding='utf-8')
FileOut = prevFileOut

Line = fileIn.readline() 
while (Line != ""):
    # print (Line)
    if (Line == EntrySeperator):
        FileOut.write( EntrySeperator )
        Line = fileIn.readline() 
        # print (Line)
        # extract the plot ID for use in filename
        PID = Line[8:Line.find(' ', 8)]
        print (PID)
        FileOutName="plot " + PID
        if (Line == EntrySeperator):
            FileOutName = tempFileName
        prevFileOut.close()
        FileOut = open (FileOutPath / (FileOutName + FileOutExt), 'w', encoding='utf-8')
        prevOutFile = FileOut
        FileOut.write(EntrySeperator)
    FileOut.write(Line)
    Line = fileIn.readline() 

fileIn.close()
FileOut.close() 
prevFileOut.close()
os.remove (FileOutPath / (tempFileName + FileOutExt))

input("Press Enter to continue.")
