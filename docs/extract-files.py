import argparse
import csv
import os
import re
import requests

# Tidy up - remove the pre-existing list of pages (if it exists)
if os.path.isfile("file_list.csv"):
    os.remove("file_list.csv")

# Set up the argument parser
parser = argparse.ArgumentParser(description='Specify the Discourse post number of the index page for your project')
parser.add_argument('index_no', type=int, help='Discourse post number of the index page')
parser.add_argument('project_name', type=str, help='Your project name, e.g. "Ubuntu Server documentation"')

# Parse the arguments
args = parser.parse_args()

index_url = f"https://discourse.ubuntu.com/raw/{args.index_no}"

response = requests.get(index_url)

if response.status_code == 200:
    data = response.text

# Find the start and end points of the navigation table
start_marker = "[details=Navigation]"
end_marker = "[/details]"
start_index = data.find(start_marker)
end_index = data.find(end_marker)

# Move the index to the start of the table
start_index += len(start_marker)

# Find the end of the table
end_index = data.find(end_marker, start_index)

# Extract table contents and split
table_contents = data[start_index:end_index].strip()
lines = table_contents.split("\n")

# Skip the first two lines, since they're related to the table header
table_lines = lines[2:]
csv_lines = [line.replace('|', ',') for line in table_lines]

with open("temp.csv", 'w') as csvfile:
    for csv_line in csv_lines:
        csvfile.write(csv_line + "\n")

# in this csv file:
# 0 is empty
# 1 is the nav number/level
# 2 is the slug (may be empty for level 0, 2 or 3)
# 3 contains either the Name or the [Name](link-inc-post-number)
#
# Based on this, we want to output:
# 0 slug
# 1 Name
# 2 Discourse post number
# 3 page type
# 4 Discourse url
# 5 Section
# 6 Subsection (if there is one)

# Tracking the contents we want to write:
actual_csv_contents = ""
# Set first line so we can skip the empty one at level 0
actual_csv_contents += f"index,{args.project_name},{args.index_no},landing page,/t/-/{args.index_no},--,--\n"

# Also want to track the page type, section and subsection
page_type_tracker = ""
section_tracker = ""
subsection_tracker = ""
section_change = ""
pattern = r'\[(.*?)\]\((.*?)\)'

# Open file and read info
with open("temp.csv", newline='', encoding='utf-8') as file:
    reader = csv.reader(file)

    # Loop over file and for each row, extract info and save page
    for index, row in enumerate(reader):
        # Save contents of row into more descriptive variables
        empty_row = row[0]
        nav_level = int(row[1])
        slug = row[2]
        slug = slug.strip()
        name_or_url = row[3]
        # Trim spaces from the front and back of strings
        name_or_url = name_or_url.lstrip()
        name_or_url = name_or_url.rstrip()

        match = re.search(pattern, name_or_url)
        if match:
            name = match.group(1)
            url = match.group(2)

            disc_number_match = re.search(r'\d{5}$', url)
            if disc_number_match:
                disc_number = disc_number_match.group(0)
            else:
                disc_number = ''
        else:
            name = name_or_url

        # Generally want these to reset every time so they're not carried
        # forward by accident
        page_slug = ""
        page_title = ""
        index_number = ""
        page_type = ""
        discourse_url = ""
        section_name = "--"
        subsection_name = "--"

        if slug != '':
            page_slug = slug
            discourse_url = url
            page_title = name
            index_number = disc_number

            if nav_level == 1:
                page_type = "landing page"
                section_name = "--"
                subsection_name = "--"
                page_type_tracker = page_slug
                actual_csv_contents += f"{page_slug},{page_title},{index_number},{page_type},{discourse_url},{section_name},{subsection_name}\n"
            else:
                section_name = section_tracker
                subsection_name = subsection_tracker
                page_type = page_type_tracker
                actual_csv_contents += f"{page_slug},{page_title},{index_number},{page_type},{discourse_url},{section_name},{subsection_name}\n"
        else:
            if nav_level == 2:
                section_tracker = name
                subsection_tracker = "--"
            else:
                subsection_tracker = name
        
        # Nav level 2 is only for headers, which are carried forward. However
        # This is done above, where the contents of the name_or_url column are
        # split out. 

        # Nav level 3 *could* be only content to be carried forward, or might
        # be a page. 
        # It's a page if there is a URL, otherwise it's a subsection to be 
        # carried forward. 
        # However, the subsection will want to change when the section does

with open("file_list.csv", "w") as final_csv:
    final_csv.write(actual_csv_contents)

# Tidy up - remove the temp file
os.remove("temp.csv")



# -----------------------------------------------------------------------------
# Notes
# -----------------------------------------------------------------------------

# Logic of csv file construction, could be either:
# | 0 |      | link |    # Level 0 = index
# | 1 | slug | link |    # Level 1 = landing page
# | 2 |      | Name |    # Level 2 = Subsection
# | 3 |      | Name |    # Level 3 = Sub-subsection
# | 4 | slug | link |    # Level 4 = page

# Or could be:
# | 0 |      | link |    # Level 0 = index
# | 1 | slug | link |    # Level 1 = landing page
# | 2 |      | Name |    # Level 2 = Subsection
# | 3 | slug | link |    # Level 3 = page

