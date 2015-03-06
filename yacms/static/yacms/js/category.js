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


$('#createpage_title').blur(function() {
    /**
    When the user leaves the input we update the slug input with 
    a sluggified version of the title.
    **/
    
    var title =  $('#createpage_title').val();    
    slug = convertToSlug(title);
    $('#createpage_slug').val(slug);
    
 
});


function to_url(parent_path, slug){

    var path;
    
    if (parent_path != "/"){
        path = parent_path + "/" + slug;
    }else{
        path = "/" + slug;
    }    
    var url = "<a href=\"/cms"+ path  + " \">" + path + "</a>" ;
    console.log(url);
    return url
}

function create_child_cmsentries_table(data){

    var t = "<table  class=\"table table-hover\">";
    t = t + "<thead><tr><th>Title</th><th>Path</th><th>Published</th></tr></thead><tbody>";
    
    for (var x = 0; x < data.length; x++){
    
        t = t + "<tr>";
        t = t + "<td>"+ data[x].title +"</td>";
        t = t + "<td>"+ to_url(cmsentry_object.path_str,data[x].slug) +"</td>";
        t = t + "<td></td></tr>";
        
        console.log(data[x]) ;          
    }
    
    t = t + "</tbody></table>";
    $("#cmsentries_table").html(t);

}

function update_cmsentries_list(parent_id){
    // This gets the list of cmsentries and updates the table.
  
    url = "/cms/api/v1/cmsentries/?parent_id=" + parent_id;      
    $.get( url, function(data) {
        /** Code here gets executed when success. 
        We get a list of cmsentries.        
        **/
                    
        create_child_cmsentries_table(data);
            
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
   });
}

$(function() {
    update_cmsentries_list(cmsentry_object.id);
});

function create_cmsentry(title, slug, page_type, path){
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
                   update_cmsentries_list(cmsentry_object.id);    
              }
        });
}



$("#createpage_button").click(function() {
    /**
    The createplage form button click handler.
    When the user clicks the button , we want to post the 
    contents of the form to  the api backend.
    **/
    var csrf = $.cookie()
    var data = $("#createpage_form").serialize();
    
    var title =  $('#createpage_title').val();    
    var slug  =  $('#createpage_slug').val();
    var page_type = $('#createpage_pagetype_select').val();
    console.log("Page_type ", page_type);
     
    var path = ""
    
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
   
});