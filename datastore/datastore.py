import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users


class Greeting(db.Model):
  """Models an individual Guestbook entry with an author, content, and date."""
  author = db.StringProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
  def get(self):
    # header
    self.response.out.write("""<html><body>""")
    
    # query the datastore
    greetings = db.GqlQuery("SELECT * FROM Greeting ORDER BY date DESC LIMIT 10")

    # display the greetings
    for greeting in greetings:
      if greeting.author:
        self.response.out.write('<b>%s</b> wrote:' % greeting.author)
      else:
        self.response.out.write('An anonymous person wrote:')
      self.response.out.write('<blockquote>%s</blockquote>' % cgi.escape(greeting.content))
                              
    # submission form
    self.response.out.write("""
          <form action="/sign" method="post">
              <div><textarea name="content" rows="3" cols="60"></textarea></div>
              <div><input type="submit" value="Sign Guestbook"></div>
          </form>""")
    # footer
    self.response.out.write("""</body></html>""")


class Guestbook(webapp2.RequestHandler):
  def post(self):
    greeting = Greeting()

    if users.get_current_user():
      greeting.author = users.get_current_user().nickname()

    greeting.content = self.request.get('content')
    key = greeting.put()
    self.redirect('/')


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/sign', Guestbook)],
                              debug=True)
