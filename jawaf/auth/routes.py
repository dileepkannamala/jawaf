from jawaf.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView

routes = [
    {'uri': 'login/', 'handler': LoginView.as_view()},
    {'uri': 'logout/', 'handler': LogoutView.as_view()},
    {'uri': 'password_change/', 'handler': PasswordChangeView.as_view()},
    {'uri': 'password_reset/', 'handler': PasswordResetView.as_view()},
]
