function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        var csrftoken = $.cookie('csrftoken');
       
        console.log(csrftoken);
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken",csrftoken);
        }
    }
});

function convertToSlug(Text)
{   /** 
    A simple sluggifier similar to what django will do.    
    **/
    return Text
    .toLowerCase()
    .replace(/ /g,'-')
    .replace(/[^\w-]+/g,'')
    ;
}


/** DISPLAY CHILD PAGES FUNCITONS **/

function update_childpages_table_state(){

    var page_id  = cmsentry_object.id //Get the id from the global cmsentry_object
    url = "/cms/api/v1/cmsentries?id="+page_id;
    
}


function get_child_categories(){
    /**  Get the list of child categories via AJAX. **/
    var parent_id = cmsentry_object.id;
    var page_type_id = cmsentry_object.page_type;

    url = "/cms/api/v1/cmsentries?parent=" + parent_id + "&expand=True&page_type=" + page_type_id; 
    
     $.get(url, function(data) {
        /** Code here gets executed when success. **/
        console.log(data);
        html = new EJS({url: '/static/yacms/js/templates/category_table.ejs'}).render({ cmsentry_objects : data });
        console.log(html);
        $("#category_table").html(html);
    })
    .done(function() {
        /** Code here gets executed also on success**/
        console.log( "second success" );
        })
        
    .fail(function() {
        /** Code here gets executed on fail **/
        alert( "error" );
        })
        
    .always(function() {
        /** This code will always execute after a request **/
        console.log( "finished" );
        })

    

}


$(function() {
    /** Update the category table list on document load.**/
    get_child_categories();    
});



/** CREATE PAGE FUNCTIONS **/
$('#createpage_title').blur(function() {
    /**
    When the user leaves the input we update the slug input with 
    a sluggified version of the title.
    **/
    
    var title =  $('#createpage_title').val();    
    slug = convertToSlug(title);
    $('#createpage_slug').val(slug);
    
 
});


function create_cmsentry(title, slug, page_type, path){
    /** 
    Creates a page given a title, slug, page_type and the path of the 
    current page.
    **/
    
    console.log(title);
    
    var data = { title: title, slug: slug, page_type: page_type, path: path};
    console.log("Going to send: " + data);
    url = "/cms/api/v1/cmsentries";
    $.ajax({
              type: "POST",
              url: url,
              data: data, // serializes the form's elements.
              success: function(data)
              {
                   console.log("created cmsentries: " +  data);
                   get_child_categories();
                   
                   //set notification that we have created succesfully.
                   //var template = 
                   //html = html = new EJS({text: template}).render(data) 
                    var message = "Succesfully created : " + title;
                    alertsuccess(message, "notifications");
                    asdfd
                   
                   
              }
        });
          
}


$("#createpage_button").click(function() {
    /**
    The createpage form button click handler. When the user clicks the button,
    we want to post the  contents of the form to  the api backend.
    
    This also calls create_cmsentry after it has created the new     
    **/
    
    
    console.log("#createpage_button clicked.");
    var csrf = $.cookie()
    var data = $("#createpage_form").serialize();
    
    var title =  $('#createpage_title').val();    
    var slug  =  $('#createpage_slug').val();
    var page_type = $('#createpage_pagetype_select').val();
    console.log("Page_type ", page_type);
     
    var path = ""
    
    console.log("CMSENTRY: ", cmsentry_object);
    if (cmsentry_object.path_str == "/"){
        path = "/" + slug;        
    } else{
        path = cmsentry_object.path_str + "/" + slug;    
    }
    
    data = { path : path , parent : cmsentry_object.id , csrf:csrf};
    console.log(data);
    
    var url = "/cms/api/v1/cmspaths/"; // the script where you handle the form input.

    $.ajax({
           type: "POST",
           url: url,
           data: data, // serializes the form's elements.
           success: function(data)
           {
                console.log("created path: " +  data.path);
                create_cmsentry(title, slug, page_type, data.id);                
           }
          
         });

    return false; // avoid to execute the actual submit of the form.
});


(function($, window) {
  $.fn.replaceOptions = function(options) {
    var self, $option;

    this.empty();
    self = this;

    $.each(options, function(index, option) {
      $option = $("<option></option>")
        .attr("value", option.value)
        .text(option.text);
      self.append($option);
    });
  };
})(jQuery, window);


$(function() {
    /** Initialize the state when the page is loaded. **/   
   
    var url = "/cms/api/v1/cmspagetypes";
    
    $.get(url, function(data) {
        /** Code here gets executed when success. **/
        
        var option_array = [];
        
        for ( x=0 ;x < data.length; x++) {
            
            option_array.push({text: data[x].text, value: data[x].id})
           
        }
        console.log(option_array);
        $('#createpage_pagetype_select').empty();
        $('#createpage_pagetype_select').replaceOptions(option_array);
        
    })
   
   
});