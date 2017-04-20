<html>
    <head>
        <script type="text/javascript" src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
        <script>
$(document).ready(function(){
    $('#submit').click(function(){
        var data = {
            'username': $('#username').val(),
            'password': $('#password').val(),
            'next': '${next}'
        }
        $.ajax({
            url: '/auth/login/',
            type : 'POST',
            dataType : 'json',
            data : JSON.stringify(data),
            success : function(result) { window.location = '${next}'; },
            error: function(xhr, resp, text) { console.log(xhr, resp, text); }
        })
    });
});
        </script>
    </head>
    <body>
    <form id="login_form" method="POST" action="/auth/login/">
        <label>Username:</label>
        <input id="username" name="username" type="text"/>
        <label>Password:</label>
        <input id="password" name="password" type="password"/>
        <input id="submit" type="button" value="login"/>
    </form>
    </body>
</html>