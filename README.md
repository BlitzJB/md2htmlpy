# Md2HTMLpy

Md2HTMLpy is a library to convert markdown to html while maintaining full control over conversion.

## Installation
```
pip install md2htmlpy
```

## Example
```md
# This is test.md file
find more information [here](http://www.moreinfo.com)
```
```py
from md2htmlpy import Client, Heading, render_md

Heading.set_attribute('class', 'test')
client = Client('test.md') 
print(client.render())

# <h1 class="test">This is test.md file</h1><p>find more information <a href="http://www.moreinfo.com">here</a></p>
```
or if you dont want to customise the generation, simply
```py
from md2htmlpy import render_md

print(render_md('test.md'))
```
## Links
[PyPI](https://pypi.org/project/md2htmlpy/)
[Github](https://github.com/blitzjb/md2htmlpy)