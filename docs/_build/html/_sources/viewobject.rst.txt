ViewObject 
==============


The life of a page request
****************************

All page requests for a page is handled by the view class CMSPageView defined in mycms/views.py  





The viewobject wraps a CMSEntries instance and provides methods to load the 
required handler and pass it to the template. 


The core of a mycms page is the viewobject and the template. 

An instance of viewobject is passed to the template.
