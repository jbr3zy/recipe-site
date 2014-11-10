# Importing libraries
import webapp2
import os
import cgi
from google.appengine.ext.webapp import template
from google.appengine.ext import db


class Recipe(db.Model):
    title = db.StringProperty(required=True)
    #author
    #picture(s)
    description = db.TextProperty()
    cook_time = db.IntegerProperty()


class Ingredient(db.Model):
    #text = db.StringProperty(required=True)
    text = db.TextProperty(required=True)
    recipe = db.ReferenceProperty(Recipe,
                                  collection_name='ingredients')


class Instruction(db.Model):
    #text = db.StringProperty(required=True)
    text = db.TextProperty(required=True)
    recipe = db.ReferenceProperty(Recipe,
                                  collection_name='instructions')

# Request handler for homepage
class MainPage(webapp2.RequestHandler):
    def get(self):
        # Capture recipes from DB query
        recipes = db.GqlQuery('SELECT * FROM Recipe')

        # Add recipes to template values
        template_values = {
            'recipes': recipes
        }

        self.response.headers['Content-Type'] = 'text/html'
        path = os.path.join(os.path.dirname(__file__), 'home.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
    	# instantiate a recipe with the values from the form data
        rec = Recipe(title=self.request.get('title'),
        			 description=self.request.get('description'),
                     cook_time=int(self.request.get('cook_time')))
        db.put(rec) # Save values to DB


        ingredient = Ingredient(text=self.request.get('ingredient'),
                                recipe=rec)

        instruction = Instruction(text=self.request.get('instruction'),
                                recipe=rec)


        db.put(ingredient)
        db.put(instruction)


        # Re-direct the user to the home page
        self.redirect('/')

# Request handler for individual recipe page
class RecipePage(webapp2.RequestHandler):
    def get(self):
        # Capture the recipe from DB query
        recipe = db.GqlQuery('SELECT * FROM Recipe WHERE __key__ = KEY(:1)', self.request.get('recipe_id')).get()

        # Add recipe to template values
        template_values = {
            'recipe': recipe
        }

        self.response.headers['Content-Type'] = 'text/html'
        path = os.path.join(os.path.dirname(__file__), 'recipe.html')
        self.response.out.write(template.render(path, template_values))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/recipe', RecipePage)
], debug=True)