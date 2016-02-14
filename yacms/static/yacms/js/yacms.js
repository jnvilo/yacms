function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		console.log("Doing ajaxSetup");
		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});

var csrftoken = Cookies.get('csrftoken');

$('input[name=title]').change(function() {
    var page_title = $("#CreateTitle").val();
    $("#CreateSlug").val(convertToSlug(page_title)); 

});


function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		var csrftoken = Cookies.get('csrftoken');
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

function create_cms_entry(path_obj){
	
	var title = $("#createpage_title").val();
	var slug = $("#createpage_slug").val();
	var page_type = $("#createpage_pagetype_select").val();
	
	var url = "/cms/api/v1/cmsentries/";
	var data = { path: path_obj.id, 
				title: title,	
				slig : slug,
				parent: path_obj.parent,
				page_type: page_type ,
				};
	
	console.log("Going to post cmsentry: ", data);
	$.ajax({
		url: url,
		type: 'POST',
		data: data,

		error: function(){ console.log("Failed to create CMS Entry"); },

		success: function(data){ 
			console.log("Created CMSEntry: " , data);	
			update_child_categories();
				
			
			
		}
	});



}


function create_path(parent_path_id){
	
	url = "/cms/api/v1/cmspaths/";
	var csrftoken = Cookies.get('csrftoken');
	var title = $("#createpage_title").val();
	var slug = $("#createpage_slug").val();
	var page_type = $("#createpage_pagetype_select").val();

	$.ajax({
		url: url,
		type: 'POST',
		data: { path: slug, parent: parent_path_id },

		error: function(){ console.log("Failed to create path"); },

		success: function(data){ 
			console.log("Created Path: " ,data);	
			
			//When path gets created then we create the content.
			create_cms_entry(data);
		
		
								
			
			
			
		}
	});

}


$("#createpage_button").click(function() {

	console.log("#createpage_button clicked.");
	var csrftoken = Cookies.get('csrftoken');
	var title = $("#createpage_title").val();
	var slug = $("#createpage_slug").val();
	var page_type = $("#createpage_pagetype_select").val();
	
	/**First get the cmsentry_object. Note that cmsentry_id is global var 
	that we defined in the header **/
	
	url = "/cms/api/v1/cmsentries/"+cmsentry_id+"/"; 

	$.ajax({
		url: url,
		type: 'GET',
		error: function(){
			console.log("Failed to get cmsentry object");
		},
		success: function(data){ 
			//On Success we create the path
			create_path(data.path);
			
		}
	});
	

	
	
	//Create the CMSPath 
	
	//Create A blank CMSContent
	
	//Create the CMSEntry

});


function get_cmsentry(){
	
	
	//Note the cmsentry_id is global defined in head of the html page.
	url = "/cms/api/v1/cmsentries/"+cmsentry_id+"/"; 
	
	 $.get(url, function(data) {
		/** Code here gets executed when success. **/
		console.log("Retrieved CMSEntry for this page: ", data);
		
		
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
 		console.log( "finished" );
		})

}



function update_child_categories(){

	/** 
	This updates the child categgories table. It is automagically executed
	whenever the page is loaded.
	**/
	
	

	url = "/cms/api/v1/cmsentries/?parent="+cmsentry_id; 

	console.log("Getting: ", url);
	$.get(url, function(data) {
		/** Code here gets executed when success. **/
		console.log("Retrieved Child Categories: ", data);
		
		//var source = $("#category_table_tmpl").html();
		//var compiled = dust.compile(source, "cat_tbl");
		//dust.loadSource(compiled);
		dust.render("category_table", {  values : data } , function(err,out){
		$("#category_table_output").html(out);		
		})
		
	})

	.fail(function() {
		/** Code here gets executed on fail **/
		alert( "error" );
		})

}


function handle_published_clicked(elem){

	
	
	console.log("Published clicked: ", elem.id, elem.innerHTML);
	var child_cmsentry_id = elem.getAttribute("child_cmsentry_id");
	var published = false; 
	
	//Update the page with a PUT depending on the current value.
	if (elem.innerHTML == "No"){
	
		console.log("its a no");
		published = true;
	}
	else{
		console.log("It's a Yes then")	;
		published = false;
	}

	url = "/cms/api/v1/cmsentries/"; 
	$.ajax({
		url: url,
		type: 'PUT',
		data: { id: child_cmsentry_id,published : published},

		error: function(data){ console.log("Publish Failed with error", data); },

		success: function(data){ 
			console.log("Updated published status of the page.: " ,data);	
			
			//When path gets created then we create the content.
			update_child_categories()
			
			
		}
	});
}

function handle_frontpage_clicked(elem){

	console.log("Frontpage clicked: ", elem.id, elem.innerHTML);
	var child_cmsentry_id = elem.getAttribute("child_cmsentry_id");
	var frontpage = false; 
	
	//Update the page with a PUT depending on the current value.
	if (elem.innerHTML == "No"){
	
		console.log("its a no");
		frontpage = true;
	}
	else{
		console.log("It's a Yes then")	;
		frontpage = false;
	}

	url = "/cms/api/v1/cmsentries/"; 
	$.ajax({
		url: url,
		type: 'PUT',
		data: { id: child_cmsentry_id,frontpage :frontpage},

		error: function(data){ console.log("Failed with error", data); },

		success: function(data){ 
			console.log("Updated frontpage status of the page.: " ,data);	
			
			//When path gets created then we create the content.
			update_child_categories()
			
			
		}
	});
	
}


function handle_frontpage_checked(elem){

	console.log("Frontpage checked: ", elem.id, elem.checked);
	url = "/cms/api/v1/cmsentries/"; 
	$.ajax({
		url: url,
		type: 'PUT',
		data: { id: view_json.id,frontpage : elem.checked},

		error: function(data){ console.log("Failed with error", data); },

		success: function(data){ 
			console.log("Updated frontpage status of the page.: " ,data);	
		
			
		}
	});
	
}

function handle_published_checked(elem){

	console.log("Published checked: ", elem.id);
	url = "/cms/api/v1/cmsentries/"; 
	$.ajax({
		url: url,
		type: 'PUT',
		data: { id: view_json.id,published : elem.checked},

		error: function(data){ console.log("Publish Failed with error", data); },

		success: function(data){ 
			console.log("Updated published status of the page.: " ,data);	
			
			
			
		}
	});
	
}

function get_content(content_id){

	console.log("Automatically loading content");
	
	url = "/cms/api/v1/cmscontents/?resource_id=" + content_id; 
	
	console.log(url);
	$.ajax({
		url: url,
		type: 'GET',
		error: function(){
			console.log("Failed to get cmsentry object");
		},
		success: function(data){ 
			//On Success we create the path
			console.log("get_content: ", data);
			$('#editor_textarea').val(data[0].content);
		}
	});
	
}







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



/** PAGE EDITOR CLICK HANDLERS **/

$('#editor_save_button').click(function() {
 
  var content = $('#editor_textarea').val();
 
  url = "/cms/api/v1/cmscontents/?include_html=True"; 
	$.ajax({
		url: url,
		type: 'PUT',
		data: { id:  view_json.content[0], content : content },

		error: function(data){ console.log("Publish Failed with error", data); },

		success: function(data){ 
			console.log("Updated published status of the page.: " ,data);	
	
			console.log(data);
			$("#page_body").html(data.html);
			
		}
	});

});


