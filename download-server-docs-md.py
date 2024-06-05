#! /usr/bin/env python3

# Packages
import requests
import csv
import os
import re
import shutil
from glob import glob

root_dir = os.getcwd()
folders = ["tutorial", "how-to", "explanation", "reference"]
landing_pages = ["tutorial.md","how-to.md","explanation.md","reference.md"]

# csv file containing pages to be downloaded/saved/organised
csv_file_list = 'file-list.csv'

# The markdown script also copies all the comments, each separated by a dashed
# line - we want to exclude everything after this marker:
eof_marker = "-------------------------"

# File to store the mapping of numbers to filenames
num_to_filename = "filename_mapping.txt"

# Function to remove all files before re-downloading fresh ones
for folder in folders:
    folder_path = os.path.join(root_dir, folder)
    for subdir, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(subdir, file)
            os.remove(file_path)
            print(f"Removed {file_path}")

for page in landing_pages:
    os.remove(page)
  
# Function to extract image URLs from markdown lines
def extract_info(markdown_line):
    pattern = r'!\[.*?\]\((.*?)\)'
    matches = re.findall(pattern, markdown_line)
    return matches

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
            # Create path for saving file (based on Diataxis)
            if page_type != "landing page":
                doc_filename = f"{page_type}/{page_slug}.md"
            else:
                doc_filename = f"{page_slug}.md"

            # Split out header line, and ignore all content after the first
            # "eof_marker"
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

            # Find lines that call images and download them
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

# ---------------------------------------------------------------------------

# Replace links with filenames:
# - loop through all newly created files and folders
# - check location of destination file/folder and replace link accordingly
# Logic:
# - if in same folder, "slug.md"
# - if in next folder up, "../slug.md"
# - if one of the landing pages, "/folder/slug.md"
# - if in a different folder at same level, "../folder/slug.md"



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
                                replacement = f'../{page_slug}.md'
                            else:
                                replacement = f'../{page_type}/{page_slug}.md'
                            new_content = new_content.replace(url_to_replace, replacement)
                            print(f"Replaced {url_to_replace} in {file} with {replacement}")

                    # Write the new content back to the file if changes were made
                    if new_content != file_content:
                        with open(file_path, 'w') as f:
                            f.write(new_content)

# Search through all landing page files and replace reference numbers
for file in landing_pages:
    with open(file, 'r') as f:
        file_content = f.read()

    new_content = file_content
    for url_to_replace, (page_slug, page_type) in lookup_table.items():
        if url_to_replace in file_content:
            if page_type == 'landing page':
                replacement = f'{page_slug}.md'
            else:
                replacement = f'{page_type}/{page_slug}.md'
            new_content = new_content.replace(url_to_replace, replacement)
            print(f"Replaced {url_to_replace} in {file} with {replacement}")

    # Write the new content back to the file if changes were made
    if new_content != file_content:
        with open(file, 'w') as f:
            f.write(new_content)

# After all pages are present and correct, we need to add the Myst toctree
# to the four landing pages
for file, folder in zip(landing_pages, folders):
    with open(file, 'a') as f:
        f.write(f"\n\n```{{toctree}}\n")
        f.write(f":hidden:\n")
        
        with open(csv_file_list, newline='') as filelist:
            reader = csv.reader(filelist)

            # Loop over file and for each row, extract info and save page
            for index, row in enumerate(reader):

                # Save contents of row into more descriptive variables
                page_slug = row[0]
                page_type = row[3]

                if page_type == folder:
                    toctree_entry = f"{page_type}/{page_slug}.md"
                    f.write(f"{toctree_entry}\n")

        f.write("```")
        
# Now, finally, we need to replace the contents of main_landing_page into 
# the index.md page to get rid of the navigation and redirect tables
file_with_nav = ["main_landing_page.txt"]
file_to_replace = ["index.md"]

for navfile, replacement in zip(file_with_nav, file_to_replace):
    with open(navfile, 'r') as f:
        contents = f.read()
        
        with open(replacement, 'w') as i:
            i.write(contents)

# ---------------------------------------------------------------------------
# Diataxis and structure: landing pages for sections/topics
# ---------------------------------------------------------------------------

print("Creating topic landing pages")

if os.path.isdir("subsections"):
    shutil.rmtree("subsections")

os.mkdir("subsections")

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
                    contents.write(h1_title)
                    contents.write(list_contents)
                    contents.write("\n")
                    contents.write(f"```{{toctree}}\n")
                    contents.write(f":hidden:\n")
                    contents.write(toc_contents)
                    contents.write("```")        

            # Re-initialise the contents counter
            toc_contents = ""
            list_contents = ""
            
            # Create the file for this subsection/section combo
            subsection = subsection_name.lower()
            subsection = subsection.replace(' ','-')
            doc_filename = f"subsections/{page_type}-{subsection}.md"

            # Create the bits that need to be generated 
            myst_anchor = f"({page_type}-{subsection})=\n\n"       
            h1_title = f"# {subsection_name}\n\n"

            if subsubsection_name != '--':
                list_contents += f"\n\n**{subsubsection_name}**\n\n"
                
            list_contents += f"* {{ref}}`{page_title} <{page_slug}>`\n"
            toc_contents += f"{page_title} <../{page_type}/{page_slug}.md>\n"
            
            prev_subsection = subsection_name

        else:
            if (subsubsection_name != '--') and (subsubsection_name != prev_subsubsection):
                list_contents += f"\n\n**{subsubsection_name}**\n\n"

            list_contents += f"* {{ref}}`{page_title} <{page_slug}>`\n"
            toc_contents += f"{page_title} <../{page_type}/{page_slug}.md>\n"
            
            prev_subsubsection = subsubsection_name

        with open(doc_filename, "w") as contents:
            contents.write(myst_anchor)
            contents.write(h1_title)
            contents.write(list_contents)
            contents.write("\n")
            contents.write(f"```{{toctree}}\n")
            contents.write(f":hidden:\n")
            contents.write(toc_contents)
            contents.write("```")                

# ---------------------------------------------------------------------------
# Diataxis and structure: Diataxis landing pages
# ---------------------------------------------------------------------------

print("Creating Diaxtaxis landing pages")

tutorial_intro = f"This section of our documentation contains step-by-step tutorials to help outline what Ubuntu Server is capable of while helping you achieve specific aims.\n\nWe hope our tutorials make as few assumptions as possible and are broadly accessible to anyone with an interest in Ubuntu Server. They should also be a good place to start learning about Ubuntu Server in general, how it works, and what it's capable of.\n\n"

howto_intro = f"If you have a specific goal, but are already familiar with Ubuntu Server, our **how-to guides** have more in-depth detail than our tutorials and can be applied to a broader set of applications. They’ll help you achieve an end result but may require you to understand and adapt the steps to fit your specific requirements.\n\n"      

explanation_intro = f"Our explanatory and conceptual guides are written to provide a better understanding of how Ubuntu Server works and how it can be used and configured. They enable you to expand your knowledge, making the operating system easier to use.\n\nIf you're not sure how or where to get started with a topic, try our introductory pages for a high-level overview and relevant links (with context!) to help you navigate to the guides and other materials of most interest to you.\n\n"

reference_intro = f"Our reference section is used for quickly checking what software and commands are available, and how to interact with various tools.\n\n"

# Delete these after
folders = ["tutorial", "how-to", "explanation", "reference"]
landing_pages = ["tutorial.md","how-to.md","explanation.md","reference.md"]
intros = [tutorial_intro, howto_intro, explanation_intro, reference_intro]

# Remove previous landing pages
for page in landing_pages:
    if os.path.isfile(page):
        os.remove(page)

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
                myst_anchor = f"({page_slug})=\n\n"
                h1_header = f"# {page_title}\n\n"

            if (page_type == folder) and (subsection_name != prev_subsection):

                subsection = subsection_name.lower()
                subsection = subsection.replace(' ','-')
            
                list_contents += f"## {subsection_name}\n\n"
                list_contents += f"```{{include}} subsections/{page_type}-{subsection}.md\n"                    
                list_contents += f":start-line: 4\n"
                list_contents += f":heading-offset: 1\n"
                list_contents += f":end-before: ```\n"
                list_contents += f"```\n\n"
                
                toc_contents += f"subsections/{page_type}-{subsection}.md\n"             

            prev_subsection = subsection_name

        with open(doc_filename, "a") as contents:
            # Create the bits that need to be generated 
            contents.write(myst_anchor)
            contents.write(h1_header)
            contents.write(intro)

            contents.write(list_contents)

            contents.write("\n")
            contents.write(f"```{{toctree}}\n")
            contents.write(f":hidden:\n")
            contents.write(f":titlesonly:\n")
            contents.write(toc_contents)
            contents.write(f"```")

