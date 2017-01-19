$(document).ready(function(){
  $("#loginForm").submit(function(e) {
    e.preventDefault();
    console.log("test");
    console.log($(this).serialize());
    $.ajax({
      type: "POST",
      url: "/login/",
      data: $(this).serialize(),
      success: function(response) {
        if (response == "true") {
          $("#loginFormButton").html("Signing In ...");
           /*setTimeout("window.location. = '/home/';", 4000);*/
           window.location = "/home/";
        } else {
          $("#loginStatus").fadeIn(1000, function(){
            $("#loginStatus").html('<span class="text-danger">Incorrect username or password.</span>');
        });
        }
      }
    });
  });
});
