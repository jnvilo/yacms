
function readCMSCategories(content_id){
/* Does a GET for the content and updates the editor textarea.

API Version 1 defines the endpoint as: 

/cms/api/v1/cmscontents/{resource_id}/
*/
    console.log("readCMSContents called.");

    var id = view_json.id;
    url = "/cms/api/v2/cmsentries/"+  id + "/get_categories/"; 
    $.ajax({
        url: url,
        type: 'GET',
        error: function(){
            console.log("Failed to get cmscontent object");
        },
        success: function(data){
        
         
         
         } 
    });
    
}