from dataclasses import dataclass
from typing import List
import argparse


@dataclass
class Config:
    file_name: str = 'README.md'
    output_file_name: str = 'README.md'
    table_of_contents_name: str = 'Table of Contents'
    depth: int = 2


@dataclass
class Tags:
    TABLE_CONTENTS_START: str = '<!--ts-->'
    TABLE_CONTENTS_END: str = '<!--te-->'

def parse_args():
    parser = argparse.ArgumentParser(description='Generate table of contents for README.md file.')
    parser.add_argument('-i', '--input', help='input file name', required=False)
    parser.add_argument('-o', '--output', help='output file name', required=False)
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

    headers = [line for line in file_contents.split('\n') if line.lstrip().startswith(f'#'*depth) and not line.lstrip().startswith(f'#'*(depth+1)) ]
    # filter out '#'*depth from lines
    headers = [header.replace(f'#'*depth, '') for header in headers]
    # strip whitespaces
    headers = [header.strip() for header in headers]

    return headers


def generate_table_of_contents(file_contents: str, table_of_contents_name: str, depth: int) -> str:
    '''
    Generate table of contents for file.
    '''
    if is_using_html_tags(file_contents):
        headers = find_headers_html(file_contents, depth)

    elif is_using_markdown_syntax(file_contents):
        headers = find_headers_markdown(file_contents, depth)

    headers = [f'- [{header.replace("-", " ")}](#{header})' for header in headers]

    table_of_contents: List[str] = [f'## {table_of_contents_name}', f'{Tags.TABLE_CONTENTS_START}\n'] + headers + [f'\n{Tags.TABLE_CONTENTS_END}']

    return '\n'.join(table_of_contents)


def is_table_of_contents_present(file_contents: str) -> bool:
    '''
    Check if table of contents is present in file.
    '''
    return Tags.TABLE_CONTENTS_START in file_contents and Tags.TABLE_CONTENTS_END in file_contents


def remove_table_of_contents(file_contents: str) -> str:
    '''
    Remove table of contents from file.
    '''
    #convert file_contents from str to list of strings 
    tmp = file_contents.split('\n')
    #find the index of the first line with Tags.TABLE_CONTENTS_START
    start = tmp.index(Tags.TABLE_CONTENTS_START)

    if start == -1:
        raise ValueError('Tags.TABLE_CONTENTS_START not found')

    print(start)
    #remove the line above the first line with Tags.TABLE_CONTENTS_START
    tmp = tmp[:start-1] + tmp[start:]
    #convert the list back to a string
    file_contents = '\n'.join(tmp)

    # remove everything between Tags.TABLE_CONTENTS_START and Tags.TABLE_CONTENTS_END
    start = file_contents.find(Tags.TABLE_CONTENTS_START)
    stop = file_contents.find(Tags.TABLE_CONTENTS_END) + len(Tags.TABLE_CONTENTS_END)

    file_contents = file_contents.replace(
        file_contents[start:stop], '')

    # check if there are empty lines after start
    while file_contents[start] == '\n':
        file_contents = file_contents[:start] + file_contents[start+1:]

    return file_contents


def main():
    config = parse_args()
    file_contents = open(config.file_name, 'r',  encoding="utf-8").read()

    if is_table_of_contents_present(file_contents):
        file_contents = remove_table_of_contents(file_contents)

    table_of_contents = generate_table_of_contents(file_contents, config.table_of_contents_name, config.depth)
    # put it on top of the file
    file_contents = table_of_contents + '\n\n' + file_contents.lstrip()
    open(config.output_file_name, 'w',  encoding="utf-8").write(file_contents)


if __name__ == '__main__':
    main()
