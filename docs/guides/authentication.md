# Authentication

## Introduction

The basic idea is to provide optional, baked in authentication for Jawaf.

Rather than using templated views - authentication actions such as logging in and logging out will be managed via
POST operations to standard endpoints.

## Setup

By default jawaf.auth is in INSTALLED_APPS in `settings.py`, and you'll find entries in your project `routes.py` as well.
An extremely basic login view/form is provided as an example.

## Password Resets

Using [this article on password recovery](https://paragonie.com/blog/2016/09/untangling-forget-me-knot-secure-account-recovery-made-simple#secure-password-reset-tokens) as a guide, Jawaf provides an endpoints to help handle resets and a convenience method.

```python
from jawaf.auth.users import generate_password_reset_path
reset_path = generate_password_reset_path(user_id=5)
# Using an imaginary email sending method as an example:
send_reset_email(reset_url='https://%s/%s' % (site_base_url, reset_path))
```

Then you'd need to handle a `POST` to that url. Let's say it's to `https://example.com/auth/password_reset/MQ==/2VvJH0hCCfN8cQ7ozGcWpbvL4FpzUfvuY7x3RIB7BaHB0APLjOmyzeqr/`

Then a `POST` to that url with `username` and `new_password` in the posted json data will validate against the username and the url to ensure the username being edited is the same as the one granted temporary access by the url. If verified, the user's password will be changed and the link invalidated for further use.

Password reset links, when generated, will expire in a default of 3 hours (override in settings.py) or when accessed once.

## Current Status

Very much in progress. Basic features are still being completed and will need reviewing.