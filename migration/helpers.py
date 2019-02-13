
from distutils.dir_util import copy_tree
from bs4 import BeautifulSoup
import os
import re


def copy_files(input_dir, output_dir):
    if [f for f in os.listdir(output_dir) if not f.startswith('.')]:
        raise Warning("Output directory is not empty! Stopping operation.")

    copy_tree(input_dir, output_dir)
    return None


def update_file_name(infile):
    """
    Renames the file to Jekyll format: YYYY-MM-DD-your file name.html
    :param infile: The path to the file.
    :return: None. The file name is pre-pended in-place.
    """
    new_name = get_date(infile) + '-' + os.path.basename(infile)
    full_new_path = os.path.join(os.path.dirname(infile), new_name)
    os.rename(infile, full_new_path)
    return None


def get_date(filename):
    """
    Grabs the date from the <time> tag and replaces the `/` with `-`.
    Returns the parsed string.
    """
    soup = BeautifulSoup(open(filename, encoding='utf-8'), 'html.parser')
    datetime = str(soup.time.string)
    date = re.search(r'[0-9]+\/[0-9]+\/[0-9]+', datetime).group().strip()
    date_parts = re.split(r'\/', date)
    order = [2, 0, 1]  # year, month, day
    reordered = [date_parts[i] for i in order]
    return '-'.join(reordered)


def edit_src_and_href_paths(infile):
    """
    Helper method to edits the file paths in "src=..." and "href=..." file paths.
    """

    def has_src_or_href(tag):
        # Closure to check if a tag has "href" or "src" attributes
        return tag.has_attr('href') or tag.has_attr('src')

    def is_css(tag):
        # Find the CSS to remove later
        return tag.name == 'link'

    prefix = '{{ site.baseurl }}/'

    soup = BeautifulSoup(open(infile, encoding='utf8'), 'html.parser')
    tags = soup.find_all(has_src_or_href)

    for tag in tags:
        # Don't edit any http references
        if 'href' in tag.attrs:
            if tag['href'].strip()[:4] != "http":
                tag['href'] = prefix+tag['href']
        elif 'src' in tag.attrs:
            if tag['src'].strip()[:4] != "http":
                tag['src'] = prefix+tag['src']

    # Remove CSS
    [s.extract() for s in soup.find_all(is_css)]

    _write_soup(infile, soup)

    return None


def get_html_files(target_dir):
    """
    Returns the list of html files in the directory(because we also copy the images, JS, and CSS.)
    :param target_dir:
    :return: A list of the files
    """
    return [os.path.join(target_dir, f) for f in os.listdir(target_dir) if f.endswith(".html")]


def remove_title_tag(infile):
    """
    Removes firs instance of a <title>...</title>
    :param infile:
    :return:
    """
    soup = BeautifulSoup(open(infile, encoding='utf8'), 'html.parser')
    soup.find(class_='entry-title').extract()
    _write_soup(infile, soup)


def add_header_markup(infile):
    """
    Adds the frontmatter to the posts. Adds field to hide the excerpts for these posts, as Jekyll cannot correctly
    display excerpts from the HTML. (It expects markdown).
    :param infile: String with file path.
    :return:
    """
    md_markup = """\
---
layout: post
hide_excerpt: true
---
"""
    with open(infile, 'r', encoding='utf-8') as original:
        data = original.read()
    with open(infile, 'w', encoding='utf-8') as modified:
        modified.write(md_markup + data)


def _write_soup(file_path, soup):
    """
    Writes a soup to a file.
    :param file_path: String with file path
    :param soup: BeautifulSoup object
    :return: None, edits the file in place.
    """
    with open(file_path, 'w+', encoding='utf-8', errors='replace') as f:
        f.truncate(0)
        f.write(str(soup))

    return None
