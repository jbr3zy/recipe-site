import webapp2
import os
import cgi
from google.appengine.ext.webapp import template
from google.appengine.ext import db


class Comment(db.Model):
  name = db.StringProperty(required=True)
  comment = db.StringProperty()

class Recipe(db.Model):
    title = db.StringProperty(required=True)
    #author
    #picture(s)
    description = db.StringProperty()
    cook_time = db.IntegerProperty()


class Ingredient(db.Model):
    text = db.StringProperty(required=True)
    recipe = db.ReferenceProperty(Recipe,
                                  collection_name='ingredients')


class Instruction(db.Model):
    text = db.StringProperty(required=True)
    recipe = db.ReferenceProperty(Recipe,
                                  collection_name='instructions')


class MainPage(webapp2.RequestHandler):
    def get(self):

        # Capture recipes from DB query
        recipes = db.GqlQuery('SELECT * FROM Recipe')

        # Add recipes to template values
        template_values = {
            'recipes': recipes
        }

        self.response.headers['Content-Type'] = 'text/html'
        path = os.path.join(os.path.dirname(__file__), 'helloworld.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
    	# instantiate a recipe with the values from the form data
        rec = Recipe(title=self.request.get('title'),
        			 description=self.request.get('description'),
                     cook_time=int(self.request.get('cook_time')))
        db.put(rec) # Save values to DB

        # Re-direct the user to the home page
        self.redirect('/')


class CommentPage(webapp2.RequestHandler):
    def get(self):
        # Capture comments from DB query
        comments = db.GqlQuery('SELECT * FROM Comment')

        # Generate HTML response string
        response = '<html>'
        for comment in comments:
            response += '<b>'+comment.name+'</b>'+' '+comment.comment+'<br />'
        response += '</html>'

        # Write the response!
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(response)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/comments', CommentPage)
], debug=True)