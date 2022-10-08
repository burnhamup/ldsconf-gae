from datetime import datetime
import os
import jinja2
import webapp2

import ldsconf.studyplan

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
      os.path.join(os.path.dirname(__file__), '..','templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

GAE_CONFERENCE_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'conferences.json')


class IndexHandler(webapp2.RequestHandler):
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('index.html')
    default_start_date, default_end_date = ldsconf.studyplan.get_default_dates()
    template_args = {
      'default_start_date': default_start_date,
      'default_end_date': default_end_date,
    }
    self.response.write(template.render(template_args))
  
  def post(self):
    try:
      start_date_raw = self.request.get('start_date')
      end_date_raw = self.request.get('end_date')
      start_date = datetime.strptime(start_date_raw, '%Y-%m-%d')
      end_date = datetime.strptime(end_date_raw, '%Y-%m-%d')
      number_of_plans = int(self.request.get('number_of_plans'))
    except:
      template = JINJA_ENVIRONMENT.get_template('error.html')
      self.response.write(template.render({}))
      return


    result = ldsconf.studyplan.generate_study_plan(start_date, end_date, number_of_plans, GAE_CONFERENCE_FILE)

    template = JINJA_ENVIRONMENT.get_template('plan.html')
    self.response.write(template.render({'plans': result}))


class ExampleHandler(webapp2.RequestHandler):
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('example.html')
    self.response.write(template.render())


class RSSExampleHandler(webapp2.RequestHandler):
  def get(self):
    pass



app = webapp2.WSGIApplication([
  ('/', IndexHandler),
  ('/example', ExampleHandler),
  ('/example/rss', RSSExampleHandler)
], debug=True)
