# Md-table-of-contents-generator
Table of contents generated from headers of a markdown file. 

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

## License

