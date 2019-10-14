from mycms.pages import CMSPage


class IndexPage(CMSPage):
    
    class Meta:
        help_text = "This is the Index Page Implementation"
        display_name = "Index"
        page_type = "index"
        

class CategoryPage(CMSPage):
    
    class Meta:
        help_text = "This is the Index Page Implementation"
        display_name = "Index"
        page_type = "index"
    
    