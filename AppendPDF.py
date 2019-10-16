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
from PyPDF2 import PdfFileMerger
import fnmatch

# Define path for input PDFs

inputPath = raw_input("Copy folder path to PDFs: ")
# print(inputPath)
os.chdir(inputPath)
pdfList = []
for file in glob.glob("*.pdf"):
    pdfList.append(file)
del file
# Loop through pdfList and store all cover, design, and pressure pdfs

coverList = fnmatch.filter(pdfList, "*cover*")
pressureList = fnmatch.filter(pdfList, "*pressur*")
designList = fnmatch.filter(pdfList, "*design*")

# Get the last modified date for each file in the list
recentCover = max(coverList, key=os.path.getctime)
recentPressure = max(pressureList, key=os.path.getctime)
recentDesign = max(designList, key=os.path.getctime)
recentList = []
recentList.append(recentCover)
recentList.append(recentDesign)
recentList.append(recentPressure)

# Create a Pdf merge object using the class from PyPDF2
def PDFmerge(pdfs, output):
    # Create the object
    pdfMerger = PdfFileMerger()
    # For every pdf in the input list, append the pdf to the end of virtual pdf
    for pdf in pdfs:
        with open(pdf, 'rb') as f:
            pdfMerger.append(f)
    # Write pdf to an output PDF
    with open(output, 'wb') as f:
        pdfMerger.write(f)

# Define main pdfs
def main ():
    pdfs = recentList
    output = 'Final.pdf'
    PDFmerge(pdfs = pdfs, output = output)
    
if __name__ == "__main__":
    main()

