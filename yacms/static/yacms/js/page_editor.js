
function load_cmsentries_content(page_id){
    /**
    Does an ajax call to /cms/api/v1/cmsentries?id=page_id to retrieve
    the list of contents of the current page. 
    **/

    var content = "There is no content yet. Edit Me!";
    var url = "/cms/api/v1/cmsentries?id="+page_id; // the url to fetch.
    $.get(url, function(cmsentries) {
        /** Code here gets executed when success. data contains the response. **/
        var data = cmsentries[0];
        console.log(data["frontpage"]);
        console.log(data["content"]);
        console.log(data.frontpage);
        var content_ids = cmsentries[0].content;
        
        if (content_ids.length !=0){
            content = get_content_text(content_ids[0]);
        } 
        else
        {
                
        
        
        
        
        
        
        }
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
    
    return content;

}

$(function(){
    console.log("Loaded page_editor");

    //Create the static HTML
    content = load_cmsentries_content(page_data.cmsentry_id);
    var data =  { content : content };

    html = new EJS({url: '/static/yacms/js/templates/page_editor.ejs'}).render(data);
    $('#page_editor').html(html);

    
    

    

    console.log("Done");
});


