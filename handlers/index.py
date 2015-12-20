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
    self.response.write(template.render({}))
  
  def post(self):
    start_date_raw = self.request.get('start_date')
    end_date_raw = self.request.get('end_date')
    start_date = datetime.strptime(start_date_raw, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_raw, '%Y-%m-%d')
    number_of_plans = int(self.request.get('number_of_plans'))
    result = ldsconf.studyplan.generate_study_plan(start_date, end_date, number_of_plans, GAE_CONFERENCE_FILE)
    template = JINJA_ENVIRONMENT.get_template('plan.html')
    self.response.write(template.render({'plans': result}))



app = webapp2.WSGIApplication([
  ('/', IndexHandler),
], debug=True)
