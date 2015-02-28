



function convertToSlug(Text)
{
    return Text
	.toLowerCase()
	.replace(/ /g,'-')
	.replace(/[^\w-]+/g,'')
	;
}

$('input[name=title]').change(function() {
    var page_title = $("#CreateTitle").val();
    $("#CreateSlug").val(convertToSlug(page_title)); 

});

//$('#CreateTable').find('tr').click( function(){

//if ( this.rowIndex != 0){    
    //var row = $(this).find('td:first').text();
    //var rows = document.getElementById("CreateTable").rows;
    //var next_row = rows[this.rowIndex + 1];
    //var next_row_text = 	$(next_row).find('td:first').text();
    //var next_row_text_startswith = next_row_text.substring(0,3)


//if (next_row_text_startswith == " - "){
    //alert("Not going to do anything");		
//}
//else{
    //$(this).after("<tr><td> - This is a new entry</td><td>another</td><td></td></tr>");
//}

//alert('You clicked ' + row);

//}else{

//console.log("Not going to do anything since you clicked the Headers.");
//}
//});


/** 
The SAVEBUTTON handlers. This takes care of the click event to submit the 
content that is being edited and then update the page.
**/

$("#SAVEBUTTON").click(function(){
 
    var csst = $.cookie('csrftoken');    
    var pathname = window.location.pathname;
    page_content = $("#EDITOR_TEXTAREA").val();
    
    var request = $.ajax({
	url: pathname + "?action=save_page",          
	type: "POST",
	data: { content : page_content, csrfmiddlewaretoken : csst },
	dataType: "json"
    });
    
    request.success(function(data){
    
	console.log(data.page_html)
	$("#CONTENT").html(data.page_html);
    
    });
    
});


$("#IPSUMBUTTON").click(function(){

    var csst = $.cookie('csrftoken');    
    var pathname = window.location.pathname;
   
    
    var request = $.ajax({
	url: pathname + "?action=get_ipsum",          
	type: "GET",
	dataType: "json"
    });
    
    request.success(function(data){
    
	console.log(data.paragraphs)
	$("#EDITOR_TEXTAREA").val(data.paragraphs);
    
    });
    
});

$("#FRONTPAGEBUTTON").click(function(){
    var csst = $.cookie('csrftoken');    
    var pathname = window.location.pathname;
   
    
    var request = $.ajax({
	url: pathname + "?action=toggle_frontpage",          
	type: "GET",
	dataType: "json"
    });
    
    request.success(function(data){
	if (data.frontpage == true){
	    $("#FRONTPAGEBUTTON").html('<i class="icon-check"></i><span>Frontpage</span>');	    
	}else {
	    $("#FRONTPAGEBUTTON").html('<i class="icon-check-empty"></i><span>Frontpage</span>');		
	}
    
    });
    
});


$("#PUBLISHPAGEBUTTON").click(function(){
    var csst = $.cookie('csrftoken');    
    var pathname = window.location.pathname;
   
    
    var request = $.ajax({
	url: pathname + "?action=toggle_publish",          
	type: "GET",
	dataType: "json"
    });
    
    request.success(function(data){
	if (data.published == true){
	    $("#PUBLISHPAGEBUTTON").html('<i class="icon-check"></i><span>Publish</span>');	    
	}else {
	    $("#PUBLISHPAGEBUTTON").html('<i class="icon-check-empty"></i><span>Published</span>');		
	}
    
    });
    
});





$("#SAVEBUTTON").mouseenter(function(){
    console.log("mouseenter");
});


$("#SAVEBUTTON").mouseleave(function(){
    console.log("mouseexit");
});

    $("#CreateButton").click(function() { 
        var csst = $.cookie('csrftoken');
        var page_title = $("#CreateTitle").val();
        var page_slug = $("#CreateSlug").val();
        var pathname = window.location.pathname;
        var handler_name = $('#PageType option:selected').attr('value');
        var request = $.ajax({
            url: pathname + "?action=make_page",          
            type: "POST",
            data: { page_type : handler_name, csrfmiddlewaretoken : csst, title : page_title , slug : page_slug },
            dataType: "json"
        });


	request.success(function(data){


    if (typeof(data.error_msg) !== 'undefined') {
        console.log("Got error: " + data.error_msg)
        var div = document.getElementById('notification');
        div.innerHTML = div.innerHTML +  "<div class=\"alert alert-error\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\">×</button>Error:  " + data.error_msg + "</div>";

    } else { 

    $('#CreateTitle').val("");
    $('#CreateSlug').val("")
    var edit_link = '<td><a href="' + data.absolute_url + '">Edit</a></td>'
    $('#CreateTable tr:first').after('<tr><td>'+  data.title + '</td><td>'+ data.path + '</td><a>' + edit_link + '</tr>');
    var div = document.getElementById('notification');
    div.innerHTML = div.innerHTML +  "<div class=\"alert alert-success\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\">×</button>Created: " + data.title + "</div>";
}
});


    request.fail(function( jqXHR, textStatus) {
        var div = document.getElementById('notification');
        div.innerHTML = div.innerHTML +  "<div class=\"alert alert-error\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\">×</button>Error:  " + textStatus + "</div>";
    });
});



$("#PAGE_META_BUTTON").click(function() { 
	
        var csst = $.cookie('csrftoken');
        var page_header_title = $("#PAGE_HEADER_TITLE").val();
	var date_submitted = $("#DATE_SUBMITTED_PICKER").val();
	var time_submitted = 	$("#TIME_SUBMITTED_PICKER").val();
	var date_modified = $("#DATE_MODIFIED_PICKER").val();
	var time_modified = $("#TIME_MODIFIED_PICKER").val();
	var meta_header = $("#META_HEADER").val();
	
         var pathname = window.location.pathname;
        var request = $.ajax({
            url: pathname + "?action=save_meta_data",          
            type: "POST",
            data: { json_page_header_title : page_header_title, 
		    csrfmiddlewaretoken : csst, 
		    json_date_submitted : date_submitted,
		    json_date_modified : date_modified,
		    json_meta_header : meta_header, 
		    json_time_submitted : time_submitted,
		    json_date_submitted : date_submitted,
		    },
            dataType: "json"
        });

	request.success(function(data){
	   
	    var div = document.getElementById("PAGE_META_MSG")
	    div.innerHTML = "<div class=\"alert alert-info\">" + data.message + "</div>";
	
	});
    
	request.fail(function( jqXHR, textStatus) {
	
	var div = document.getElementById("PAGE_META_MSG")
	    div.innerHTML = "<div class=\"alert alert-error\">" + data.message + "</div>";
	

	   
	});
});


$("#TOGGLE_EDITOR").click(function(){
 console.log("TOGGLE")
  $("#EDITOR_DIV").toggle();
});
