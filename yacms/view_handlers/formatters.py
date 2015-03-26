from __future__ import division, absolute_import, print_function, unicode_literals
from loremipsum import generate_paragraphs
from yacms.creole import creole2html
from pprint import pformat
import simplejson as json

from django.conf import settings
import shlex
import ConfigParser
import StringIO

from xml.sax.saxutils import escape

try:
    from pygments import highlight
    from pygments.formatters.html import HtmlFormatter
    PYGMENTS = True
except ImportError:
    PYGMENTS = False

from yacms.creole.shared.utils import get_pygments_lexer, get_pygments_formatter

def html(text):
    """
    Macro tag <<html>>...<</html>>
    Pass-trought for html code (or other stuff)
    """
    return text

#----------------------------------------------------------------------
def  HTML(text):
    """"""
    return html(text)
    
def pre(text):
    """
    Macro tag <<pre>>...<</pre>>.
    Put text between html pre tag.
    """
    return '<pre>%s</pre>' % escape(text)


def code(*args, **kwargs):
    """
    Macro tag <<code ext=".some_extension">>...<</code>>
    If pygments is present, highlight the text according to the extension.
    """
    
    text = kwargs.get("text", None)
    ext = kwargs.get("ext", ".sh")
    nums = kwargs.get("nums",None)
    
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

    lexer = get_pygments_lexer(source_type, text)
    #formatter = get_pygments_formatter()

    try:
        if nums:
            formatter = HtmlFormatter(linenos='table',lineseparator="\n")
        else:
            formatter = HtmlFormatter(lineseparator="\n")
        highlighted_text = highlight(text, lexer, formatter).decode('utf-8')
    except:
        highlighted_text = pre(text)
    #finally:
    #    return highlighted_text.replace('\n', '<br />\n')

    return highlighted_text 
    
#----------------------------------------------------------------------
def  alertblock(text):
    """"""    
    template = """<div class="alert alert-block">{}</div>"""
    return template.format(text)

#----------------------------------------------------------------------
def  alerterror(text):
    """"""    
    template = """<div class="alert alert-error">{}</div>"""
    return template.format(text)

#----------------------------------------------------------------------
def  alertsuccess(text):
    """"""    
    template = """<div class="alert alert-success">{}</div>"""
    return template.format(text)

#----------------------------------------------------------------------
def  alertinfo(text):
    """"""    
    template = """<div class="alert alert-info">{}</div>"""
    return template.format(text)

#----------------------------------------------------------------------
def  infoblock(*args, **kwargs):
    """"""
    
    text = kwargs.get("text", "No text provided.")
    style = kwargs.get("style", "width: 400px; float: right; margin-left:10px")
    image = kwargs.get("image", None)
    author = kwargs.get("author", None)
    
    
    if image:
        image = """<div class="quote-photo"><img src="img/temp/user.jpg" alt=""></div>"""
    else:
        image = ""
        
    if author:
        author = """<div class="quote-author">James Livinston - <span>The New York Post</span></div>"""
    else:
        author=""
        
    template = """
<div class="boxinfo" style="{}">
        <div class="testimonials-user">{}<p>{}</p>{}</div>
</div>""".format(style,image, text, author)
    
    return template

    
#----------------------------------------------------------------------
def  image(*args, **kwargs):
    """
    We parse the content of the text to get the information about the image.
    
    """
    
    text = kwargs.get("text", None)
    image = kwargs.get("image", None)
    request = kwargs.get("request", None)
    
    
    if image is none:
        return "Image Not Provided!"
    
    
    return request.path

    #s_config = """
    #[example]
    #is_real: False
    #"""
    #buf = StringIO.StringIO(text)
    #config = ConfigParser.ConfigParser()
    #config.readfp(buf)
    #print config.getboolean('style', 'width')   
    
  
    
    
#----------------------------------------------------------------------
def  debug(*args, **kwargs):
        
    """"""
    
    print("Recieved args: {}".format(args))
    print("REcieved kwargs: {}".format(kwargs))
    for each in args:
        print(args)
        
    for each in kwargs:
        print(each)
        
    result =  "Recieved kwargs: {}".format(kwargs)
    return result
    
    
########################################################################
class  CreoleFormatter(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, raw_content=None, request=None):
        """Constructor"""
        self.raw_content = raw_content
        self.request = request
    #----------------------------------------------------------------------
    def  html(self, fake_content=False, request=None):
        """Returns the html"""
        
        if request is None:
            request = self.request
        if fake_content:
            paragraphs = generate_paragraphs(5, start_with_lorem=False)
            p = ""
            for paragraph in paragraphs:
                p =  unicode(paragraph[2]) + "\n\n" + p
            return creole2html(p)            
            
        return creole2html(self.raw_content, macros={ "code": code, 
                                                   "pre": pre,
                                                   "html": html,
                                                   "HTML":HTML,
                                                   "alertblock":alertblock,
                                                   "alertsuccess":alertsuccess,
                                                   "alertinfo":alertinfo,
                                                   "alerterror":alerterror,
                                                   "infoblock":infoblock,
                                                   "image": image,
                                                   "debug":debug,
                                                  }, 
                                           verbose=None,  
                                           stderr=None,
                                           request=request)
        
        
   