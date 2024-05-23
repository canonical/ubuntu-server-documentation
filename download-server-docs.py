#! /usr/bin/env python3

# Packages
import requests
import csv
import os
import re

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
file_with_nav = "main_landing_page.txt"
file_to_replace = "index.md"
with open(file_with_nav, 'r') as f:
    contents = f.read()
    
    with open(file_to_replace, 'w') as i:
        i.write(contents)


