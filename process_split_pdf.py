import os
import time
import logging
import json

### Global Variable Initializaton ###
LOG_PATH = "Z:/Software/AndrewsUtilities/logs/pdf_processing.log"

TAGS_FILE = open("Z:/Software/AndrewsUtilities/tags.json")
tags = json.load(TAGS_FILE)
TAGS_FILE.close()

def split_name(text):
    dashes = [i for i, letter in enumerate(text) if letter == '-']
    if len(dashes) == 1: #If there's only one '-', it must be where we should split
        return text[:dashes[0]] + '.pdf'
    else:
        found_tag = False
        split_dash = None
        for index in dashes:
            for tag in tags:
                if text[index+1:].startswith(tag['tag']):
                    found_tag = True
                    split_dash = index
                    break
        
        if found_tag:
            return text[:split_dash] + '.pdf'
        else:
            print("Found multiple dashes when attempting to fix a file name. Which one of these looks right to you?")
            counter = 1
            for index in dashes:
                print(str(counter) + ": \"" + text[:index] + ".pdf\"")
                counter = counter + 1
                
            choice = input("File name selection: ")
            return text[:dashes[int(choice)-1]] + '.pdf'
            

working_dir = './'

print("This tool can help you process files created by splitting a PDF!")
print("Which tool did you use to split the PDF?")
print("1 - Kofax PowerPDF Advanced")
print("2 - Standalone PDF Splitting Tool")
tool_used = input("Tool used: ")
used_standalone = int(tool_used) == 2

file_prefix = None
if not used_standalone:
    file_prefix = input("Prefix to remove ('NONE' if no prefix): ")
    if file_prefix == "NONE":
        file_prefix = None
else:
    print("Please provide the name of the folder containing the PDF files. This folder must be inside the folder running this script.")
    print("If the PDF files are in the same folder as this script, enter 'NONE'")
    pdf_dir = input("Name of folder containing PDF files: ")
    if pdf_dir != "NONE":
        if not pdf_dir.endswith('/'):
            pdf_dir = pdf_dir + '/'
        working_dir = os.path.join(working_dir, pdf_dir)

output_dirname = input("Name for output folder: ")
if not output_dirname.endswith('/'):
    output_dirname = output_dirname + '/'

output_dir = os.path.join('./', output_dirname)
### End Global Variables ###

START = time.time()
print("Processing Files...")

logging.basicConfig(filename=LOG_PATH, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

#Create directories as needed
for tag in tags:
    if not os.path.exists(output_dir + tag['folder']):
        print("Creating directory: " + output_dir + tag['folder'])
        os.makedirs(output_dir + tag['folder'])

num_files = 0

#Iterate over all files in directory
for filename in os.listdir(working_dir):
    if os.path.isfile(os.path.join(working_dir + filename)):
        is_pdf = '.pdf' in filename.lower()
        if used_standalone: #Used standalone splitter
            new_name = split_name(filename)
        else: #Used Kofax PowerPDF
            if file_prefix != None and filename.startswith(file_prefix):
                new_name = filename.replace(file_prefix, '')
        
        if is_pdf: #Only move PDF files
            num_files = num_files + 1
            new_path = output_dir
            for tag in tags:
                if tag['tag'] in new_name:
                    new_name = new_name.replace(tag['tag'], '')
                    new_path = os.path.join(output_dir, tag['folder'])
                    break
                    
            new_name = new_name.strip() #Remove any extra whitespace
            new_file = os.path.join(new_path, new_name)
            logging.info("\"" + os.path.join(working_dir, filename) + "\" -> \"" + new_file + "\"")
            os.rename(os.path.join(working_dir, filename), new_file)
            
for tag in tags:
    if len(os.listdir(os.path.join(output_dir, tag['folder']))) == 0:
        print("Clearing empty directory: " + os.path.join(output_dir, tag['folder']))
        os.rmdir(os.path.join(output_dir, tag['folder'])) #Remove any folders we created if they're still empty
            
print("Done! Processed %d files in %3.2f milliseconds!" % (num_files, (time.time() - START) * 1000.0))