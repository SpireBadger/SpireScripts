# Project: Merge Design PDF
# Create Date: 08/20/2019
# Last Updated: 08/20/2019
# Create by: Robert Domiano
# Purpose: Merge the cover, design, and pressure  PDF's without using
#          PDFPro.
# Python Version:   2.7.5
# Input Variables: 
# Output: 

import glob
import os
from PyPDF2 import PdfFileMerger, PdfFileReader
import fnmatch

# Define path for input PDFs

inputPath = raw_input("Copy folder path to PDFs: ")
print(inputPath)
os.chdir(inputPath)
pdfList = []
for file in glob.glob("*.pdf"):
    pdfList.append(file)
del file
# Loop through pdfList and store all cover, design, and pressure pdfs

coverList = fnmatch.filter(pdfList, "*cover*")
pressureList = fnmatch.filter(pdfList, "*pressure*")
designList = fnmatch.filter(pdfList, "*design*")

# Get the last modified date for each file in the list
recentCover = max(coverList, key=os.path.getctime)
recentPressure = max(pressureList, key=os.path.getctime)
recentDesign = max(designList, key=os.path.getctime)
recentList = []
recentList.append(recentCover)
recentList.append(recentPressure)
recentList.append(recentDesign)

merger = PdfFileMerger()
