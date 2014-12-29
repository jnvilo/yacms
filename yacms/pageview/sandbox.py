from bs4 import BeautifulSoup
import re

html = """
<h1>This is a test</h1>
sdfasdf
<h2>This is h2</h2>
sdfjasd sdfa jklasdf
asdfj

adsfja

<p>this is a para</p>
<h2>This is another h2</h2>
This is anotehr entry into there


<h2>this is the third H2</h2>
"""


i