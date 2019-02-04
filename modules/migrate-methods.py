
from shutil import copyfile
from bs4 import BeautifulSoup
import os
import re


class MigrateChain():

    def __init__(self, input_dir, target_dir):
      self.input_dir = os.fsencode(input_dir)
      self.target_dir = os.fsencode(target_dir)

    def migrate(self):
        """
        Copies files and applies the methods to edit the files for Jekyll.
        """

        # Copy to new directory
        for f in os.listdir(self.input_dir):
            copyfile(f, self.target_dir)

        # Apply edits in new directory
        for f in os.listdir(self.target_dir):
            update_file_name(f)
            parse_paths(f)
            add_header_markup(f)


def update_file_name(infile):
    new_name = get_date(infile) + infile.name
    os.rename(infile, new_name)


def get_date(file):
    """
    Grabs the date from the <time> tag and replaces the `/` with `-`.
    Returns the parsed string.
    """
    soup = BeautifulSoup(file, 'html.parser')
    datetime = str(soup.time.string)
    date = re.search(r'[0-9]+\/[0-9]+\/[0-9]+', datetime).group()
    parsed_date = re.sub(r'\/', '-', date)
    # TODO: Swap the date format to YYY-MM-DD
    return parsed_date.strip()


def parse_paths(infile):
    """
    Helper method to edits the file paths in "src=..." and "href=..." file paths.
    """
    def has_src_or_href(tag):
        return tag.has_attr('href') or tag.has_attr('src')

    soup = BeautifulSoup(infile, 'html.parser')
    tags = soup.find_all(has_src_or_href)

    for tag in tags:
        if tag['href'] != None and tag['href'][:4] != "http":
            tag['href'] = '/'+tag['href']
        if tag['src'] != None and tag['href'][:4] != "http":
            tag['src'] = '/'+tag['src']

    # TODO: Not sure if the return type is correct
    return soup


# I know global variables are bad but it's 7:15 and I want to go home.
header ="""
---
layout: post
---
"""


def add_header_markup(infile):
    with open(infile, 'r') as original: data = original.read()
    with open(infile, 'w') as modified: modified.write(header + data)