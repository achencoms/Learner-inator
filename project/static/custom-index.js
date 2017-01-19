$(document).ready(function(){
  $("#loginForm").submit(function(e) {
    e.preventDefault();
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
  $("#registerForm").submit(function(e) {
    e.preventDefault();
    console.log("we did it! ")
    $.ajax({
      type: "POST",
      url: "/register/",
      data: $(this).serialize(),
      success: function(response) {
        if (response == "true") {
          $("#registerFormButton").html("Signing Up ...");
           /*setTimeout("window.location. = '/home/';", 4000);*/
           window.location = "/home/";
        } else {
          $("#registerStatus").fadeIn(1000, function(){
            $("#registerStatus").html('<span class="text-danger">Username is taken.</span>');
        });
        }
      }
    });
  });
});
