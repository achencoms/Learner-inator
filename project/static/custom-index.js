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
  $("#loginClose").click(function(e) {
    $("#loginForm").find("input[type=text], input[type=password]").val("");
    $("#loginStatus").html('');
  });
  $("#registerClose").click(function(e) {
    $("#registerForm").find("input[type=text], input[type=password]").val("");
    $("#registerStatus").html('');
  });
  /* Validate password */
  $("#registerConfirmPassword").change(function(e) {
      icon = $("#confirmPasswordIcon");
      if (! icon.hasClass("glyphicon")) {
	  icon.addClass("glyphicon");
      }
      /* Check that password & confirm password not empty, then do the rest */
      /* debug to see why wrong passwords are getting checkmarks */
      /* get icon on one line */
      /* genetic cars? */
      if ($("#registerPassword").value != $("registerConfirmPassword").value) {
	  if (icon.hasClass("glyphicon-ok")) {
	      icon.removeClass("glyphicon-ok");
	  }
	  icon.addClass("glyphicon-remove");
      } else {
	  if (icon.hasClass("glyphicon-remove")) {
	      icon.removeClass("glyphicon-remove");
	  }
	  icon.addClass("glyphicon-ok");
      }
  });
});
