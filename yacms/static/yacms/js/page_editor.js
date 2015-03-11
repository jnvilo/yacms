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
      

$(function(){
    /* On Document load, initialize the page_editor. Editing this in the web page. */ 
    var page_id = cmsentry_object.id;
    var cmsentries_url = "/cms/api/v1/cmsentries?id="+page_id; // the url to fetch.


    //Update the Content Editor
    if (cmsentry_object.content.length != 0 ){
        
        /* The model id of the content object we want can be obtained
        from the global cmsentry_object. This cmsentry_object is ensured
        to be present in the html header injected by a script.*/
    
        var content_id = cmsentry_object.content[0];
        var content_url = "/cms/api/v1/cmscontents?id=" + content_id;
        
        $.get(content_url, function(data) {
        /** Code here gets executed when success. data contains the response. **/
            result = data[0]["content"];
            cmsentry_object["content_object"] = data[0]; //tuck it away into cmsentry_object.
            cmsentry_object["context_text"] = result
        })
         .done(function() {
            $("#page_editor_textarea").val(cmsentry_object.context_text);
        
        })
        
    } else{
        $("#page_editor_textarea").val("Article has no content.");    
    }
    
    
    //Set the frontpage and publish values
    if (cmsentry_object.frontpage == true){
         $("#icon_frontpage").attr("class","icon-check");          
    }else{
        $("#icon_frontpage").attr("class","icon-check-empty");           
        
    }
    
    
    //Set the publish button value
    if (cmsentry_object.published == true){
        $("#icon_published").attr("class","icon-check");          
    }else{
        $("#icon_published").attr("class","icon-check-empty");           
    }
    
    
});


$('#button_frontpage').click(function(){
    console.log("clicked the button_frontpage");  
    
    var icon = $("#icon_frontpage").attr("class");
    console.log(icon);
    
    if (cmsentry_object.frontpage == true){
        cmsentry_object.frontpage = false;
    }else{
        cmsentry_object.frontpage = true;    
    }
        
    //Now make an ajax call to save the state.
    $.ajax({
       type: "PUT",
       url: "/cms/api/v1/cmsentries/",
       data:  { frontpage : cmsentry_object.frontpage, id: cmsentry_object.id }, // serializes the form's elements.
       success: function(data)
       {
            cmsentry_object["frontpage"] = data["frontpage"];
            console.log("Frontpage : ", cmsentry_object["frontpage"]);
            //Set the frontpage and publish values
            if (cmsentry_object.frontpage == true){
                console.log("Its True so setting icon to check");
                $("#icon_frontpage").attr("class","icon-check");   
            
            }else{
                console.log("setting icon to check-empty", cmsentry_object["frontpage"]);
                $("#icon_frontpage").attr("class","icon-check-empty");           
            }    
       }
    });
   
});


$('#button_published').click(function(){
    
    var icon = $("#icon_published").attr("class");
    if (cmsentry_object.published == true){
        cmsentry_object.published = false;
    }else{
        cmsentry_object.published = true;    
    }
        
    //Now make an ajax call to save the state.
    $.ajax({
       type: "PUT",
       url: "/cms/api/v1/cmsentries/",
       data:  { published : cmsentry_object.published, id: cmsentry_object.id }, // serializes the form's elements.
       success: function(data)
       {
            cmsentry_object["published"] = data["published"];
            console.log("published : ", cmsentry_object["published"]);
            //Set the published and publish values
            if (cmsentry_object.published == true){
                $("#icon_published").attr("class","icon-check");   
            
            }else{
                $("#icon_published").attr("class","icon-check-empty");           
            }    
       }
    });
   
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


$('#button_lorem_ipsum').click(function(){

    var url = "/cms/api/v1/loremipsum";
    $.ajax({
           type: "POST",
           url: url,
           data:  { "num_paragraphs" : 5 }, // serializes the form's elements.
           success: function(data)
           {
                console.log(data);
                $("#page_editor_textarea").val(data.content);
           }
          
         });
         
});
    