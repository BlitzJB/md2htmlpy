from .client import Client
from .models import (
    Heading,
    Paragraph,
    List,
    ListItem,
    BlockQuote,
    Image
)

def render_md(file):
    return Client(file).render()