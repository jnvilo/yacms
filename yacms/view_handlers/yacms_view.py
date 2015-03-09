from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import


from django.conf import settings
from django.forms.models import model_to_dict
from loremipsum import generate_paragraphs
from creole import creole2html
import simplejson as json
from bs4 import BeautifulSoup
class YACMSViewObject(object):
    
    """
    A YACMSViewObject represents a full page object. It takes care of 
    coupling together the different pieces of a page such that it can 
    be serialized.  The YACMSViewObject handles the management of the 
    attributes of the CMSEntry model. 
    """
    def __init__(self, path=None, page_id=None, page_object=None):
        
        if  page_object:
            self.path = page_object.path.path
            self._page_id = page_object.id
            self._obj = page_object
        
        else:            
            self.path = path
            self._page_id = page_id
            self._obj = None

        x = __import__("yacms.view_handlers")
        y = getattr(x, "view_handlers")
        ViewClass  = getattr(y, self.page_object.page_type.view_class)
        instance =  ViewClass(self.page_object)
        self.view_handler = instance        
        
        
    def __getattr__(self, name):
        """Maps values to attributes.
        Only called if there *isn't* an attribute with this name
        """
        obj = self.view_handler
        
        try:
            value = getattr(obj, name)
            return value
        
        except AttributeError as e:
            return None
        
    @property
    def page_object(self, reload=False):
        """
        Loads the database entry object. Raises PageDoesNotExist
        """
       
        if (self._obj is None) or (reload):
            from yacms.models import CMSEntries
            if self.path:
                if not self.path.startswith("/"):
                    self.path =   "/" + self.path
                
                obj = CMSEntries.objects.get(path__path=self.path)
            elif self.page_id:
                obj = CMSEntries.objects.get(pk=self.page_id)
            else:
                raise RuntimeError("YACMSViewObject did not get a path or page_id.")
                
            self._obj = obj
            return obj
        
        else:
            return self._obj
       
    @property 
    def page_id(self):
        if self._page_id is None:
            self._page_id = self.page_object.id
        return self._page_id
    
    @page_id.setter
    def page_id(self, value):
        self._page_id = value
    
    @property
    def title(self):
        """The page title"""
        return self.page_object.title
        
    @property
    def created_timestamp(self):
        return self.page_object.date_created
    
    @property 
    def path_id(self):
        return self.page_object.path.id
    
    @property 
    def path_str(self):
        p = self.page_object.path.path
        return p
    
    @property
    def html_content(self):
        """The html content of the page"""
        
        #TODO: Fix me: This loads only the first content entry. 
        #      This should be updated to load by date.
    
        try:
            content_obj = self.page_object.content.all()[0]
        except IndexError as e:
            
            if settings.DEBUG:
                paragraphs = generate_paragraphs(5, start_with_lorem=False)
                p = ""
                for paragraph in paragraphs:
                    p =  unicode(paragraph[2]) + "\n\n" + p
                return creole2html(p)
               
            else:
                return "Error: There is no content for this page."
        
        #TODO: Fix me: right now hardcoded to creole.        
        _html_content =  creole2html(content_obj.content)
    
        
        return _html_content
    
    @property
    def meta_keywords(self):
        """Returns a string list of keywords."""
        pass
    
    @property
    def meta_author(self):
        """Returns the author of the page."""
        pass
    
   
    @property
    def date_modified(self):
        """Date the page was modified"""
        pass

    @property
    def introduction(self):
        #We use beautifulsoup to extract the first paragraph
        html_content = self.html_content
       
        soup = BeautifulSoup(html_content)
        intro = soup.find("p")
        return str(intro)
            
        
        
    

    
    @property
    def template(self):
        
        #If self.page_object.template is empty, then we're fucked because
        #this will raise an AttributeError
        try:
            tmpl  = self.page_object.template.name
        except AttributeError as e:
            #no specific template defined so we just use the default template
            tmpl = self.page_object.page_type.view_template
        
        
        """
        TODO: Fix this so that it is not forcing to 
        get templates from yacms and instead set another
        directory.
        """
        if not tmpl.startswith("yacms"):
            tmpl = "yacms/"+tmpl
            
        return tmpl

    
    @property
    def data(self):
        d =  model_to_dict(self.page_object)
        path_str = self.page_object.path.path
        d["path_str"] = path_str
        
        return d
    
    @property
    def json_data(self):
        value =  json.dumps(self.data)
        return value