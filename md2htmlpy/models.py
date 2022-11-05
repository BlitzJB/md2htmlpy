import re


class Element: 
    ...

class Heading(Element):
    props = {}

    def __init__(self, content: str, level: int = 1) -> None:
        self.content = content
        self.level = level

    
    def template(self):
        return f"<h{self.level}{self.generate_attributes()}>{self.content}</h{self.level}>"

    @classmethod
    def set_attribute(cls, key, value):
        cls.props[key] = value


    def generate_attributes(self):
        return ' ' + ' '.join([f'{attr[0]}="{attr[1]}"' for attr in self.props.items()]) if self.props else ''

class Paragraph(Element): 
    props = {}

    def __init__(self, content: str) -> None:
        self.content = content

    def template(self):
        self.parse_links()
        return f"<p{self.generate_attributes()}>{self.content}</p>"

    def parse_links(self):
        matches = re.findall('\[(.+?)\]\((.+?)\)', self.content)
        for match in matches:
            self.content = self.content.replace(f'[{match[0]}]({match[1]})', f'<a href="{match[1]}">{match[0]}</a>')

    @classmethod
    def set_attribute(cls, key, value):
        cls.props[key] = value


    def generate_attributes(self):
        return ' ' + ' '.join([f'{attr[0]}="{attr[1]}"' for attr in self.props.items()]) if self.props else ''

class List(Element): 
    list_items: list
    props = {}

    def __init__(self, type: str = 'unordered') -> None:
        self.type = 'ul' if type == 'unordered' else 'ol'
        self.list_items = []

    def append(self, list_item: 'ListItem'):
        self.list_items.append(list_item)

    def template(self):
        return f"<{self.type}{self.generate_attributes()}>{self.render_children()}</{self.type}>"

        
    def render_children(self):
        return ''.join([child.template() for child in self.list_items])

    @classmethod
    def set_attribute(cls, key, value):
        cls.props[key] = value


    def generate_attributes(self):
        return ' ' + ' '.join([f'{attr[0]}="{attr[1]}"' for attr in self.props.items()]) if self.props else ''

class ListItem(Element): 
    props = {}

    def __init__(self, content: str, type: str = 'unordered') -> None:
        self.content = content
        self.type = type

    def template(self):
        return f"<li{self.generate_attributes()}>{self.content}</li>"

    @classmethod
    def set_attribute(cls, key, value):
        cls.props[key] = value

    def generate_attributes(self):
        return ' ' + ' '.join([f'{attr[0]}="{attr[1]}"' for attr in self.props.items()]) if self.props else ''

class Link(Element): 
    props = {}

    def __init__(self, content: str) -> None:
        self.content = content

    @classmethod
    def set_attribute(cls, key, value):
        cls.props[key] = value


    def generate_attributes(self):
        return ' ' + ' '.join([f'{attr[0]}="{attr[1]}"' for attr in self.props.items()]) if self.props else ''

class Image(Element): 
    props = {}

    def __init__(self, src: str, alt_text: str) -> None:
        self.src = src
        self.alt_text = alt_text

    def template(self):
        return f'<img src="{self.src}" alt="{self.alt_text}"{self.generate_attributes()} />'

    @classmethod
    def set_attribute(cls, key, value):
        cls.props[key] = value


    def generate_attributes(self):
        return ' ' + ' '.join([f'{attr[0]}="{attr[1]}"' for attr in self.props.items()]) if self.props else ''

class BlockQuote(Element): 
    props = {}

    def __init__(self, content: str) -> None:
        self.content = content

    def template(self):
        return f"<q{self.generate_attributes()}>{self.content}</q>"

    @classmethod
    def set_attribute(cls, key, value):
        cls.props[key] = value


    def generate_attributes(self):
        return ' ' + ' '.join([f'{attr[0]}="{attr[1]}"' for attr in self.props.items()]) if self.props else ''

class LineBreak:
    def template(self):
        return "<br/>"
