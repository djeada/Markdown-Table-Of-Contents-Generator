from src.main import (
    is_using_html_tags,
    is_using_markdown_syntax,
    find_headers_html,
    find_headers_markdown,
)

html_file_contents = """
<h1>Title</h1>
<p>This is a paragraph.</p>
<h2>Subtitle</h2>
<p>This is a paragraph.</p>
<h1>Programs</h1>
<h2>Python</h2>
<p>This is a paragraph.</p>
<h2>Java</h2>
<p>This is a paragraph.</p>
<h2>C++</h2>
<p>This is a paragraph.</p>
<h1>Languages</h1>
<h2>English</h2>
<p>This is a paragraph.</p>
<h2>Spanish</h2>
<p>This is a paragraph.</p>
"""

markdown_file_contents = """
# Title
This is a paragraph.
## Subtitle
This is a paragraph.
# Programs
## Python
This is a paragraph.
## Java
This is a paragraph.
## C++
This is a paragraph.
# Languages
## English
This is a paragraph.
## Spanish
This is a paragraph.
"""


def test_is_using_html_tags():
    assert is_using_html_tags(html_file_contents)
    assert not is_using_markdown_syntax(html_file_contents)


def test_find_headers_html():
    depth_to_headers = {
        1: ["Title", "Programs", "Languages"],
        2: ["Python", "Java", "C++", "English", "Spanish", "Subtitle"],
        3: list(),
    }

    for depth, headers in depth_to_headers.items():
        expected = sorted(headers)
        actual = sorted(find_headers_html(html_file_contents, depth))
        assert expected == actual


def test_find_headers_markdown():
    depth_to_headers = {
        1: ["Title", "Programs", "Languages"],
        2: ["Python", "Java", "C++", "English", "Spanish", "Subtitle"],
        3: list(),
    }

    for depth, headers in depth_to_headers.items():
        expected = sorted(headers)
        actual = sorted(find_headers_markdown(markdown_file_contents, depth))
        assert expected == actual
