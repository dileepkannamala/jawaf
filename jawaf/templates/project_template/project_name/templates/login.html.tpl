<html>
    <body>
    <form method="POST" action="/auth/login/">
        <label>Username:</label>
        <input name="username" type="text"/>
        <label>Password:</label>
        <input name="password" type="password"/>
        <input name="next" type="hidden" value="${next}"/>
        <input type="submit" value="login"/>
    </form>
    </body>
</html>