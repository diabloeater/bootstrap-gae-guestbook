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
import cgi
import datetime
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users

guestbook_key = ndb.Key('Guestbook', 'default_guestbook')

class Greeting(ndb.Model):
  author = ndb.UserProperty()
  content = ndb.TextProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
  def get(self):    
    self.response.out.write("""<!DOCTYPE html><html lang="en"><head>            
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1,  user-scalable=no">
            <meta name="description" content="">
            <meta name="author" content="">
            <title>Guestbook</title>
            <link href="resource/bootstrap/bootstrap.min.css" rel="stylesheet">
            <script src="resource/bootstrap/jquery.js"></script>
            <script src="resource/bootstrap/bootstrap.js"></script></head>
            <body>
                <nav class="navbar navbar-inverse" role="navigation">
                    <div class="container-fluid">
                        <div class="navbar-header">     
                            <a class="navbar-brand" href="#">Guestbook</a>                            
                        </div>
                    </div>                    
                </nav>
                <div class="container"><div class="row">
            """)    
    

    greetings = ndb.gql('SELECT * '
                        'FROM Greeting '
                        'WHERE ANCESTOR IS :1 '
                        'ORDER BY date DESC LIMIT 10',
                        guestbook_key)

    for greeting in greetings:
      self.response.out.write("""<div class="panel panel-default">
                                   <div class="panel-heading">
                                     <h3 class="panel-title">""")
      if greeting.author:
        self.response.out.write('<b>%s</b> wrote:' % greeting.author.nickname())
      else:
        self.response.out.write('An anonymous person wrote: (%s)</h3></div>' % greeting.date)
      self.response.out.write('<div class="panel-body">%s </div></div>' %
                              cgi.escape(greeting.content))


    self.response.out.write("""</div></div><br/><br/><br/>
        <nav class="navbar navbar-default navbar-fixed-bottom">
          <div class="container">   
            <form action="/sign" method="post">
              <div class="input-group">              
                <input  class="form-control" type="text"  name="content" required="">            
                <div class="input-group-btn"> <input type="submit" value="Sign Guestbook" class="btn btn-default"></div>              
              </div>
            </form>
          </div>          
        </body>        
      </html>""")


class Guestbook(webapp2.RequestHandler):
  def post(self):
    greeting = Greeting(parent=guestbook_key)

    if users.get_current_user():
      greeting.author = users.get_current_user()

    greeting.content = self.request.get('content')
    greeting.put()
    self.redirect('/')


app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/sign', Guestbook)
], debug=True)
