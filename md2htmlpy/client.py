import contextlib
from .models import (
    Heading,
    Paragraph,
    List,
    ListItem,
    BlockQuote,
    Image,
    LineBreak
)
from os import PathLike
from typing import Literal
import re

def find_largest_substring(char, line):
    if char not in line:
        return False
    len_ = 1
    while True:
        if char * len_ not in line:
            return len_-1
        len_ += 1


class Client: 
    def __init__(self, file: PathLike) -> None:
        self.f = open(file, 'r')
        self.props = {}

    
    def set_props(self, element: Literal['Heading', 'Paragraph', 'List', 'ListItem', 'Link', 'Image'], **props: dict):
        self.props[element.lower()] = props

    
    def render(self):
        lines = self.f.readlines()
        elements = []

        # matching different possibilities for the elements
        # Wanted to use the new match in python, but that would mean we loose compatibility for python<3.10
        for index, line in enumerate(lines):
            if line.endswith('\n'):
                if line == '\n':
                    with contextlib.suppress(IndexError):
                        if lines[index+1] == '\n':
                            elements.append(LineBreak())
                    continue
                else:
                    line = line[:-1:]
            if line.startswith('#'):
                level = find_largest_substring('#', line)
                elements.append(Heading(level=level, content=line[level+1::]))
            elif line.startswith('-') or line.startswith(' -'):
                if line.startswith('-'):
                    elements.append(ListItem(type='unordered', content=line[2::]))
                elif line.startswith(' -'):
                    elements.append(ListItem(type='unordered', content=line[3::]))
            elif line.startswith('!'):
                # TODO: handle limitation: would yeet other contents in the line with the image
                match = re.findall('!\[(.+?)\]\((.+?)\)', line)
                if not match:
                    continue
                elements.append(Image(src=match[0][1], alt_text=match[0][0]))
            elif line.startswith('>'):
                elements.append(BlockQuote(content=line[2::]))
            else:
                if isinstance(elements[-1], Paragraph):
                    # If the previous line was a paragraph, add this into that paragraph itself
                    elements[-1].content += line
                else:
                    elements.append(Paragraph(content=line))
        
        # Parsing for ListItems and putting them into List instances
        current_list: List | None = None
        outlist = []
        for element in elements:
            if isinstance(element, ListItem):
                if not current_list:
                    current_list = List(type=element.type)
                current_list.append(element)
            else:
                if current_list:
                    outlist.append(current_list)
                    current_list = None
                outlist.append(element)

        # Triggering rendering of induvidual elements and returning
        return ''.join([elem.template() for elem in outlist])
            