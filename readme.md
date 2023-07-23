# Introduction
This web application is a support ticket/helpdesk system designed, implemented and tested by myself, Kyle Macdiarmid.

This application utilises Flask, SQLite and SQLAlchemy, to support development, and is driven by Python, HTML, CSS, and JavaScript. 

The database is included as a file - website/database.db, and is SQLite so a compatible DB Browser is required to view the data.

In this application, users have the ability to log new helpdesk tickets with a title and description. They can then manage their own ticket, modifying or deleting the ticket. Adminstrators can then view all open tickets from all users, modify them with responses, as well as delete them. Administrators can also manage all users.

# Logins:
## Administrator account
admin@qa.com
Admin123

## Regular user
user@qa.com
User123

# How to access
The  app can be started from the root of the project with the following command: "python main.py". Main.py is the entrypoint for the application.

Once logged in as an administrator, you can view all tickets, create new ones, make modifications, and delete tickets. 

Once logged in as a normal user, you can only see your own tickets, edit and create new tickets, as well as delete your own.

As an administrator, you can view all users on the "admin" tab and remove users.

# OWASP mitigations
## Cryptographic failures
To mitigate against this OWASP vulnerability, we use SHA256 hashing on all passwords to ensure that everything is encrypted end-to-end.
Evidence: https://prnt.sc/R1EQMsCTWZas

## Broken access controls
To mitigate against this vulnerability, we do a few things:
- @login_required - This is an attribute we can put on functions that enforces the need for a signed-in user before any code in that function can be run. 

We also lock down methods to certain HTTP request types (GET, POST) as required, and do extra permission checks when needed without external input to prevent users bypassing authentication by sending requests manually with administrator-like credentials.

Evidence: https://prnt.sc/aRLLBejlGML6 | https://prnt.sc/cx_xuX4YYznq 

## SQL Injection
We use form validation, as well as SQLAlchemy to prevent any chance of SQL injection.  For example, if we try to do a standard SQL injection attack in the login form, the form validation will fail.

Evidence: https://prnt.sc/6bFPbEJAtuKS | https://prnt.sc/Cu0phzaeT1QA | https://prnt.sc/SWuGpPOjeTvb

## Server-side request forgery
We protect against this vulnerability by limiting the number of external requests made. None of the python code makes external requests, the only external calls made are to the Bootstrap and JQuery CDN's.

Evidence: https://prnt.sc/ZaefbdAJTIr- | https://prnt.sc/7xYHBZcrJrC9
