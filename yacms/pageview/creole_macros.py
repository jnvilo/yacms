# coding: utf-8
from __future__ import division, absolute_import, print_function, unicode_literals

from xml.sax.saxutils import escape


from . creole_utils import get_pygments_lexer, get_pygments_formatter

try:
    from pygments import highlight
    PYGMENTS = True
except ImportError:
    PYGMENTS = False



def html(text):
    """
    Macro tag <<html>>...<</html>>
    Pass-trought for html code (or other stuff)
    """
    return text


def pre(text):
    """
    Macro tag <<pre>>...<</pre>>.
    Put text between html pre tag.
    """
    return '<pre>%s</pre>' % escape(text)

def code(ext, text):
    """
    Macro tag <<code ext=".some_extension">>...<</code>>
    If pygments is present, highlight the text according to the extension.
    """
    if not PYGMENTS:
        return pre(text)

    try:
        source_type = ''
        if '.' in ext:
            source_type = ext.strip().split('.')[1]
        else:
            source_type = ext.strip()
    except IndexError:
        source_type = ''

    lexer = get_pygments_lexer(source_type, code)
    formatter = get_pygments_formatter()

    try:
        highlighted_text = highlight(text, lexer, formatter).decode('utf-8')
    except:
        highlighted_text = pre(text)
    finally:
        #return highlighted_text.replace('\n', '<br />\n')
        return highlighted_text
    
    
def image(*args, **kwargs):
    
    width=kwargs.get("width", None)
    height=kwargs.get("height", None)
    text = kwargs.get("text", None)
    
    if text is None:
        return ""
    
    html = """
<div class="row-fluid">
<div class="span12">
    <div class="span2"></div>
    <div class="span8">
        <img src="__DOCUMENT_URL_REGEX_REPLACED__/{}" style="margin-bottom: 15px; margin-right:auto; margin-left:auto; display:block;"></img>
    </div>
    <div class="span2"></div>
</div>
</div>
    """
    
    #html = """
    #<div class="row-fluid">
        #<div class="span8">
            #<img src="__DOCUMENT_URL_REGEX_REPLACED__/{}" style="margin-bottom: 15px;"></img>
        #</div>
    #</div>
        #"""
            
    
    return html.format(text)
    