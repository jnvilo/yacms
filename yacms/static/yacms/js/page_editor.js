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


function save_content(page_id){
    /** save_content **/         
    console.log("");
}
      
function load_content(content_id){
    var url = "/cms/api/v1/cmscontents?id=" + content_id;
    var result; 
    console.log("content_id is ", content_id);
   
    $.get(url, function(data) {
        /** Code here gets executed when success. data contains the response. **/
        console.log("AJAX: " , data[0]);

        result = data[0]["content"];
        
        //Save this data into the global cmsentry_object as content_text
        cmsentry_object["content_object"] = data[0];  
        console.log("Retrieved content: " , cmsentry_object["content_object"]);
        
        $("#page_editor_textarea").val(result);
        //With this we update the editor        
    });
    console.log("load_content returning: ", result );
}

function load_cmsentries_content(page_id){

    console.log("Entering : load_cmsentries_content");
    /**
    Does an ajax call to /cms/api/v1/cmsentries?id=page_id to retrieve
    the list of contents of the current page. 
    **/

    var url = "/cms/api/v1/cmsentries?id="+page_id; // the url to fetch.
    $.get(url, function(cmsentries) {
        /** Code here gets executed when success. data contains the response. **/
        var data = cmsentries[0];
        var content_ids = cmsentries[0].content;
        
        if (content_ids.length !=0){
            load_content(content_ids[0]);
            /* cmsentry_object to contain the content_id */  
            cmsentry_object["content_id"] = content_ids[0];
            console.log("Content ID: ", cmsentry_object["content_id"]);
            
        } 
        else{
            $("#page_editor_textarea").val("No page content");         
        }
    });
}

$(function(){
    /* Gets executed when the page loads */
    //Create the static HTML
    load_cmsentries_content(cmsentry_object.id);    
    console.log("Done");
});


$('#button_frontpage').click(function(){
    console.log("clicked the button_frontpage");  
    
    var icon = $("#icon_frontpage").attr("class");
    console.log(icon);
     
    if (icon == "icon-check-empty"){
        //Make ajax call 
        $("#icon_frontpage").attr("class","icon-check");          
    
    }else{
        $("#icon_frontpage").attr("class","icon-check-empty");           
    }
});


$('#button_save').click(function(){
    console.log("clicked the save button");
    
    var url = "/cms/api/v1/cmscontents/?include_html=True";
    var content = $("#page_editor_textarea").val();
        console.log(content);
        
        $.ajax({
           type: "PUT",
           url: url,
           data:  { content : content , id : cmsentry_object.content_object.id }, // serializes the form's elements.
           success: function(data)
           {
                $("#page_body").html(data.html);
           }
          
         });

});


$('#button_publish').click(function(){
    console.log("clicked the button_publish");  
    
    var icon = $("#icon_publish").attr("class");
    console.log(icon);
     
    if (icon == "icon-check-empty"){
        //Make ajax call 
        $("#icon_publish").attr("class","icon-check");          
    
    }else{
        $("#icon_publish").attr("class","icon-check-empty");           
    }
});