Development Notes:
========================

Writing Page Editors 
***********************

Each new page type requires a way of creating and editing new pages.  For example a CategoryPage type, we need to be able to edit the content attribute
for the page. 

.. note:: 
  
  *  mycms/static/mycms/editor contains the js and css for the editor. 
  
  *  html is placed within the page template and shown when user clicks the edit page whenever ?toolbar=True is passed in the request param. 


Editors have three basic components: 

* javascript code - The javascript code is in mycms/static/mycms/editor. For example we have there the article.editor.js and category.editor.js which contains code for editing SinglePage and CategeryPage articles. 

* html code . This code exists within the page template . For the category page, this would be in mycms/templates/mycms/CategoryPage. 
The code for the editor starts as follows: 

.. code-block:: python
  
  {% if view_object.request.user.username == "admin" %}
    <div id="overlay">    
  
      the overlay allows us to put an overlay page where we render 
      the editor user interface. 
    
    
    </div>
  {% endif %}
  
  


* style sheets - All styles used for the editors should be in mycms/static/mycms/editor/

