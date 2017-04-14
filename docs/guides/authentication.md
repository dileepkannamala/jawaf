# Authentication

## Introduction

The basic idea is to provide optional, baked in authentication for Jawaf.

Rather than using templated views - authentication actions such as logging in and logging out will be managed via
POST operations to standard endpoints.

## Setup

By default jawaf.auth is in INSTALLED_APPS in `settings.py`, and you'll find entries in your project `routes.py` as well.
An extremely basic login view/form is provided as an example.

## Current Status

Very much in progress. Basic features are still being completed and will need reviewing.