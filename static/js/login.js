
$(function() {

    $("#btnlogin").click(function() {
        $.ajax({
            url : "/validate",
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                if (response == 'success') {
                    window.location.replace("/user")
                }
                else {
                    var responseTag = "<div id = 'response'>" + response + "</div>"
                    $("#errorMessage").append(responseTag);
                    $("#errorMessage").removeClass("hid");
                    setTimeout(function() {
                        $("#errorMessage").addClass("hid");
                        $("#response").remove();
                    }, 1000);
                }
            },
            error: function(error) {
                console.log(error);
                var responseTag = "<div id = 'response'>" + error + "</div>"
                $("#errorMessage").append(responseTag);
                $("#errorMessage").removeClass("hid");
                setTimeout(function() {
                    $("#errorMessage").addClass("hid");
                    $("#response").remove();
                }, 1000);
            }
        });
    });
});