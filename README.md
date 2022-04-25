# Md-table-of-contents-generator
Generate a table of contents from the headers of your markdown file.

## Purpose

This script will create a table of contents for a specified markdown file.
A table of contents may be generated for headers defined using html tags as well as headers defined with markdown syntax.
If the provided file already has a table of contents, the script will replace it with the new one.

## Installation

It is advisable to use virtualenv to install the program.

    git clone https://github.com/djeada/Markdown-table-of-contents-generator.git
    cd md-table-of-contents-generator
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Usage

Use the following command to display the help:

    cd md-table-of-contents-generator
    python md-table-of-contents-generator.py --help

Use the following command to generate the table of contents for a markdown file with the filename README.md and save it to the file README.md.toc: 

    python md-table-of-contents-generator.py --input=README.md --output=README.md.toc

## Contributing
It is an open source project, so feel free to contribute!

## License
This project is licensed under the <a href="https://github.com/djeada/Markdown-table-of-contents-generator/blob/master/LICENSE">MIT license</a>.
