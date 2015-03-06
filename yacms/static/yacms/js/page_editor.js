
$(function(){
console.log("Loaded page_editor");

var data = { val: "hello"};
var b = tmpl("tmpl-demo", data);
console.log(b);
$('#page_editor').html(b);

console.log("Done");
});
