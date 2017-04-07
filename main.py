#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import re
import cgi

#<!DOCTYPE html>
#<html lang=en>
#<head>
#    <title>UserSignup</title>
#    <link rel='stylesheet' type='text/css' href='stylesheet.css'/>
#</head>
#<body>
form="""
    <h2>User Signup</h2>
    <form method='post'>
        <label>Username: <input type='text' name='username' value='%(username)s'></label>
        <label style="color:red">%(username_error)s</label>
        <br>
        <br>
        <label>Password: <input type='password' name='password' value=''></label>
        <label style="color:red">%(pass_error)s</label>
        <br>
        <br>
        <label>Verify password: <input type='password' name='verify' value=''></label>
        <label style="color:red">%(verify_error)s</label>
        <br>
        <br>
        <label>Email (optional): <input type='text' name='email' value='%(email)s'></label>
        <label style="color:red">%(email_error)s</label>
        <br>
        <br>
        <input type='submit'>
    </form>
"""

    #</body>
#</html>

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class UserSignup(webapp2.RequestHandler):
    def write_form(self,username="",password="",verify="",email="",username_error="",pass_error="",verify_error="",email_error=""):
        self.response.out.write(form %{
                                        "username": username,
                                        "username_error": username_error,
                                        "password": password,
                                        "pass_error": pass_error,
                                        "verify": verify,
                                        "verify_error": verify_error,
                                        "email" : email,
                                        "email_error": email_error
                                        })
    def get(self):
        self.write_form()

    def post(self):
        user_name = self.request.get("username")
        user_pass = self.request.get("password")
        user_verify = self.request.get("verify")
        user_email = self.request.get("email")
        username_error = ""
        pass_error = ""
        verify_error = ""
        email_error = ""

        if not valid_username(user_name):
            username_error = "That is not a valid username"
        if not valid_password(user_pass):
            pass_error = "That is not a valid password"
        if user_pass != user_verify:
            verify_error = "Passwords do not match"
        if not valid_email(user_email):
            email_error = "That is not a valid email"

        if (not valid_username(user_name) or not valid_password(user_pass) or not (user_pass == user_verify) or not valid_email(user_email)):
            self.write_form(user_name, user_pass, user_verify, user_email,username_error,pass_error,verify_error,email_error)
        else:
            self.redirect('/welcome?username=' + user_name)

class WelcomePage(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.response.out.write('Welcome ' + username)
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([('/', UserSignup),
                            ('/welcome', WelcomePage)],
                            debug=True)
