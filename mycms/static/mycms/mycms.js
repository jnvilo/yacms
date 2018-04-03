

function on() {
        console.log("Showing overlay");
    document.getElementById("overlay").style.display = "block";
}

function close_admin_overlay() {
    document.getElementById("overlay").style.display = "none";
}

$("#close-admin-overlay-button").click(function(){
        console.log("close-admin-overlay-button clicked");
        close_admin_overlay();
        });
