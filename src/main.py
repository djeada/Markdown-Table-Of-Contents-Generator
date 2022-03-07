from dataclasses import dataclass
from typing import List
import argparse


@dataclass
class Config:
    file_name: str = 'README.md'
    table_of_contents_name: str = 'Table of Contents'


def parse_args():
    parser = argparse.ArgumentParser(description='Generate table of contents for README.md file.')
    parser.add_argument('-f', '--file', help='file name', required=False)
    parser.add_argument('-t', '--table-of-contents', help='table of contents name', required=False)

    args = parser.parse_args()
    config = Config()
    if args.file:
        config.file_name = args.file
    if args.table_of_contents:
        config.table_of_contents_name = args.table_of_contents

    return config


def is_using_html_tags(file_contents: str) -> bool:
    '''
    Check if file is using html tags for declaration of headers.
    '''
    html_tags = (f'<h{i}>' for i in range(1, 6))
    return any(tag in file_contents for tag in html_tags)


def is_using_markdown_syntax(file_contents: str) -> bool:
    '''
    Check if file is using markdown syntax for headers.
    '''
    return '#' in file_contents


def find_headers_html(file_contents: str, depth: int = 1) -> List[str]:
    '''
    Find headers in file.
    '''
    if depth < 1 or depth > 6:
        raise ValueError('Depth must be between 1 and 6')

    headers = [line for line in file_contents.split('\n') if f'<h{depth}>' in line]
    # filter out <h{depth}> </h{depth}> from lines
    headers = [header.replace(f'<h{depth}>', '').replace(f'</h{depth}>', '') for header in headers]
    # strip whitespaces
    headers = [header.strip() for header in headers]

    return headers


def find_headers_markdown(file_contents: str, depth: int = 1) -> List[str]:
    '''
    Find headers in file.
    '''
    if depth < 1 or depth > 6:
        raise ValueError('Depth must be between 1 and 6')

    headers = []
    # get the whole line after the header #
    # add it to the list of headers
    for i in range(file_contents.find('#' * depth), len(file_contents)):
        if file_contents[i] == '\n':
            headers.append(file_contents[file_contents.find('#' * depth) + depth:i])

    return headers


def generate_table_of_contents(file_contents: str, table_of_contents_name: str) -> str:
    '''
    Generate table of contents for file.
    '''
    if is_using_html_tags(file_contents):
        headers = find_headers_html(file_contents)

    elif is_using_markdown_syntax(file_contents):
        headers = find_headers_markdown(file_contents)

    headers = [f'- [{header.replace("-", " ")}](#{header})' for header in headers]

    table_of_contents: List[str] = [f'## {table_of_contents_name}', '<!--ts-->\n'] + headers + ['\n<!--te-->']

    return '\n'.join(table_of_contents)


def is_table_of_contents_present(file_contents: str) -> bool:
    '''
    Check if table of contents is present in file.
    '''
    return '<!--ts-->' in file_contents and '<!--te-->' in file_contents


def remove_table_of_contents(file_contents: str) -> str:
    '''
    Remove table of contents from file.
    '''
    # find in which line <!--ts--> appears
    start_line = file_contents.find('<!--ts-->')
    # remove two lines above <!--ts-->
    file_contents = file_contents[:start_line - 2] + file_contents[start_line:]
    # remove everything between <!--ts--> and <!--te-->
    file_contents = file_contents.replace(
        file_contents[file_contents.find('<!--ts-->'):file_contents.find('<!--te-->') + 8], '')
    return file_contents


def main():
    config = parse_args()
    file_contents = open(config.file_name, 'r').read()

    if is_table_of_contents_present(file_contents):
        file_contents = remove_table_of_contents(file_contents)

    table_of_contents = generate_table_of_contents(file_contents, config.table_of_contents_name)
    # put it on top of the file
    file_contents = table_of_contents + '\n\n' + file_contents
    open(config.file_name, 'w').write(file_contents)


if __name__ == '__main__':
    main()
