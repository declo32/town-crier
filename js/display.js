//MAKE NOTE! All the paths are related to the index.html, NOT this file!
$(document).ready(function(){
    $(".time").text(new Date().toDateString())
    $.get("./slide.html", function(data){
        $(".school-announcement").append(data);
    })
})