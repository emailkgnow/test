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
import cgi
import re


form="""<form method="post">
    <h1 style='color:blue'>Please Enter some text to ROT13:.</h1>
    <br>
    <textarea name="text"
                style="height: 100px; width: 400px;">{my_encoded_input}</textarea>
    <input type="submit">
     <h3 style="color:red">Best Regards, The NSA </h3>
 </form>
"""


class MainHandler(webapp2.RequestHandler):

    def get(self):
        self.response.out.write(form.format(my_encoded_input=""))


    def post(self):
        user_input=self.request.get("text")
        new_encoded_input=mycodec(user_input)
        self.response.out.write(form.format(my_encoded_input= escape_html(new_encoded_input)))




def escape_html(s):
    "used to escape inputs that will effect  the form html like <br> for example "

    return cgi.escape(s,quote=True) #the True is to escape quotes also


def get_letter_postion(letter):
    "returns the position of the letter in the alphabet"

    cap="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    low="abcdefghijklmnopqrstuvwxyz"


    n=range(1,27)

    cap_table={x:y for x,y in zip(cap,n)}
    low_table={x:y for x,y in zip(low,n)}

    if letter in cap:
        return cap_table[letter]
    if letter in low:
        return low_table[letter]

def translate_letter(letter):
    "translates the letter using its position in the alphabet"

    cap="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    low="abcdefghijklmnopqrstuvwxyz"

    n=range(1,27)

    #note that the below dict comps are the opposite of the ones in the get_letter_position as here I want to get
    #  the letter
    cap_table={x:y for x,y in zip(n,cap)}
    low_table={x:y for x,y in zip(n,low)}
    try:
        letter_position = get_letter_postion(letter)
        new_letter_position=0

        if letter_position>13:
            new_letter_position=letter_position - 13
        else:
            new_letter_position=letter_position + 13
        new_letter=None
        for l in letter:
            if letter.isupper():
                return cap_table[new_letter_position]
            if letter.islower():
                return low_table[new_letter_position]
    except:
        return letter


def mycodec(word):
    'does the actual encoding and decoding'

    new_input=[]
    for i in word:
        translate_letter(i)
        new_input.append(translate_letter(i))
    return ''.join(new_input)

#################################################################################################################

form2='''<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
<form method="post"><h3>

    <label><b>Username</b></label>
                 <input type="text" name="username" value={username}>
                    <label style="color:red">{username_feedback}</label><br>

    <label><b>Password</b></label>
                 <input type="password" name="password" value={password}>
                    <label style="color:red">{password_feedback}</label><br>

    <label><b>Verify</b></label>
                 <input type="password" name="verify" value={verify}>
                    <label style="color:red">{verify_feedback}</label><br>

    <label><b>Email</b></label>
                 <input type="text" name="email" value={email}>
                    <label style="color:red" >{email_feedback}</label><br><br></h3>
    <input type="submit">

        </form>
</body>
</html>'''
class SignupHandler(webapp2.RequestHandler):

    def write_form(self,
                   input_username='',input_username_feedback='',
                   input_password='',input_password_feedback='',
                   input_verify='', input_verify_feedback='',
                   input_email='', input_email_feedback=''):


        self.response.out.write(form2.format(username=input_username,
                                             username_feedback=input_username_feedback,
                                             password=input_password,
                                             password_feedback=input_password_feedback,
                                             verify=input_verify,
                                             verify_feedback=input_verify_feedback,
                                             email=input_email,
                                             email_feedback=input_email_feedback))



    def get(self):
        self.write_form()


    def post(self):
        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
        user_email = self.request.get('email')

        user_username_wrong=''
        user_email_wrong=''

        username_feedback_wrong=''
        password_feedback_wrong=''
        verify_feedback_wrong=''
        email_feedback_wrong=''

        if (    self.check_username(user_username) and
                self.check_password(user_password) and
                self.check_verify(user_password,user_verify) and
                self.check_email((user_email))):
            self.redirect("/welcome?username="+user_username)
            #so we feed the username we need on the welcome page to the url and get it from there to use on the welcome page

        if not self.check_username(user_username):
            user_username_wrong=user_username
            username_feedback_wrong='try again'

        if not self.check_password(user_password):
            password_feedback_wrong='try again'

        if not self.check_verify(user_password,user_verify):
            verify_feedback_wrong='try again'

        if not self.check_email(user_email):
            user_email_wrong=user_email
            email_feedback_wrong='try again'

        self.write_form(input_username= user_username_wrong,
                                             input_username_feedback=username_feedback_wrong,
                                             input_password_feedback=password_feedback_wrong,
                                             input_verify_feedback=verify_feedback_wrong,
                                             input_email=user_email_wrong,
                                             input_email_feedback=email_feedback_wrong)


    def check_username(self,username):

        username_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return username_re.match(username)

    def check_password(self,password):
        password_re = re.compile(r"^.{3,20}$")
        return password_re.match(password)

    def check_verify(self,password,verify):
        if password==verify:
            return True
        else:
            return False

    def check_email(self,email):

        email_re = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
        return email_re.match(email)

class WelcomeHandler(webapp2.RequestHandler):
    '''this just uses the redirect concept as best practice after a user successfully/
    does something'''

    def get(self):
        user_name=self.request.get('username')
        self.response.out.write("<h1 style='color:red'>Thank You {my_username}!</h1>".format(my_username=user_name))


app = webapp2.WSGIApplication(
    [('/', MainHandler),('/signup',SignupHandler),('/welcome',WelcomeHandler)],
    debug=True)
