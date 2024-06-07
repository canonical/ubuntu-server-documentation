#! /usr/bin/env python3

# -----------------------------------------------------------------------------
# This script will copy the raw markdown code from Discourse and create pages
# for each in markdown. It will also download all images and save them into a
# subfolder within each Diataxis section to keep them tidy. 
#
# The script will then create Diataxis landing pages in restructuredtext (so
# Sphinx doesn't chuck a wobbly) that cross-reference those markdown files. 
# All of this is created automatically. For simplicity, I recommend following
# the same structure in the CSV, otherwise you'll have to modify the script. 
#
# You can automatically insert some text on the four Diataxis landing pages if
# you want introductory text.
#
# Section 1: Create page files + download/save images
# Section 2: Replace discourse post links with relative paths to file
# Section 3: 
# Section 4: 
# -----------------------------------------------------------------------------

# Packages to import
import csv
import os
import re
import requests
import shutil


# ----------- FUNCTIONS:
# Set length of heading underlines
def h1_underline(header_text):
    underline = ('*' * len(header_text))
    return underline

def h2_underline(header_text):
    underline = ('=' * len(header_text))
    return underline

# Extract image URLs from markdown lines
def extract_info(markdown_line):
    pattern = r'!\[.*?\]\((.*?)\)'
    matches = re.findall(pattern, markdown_line)
    return matches 


# ----------- INPUT:
# csv file containing pages to be downloaded/saved/organised. Each row in the
# csv file corresponds to a page in the Discourse documentation. Page slugs
# and index numbers (from the Discourse post) must be unique.
csv_file_list = 'file_list.csv'

# Introductory text inserted before any of the links/sections on the Diataxis
# landing pages. Change this to be appropriate for your product.
intros = ["intro_tutorial.txt", "intro_how-to.txt", "intro_explanation.txt", "intro_reference.txt"]


# ----------- STATIC VARIABLES:
# Declare variables that I can loop over when generating or checking against
# the Diataxis sections
root_dir = os.getcwd()
folders = ["tutorial", "how-to", "explanation", "reference"]
landing_pages = ["tutorial.rst","how-to.rst","explanation.rst","reference.rst"]

# The markdown script also copies all the comments, each separated by a dashed
# line - we want to exclude everything after this marker:
eof_marker = "-------------------------"

# File to store the mapping of numbers to filenames
num_to_filename = "filename_mapping.txt"


# ----------- CLEANUP PREVIOUS RUN:
# Remove all files and folders before re-downloading the current/up-to-date
# ones.
def clear_old_stuff():
# Remove previous Diataxis main landing pages.
    for page in landing_pages:
        if os.path.isfile(page):
            os.remove(page)  

    # Remove the subsections folder and all pages within, which provides the
    # Diataxis scaffolding (fully generated, not downloaded) -> remake folder.
    if os.path.isdir("subsections"):
        shutil.rmtree("subsections")
    os.mkdir("subsections")

    for folder in folders:
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        os.mkdir(folder)
        os.mkdir(os.path.join(folder, 'images')) 

# ----------------------------------------------------------------------------- 
# Section 1: Create page files + download/save images
# -----------------------------------------------------------------------------

# Call the function that cleans up the previous run
clear_old_stuff()

# Open file and read info
with open(csv_file_list, newline='', encoding='utf-8') as filelist:
    reader = csv.reader(filelist)

    # Loop over file and for each row, extract info and save page
    for index, row in enumerate(reader):

        # Save contents of row into more descriptive variables
        page_slug = row[0]
        page_title = row[1]
        index_number = row[2]
        page_type = row[3]

        # Since we are creating landing pages separately, we don't want to
        # save any file that has a page type of "landing page". 
        if page_type == 'landing page':
            continue

        # Get the raw markdown from each discourse post
        url = f"https://discourse.ubuntu.com/raw/{index_number}"
        print(f"getting {url}")

        # Create a MyST compatible heading anchor for the page from the file
        # name/slug - in this way we don't have to mess around with file paths
        myst_anchor = f"({page_slug})=\n"   
        
        # Save title from spreadsheet
        h1_title = f"# {page_title}\n"

        # Get page contents
        response = requests.get(url)
        if response.status_code == 200:
            # Create path for saving file (based on Diataxis).
            doc_filename = f"{page_type}/{page_slug}.md"

            # Split out header line, and ignore all content after the first
            # "eof_marker" (so that we exclude the comments and only include
            # the contents from the original post).
            split_header = response.text.split('\n')
            body_text = '\n'.join(split_header[1:])

            excluding_comments = []
            for line in split_header[1:]:
                if eof_marker in line:
                    break
                excluding_comments.append(line)

            excluding_comments = '\n'.join(excluding_comments)

            with open(doc_filename, "w") as contents:
                contents.write(myst_anchor)
                contents.write(h1_title)
                contents.write(excluding_comments)

            # Find lines in the original post that call images and download
            # them.
            for line in excluding_comments.split('\n'):

                # Markdown for calling images is in the form "![]()"
                if line.strip().startswith('!['):
                    images = extract_info(line)

                    for img in images:
                        try:
                            img_response = requests.get(img)

                            if img_response.status_code == 200:
                                # Create file using the filename from the URL
                                img_filename = os.path.join(f"{page_type}/images/", os.path.basename(img))

                                with open(img_filename, 'wb') as img_file:
                                    img_file.write(img_response.content)

                                print(f"Downloaded image {img} and saved as {img_filename}")

                            else:
                                print(f"Failed to download image {img}")

                        except Exception as e:
                            print(f"Error downloading image {img}: {e}")

        else:
            print(f"Failed to download page {url}")

# --------------------------------------------------------
# Section 2: Replace discourse post links with relative paths to file
# ----------------------------------------------------------------------------
#
# Replace links with filenames:
# - Loop through all newly created files and folders
# - Check location of destination file/folder and replace link accordingly
# Logic:
# - If in same folder, "slug.md"
# - If in next folder up, "../slug.md"
# - If one of the landing pages, "/folder/slug.md"
# - If in a different folder at same level, "../folder/slug.md"
#
# Although eventually we'll want to replace these with "ref" links, that can
# be future work - not sure if it will even work with combined rst/myst.

lookup_table = {}

# Open file and read info
with open(csv_file_list, newline='') as filelist:
    reader = csv.reader(filelist)

    # Loop over file and for each row, extract info and save page
    for index, row in enumerate(reader):

        # Save contents of row into more descriptive variables
        page_slug = row[0]
        page_title = row[1]
        index_number = row[2]
        page_type = row[3]
        url_to_replace = row[4]

        lookup_table[url_to_replace] = (page_slug, page_type)

# Search through all files and replace reference numbers
print("Searching markdown files: replacing reference numbers")
for folder in folders:
    folder_path = os.path.join(root_dir, folder)
    for subdir, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(subdir, file)
            if file_path.endswith(".md"):
                with open(file_path, 'r') as f:
                    file_content = f.read()

                    new_content = file_content
                    for url_to_replace, (page_slug, page_type) in lookup_table.items():
                        if url_to_replace in file_content:
                            if folder == page_type:
                                replacement = f'{page_slug}.md'
                            elif (folder != page_type) and (page_type == 'landing page'):
                                replacement = f'../{page_slug}.rst'
                            else:
                                replacement = f'../{page_type}/{page_slug}.md'
                            new_content = new_content.replace(url_to_replace, replacement)
                            print(f"Replaced {url_to_replace} in {file} with {replacement}")

                    # Write the new content back to the file if changes were made
                    if new_content != file_content:
                        with open(file_path, 'w') as f:
                            f.write(new_content)
print("Finished replacing reference numbers in markdown files")

# ---------------------------------------------------------------------------
# Diataxis and structure: landing pages for sections/topics
# ---------------------------------------------------------------------------

print("Creating topic landing pages")

# Opening the csv file again!
with open(csv_file_list, newline='') as filelist:
    reader = csv.reader(filelist)

    # Variable to track previous subsection and subsubsection names
    prev_pagetype = None
    prev_subsection = None
    prev_subsubsection = None
    doc_filename = None
        
    toc_contents = ""
    list_contents = ""
            
    # Loop over file and for each row, extract info
    for index, row in enumerate(reader):

        # Save contents of row into more descriptive variables
        page_slug = row[0]
        page_title = row[1]
        page_type = row[3]
        subsection_name = row[5]
        subsubsection_name = row[6]

        if subsection_name == '--':
            continue
            
        if subsection_name != prev_subsection:
            if doc_filename:    
                with open(doc_filename, "w") as contents:
                    contents.write(myst_anchor)
                    contents.write(h1_header)
                    contents.write(underline)
                    contents.write("\n\n")
                    contents.write(list_contents)
                    contents.write("\n")
                    contents.write(f".. toctree::\n")
                    contents.write(f"    :hidden:\n\n")
                    contents.write(toc_contents)
        

            # Re-initialise the contents counter
            toc_contents = ""
            list_contents = ""
            
            # Create the file for this subsection/section combo
            subsection = subsection_name.lower()
            subsection = subsection.replace(' ','-')
            doc_filename = f"subsections/{page_type}-{subsection}.rst"

            # Create the bits that need to be generated
            myst_anchor = f".. _{page_type}-{subsection}:\n\n"
            h1_header = f"{subsection_name}\n"
            underline = h1_underline(h1_header)
                
            if subsubsection_name != '--':
                list_contents += f"\n\n**{subsubsection_name}**\n\n"

            list_contents += f"* :ref:`{page_title} <{page_slug}>`\n"
            toc_contents += f"    {page_title} <../{page_type}/{page_slug}>\n"

            prev_subsection = subsection_name

        else:
            if (subsubsection_name != '--') and (subsubsection_name != prev_subsubsection):
                list_contents += f"\n\n**{subsubsection_name}**\n\n"

            list_contents += f"* :ref:`{page_title} <{page_slug}>`\n"
            toc_contents += f"    {page_title} <../{page_type}/{page_slug}>\n"
            
            prev_subsubsection = subsubsection_name

        with open(doc_filename, "w") as contents:
            contents.write(myst_anchor)
            contents.write(h1_header)
            contents.write(underline)
            contents.write("\n\n")
            contents.write(list_contents)
            contents.write("\n")
            contents.write(f".. toctree::\n")
            contents.write(f"    :hidden:\n\n")
            contents.write(toc_contents)
              

# ---------------------------------------------------------------------------
# Diataxis and structure: Diataxis landing pages
# ---------------------------------------------------------------------------

print("Creating Diaxtaxis landing pages")

# Create files
for page, folder, intro in zip(landing_pages, folders, intros):
    doc_filename = page

    toc_contents = ""
    list_contents = ""
    myst_anchor = ""
    h1_header = ""
            
    # Variable to track previous subsection and subsubsection names
    prev_subsection = None

    # Opening the csv file yet again!
    with open(csv_file_list, newline='') as filelist:
        reader = csv.reader(filelist)

        # Loop over file and for each row, extract info
        for index, row in enumerate(reader):

            # Save contents of row into more descriptive variables
            page_slug = row[0]
            page_title = row[1]
            page_type = row[3]
            subsection_name = row[5]

            if page_slug == folder:
                myst_anchor = f".. _{page_slug}:"
                h1_header = f"{page_title}"
                h1_ul = h1_underline(h1_header)
                
            if (page_type == folder) and (subsection_name != prev_subsection):
                subsection = subsection_name.lower()
                subsection = subsection.replace(' ','-')
                h2_ul = h2_underline(subsection_name)

                list_contents += f"{subsection_name}\n"
                list_contents += f"{h2_ul}\n\n" 
                list_contents += f".. include:: subsections/{page_type}-{subsection}.rst\n"                    
                list_contents += f"    :start-line: 4\n\n"
#                list_contents += f"    :end-before: .. toctree::\n\n"
                
                toc_contents += f"    subsections/{page_type}-{subsection}.rst\n"             

            prev_subsection = subsection_name

        with open(doc_filename, "a") as contents:
            # Create the bits that need to be generated 
            contents.write(f"{myst_anchor}\n\n")
            contents.write(f"{h1_header}\n")
            contents.write(f"{h1_ul}\n\n")

            contents.write(f".. include:: {intro}\n\n")

            contents.write(f"{list_contents}\n\n")

            contents.write(f".. toctree::\n")
            contents.write(f"    :hidden:\n")
            contents.write(f"    :titlesonly:\n\n")
            contents.write(toc_contents)

print("All done! Enjoy your offline Discourse docs \o/")
