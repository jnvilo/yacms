function show_images_overlay(element){

    
  console.log(element);
  var src = element["src"];
  var filename = src.substring(src.lastIndexOf("/")+1);
  //console.log(filename);
  //console.log(document.URL);
  //console.log(src);
  //console.log(window.location);
  
  document.getElementById("image-overlay").style.display = "block";
  //document.getElementById("image-overlay").visibility = "visible";
  //document.getElementById("image-overlay").cursor = "default";
}


function close_image_overlay(){
  document.getElementById("image-overlay").style.display = "none";

}


