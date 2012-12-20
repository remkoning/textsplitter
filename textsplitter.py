import os
import webapp2
import jinja2
from google.appengine.ext import db

from image_list import image_list
image_list.sort()


image_index = {'durkheim':0,
              'erwyn':861, 'anupom':6460}
max_index   = {'durkheim':len(image_list),
               'erwyn':6001, 'anupom':len(image_list)}


big_fields  = ['BASIC FUNCTION AND RESPONSIBILITY',
               'CHARACTERISTIC DUTIES AND RESPONSIBILITIES',
               'DESIRABLE QUALIFICATIONS',
               'QUALIFICATIONS',
               'RELATED DUTIES',
               'SUPERVISION EXERCISED',
               'SUPERVISION RECEIVED',
               'TEXT BELOW TITLE']

fields      = ['NECESSARY QUALIFCIATIONS',
               'DUTIES']


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env    = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Selection(db.Model):
    image    = db.StringProperty(required = True)
    image_i  = db.IntegerProperty(required = True)
    field    = db.StringProperty(required = True)

    mouse_x0 = db.IntegerProperty(required = True)
    mouse_y0 = db.IntegerProperty(required = True)
    mouse_x1 = db.IntegerProperty(required = True)
    mouse_y1 = db.IntegerProperty(required = True)

    skew     = db.IntegerProperty(required = True)

    workerid = db.StringProperty(required = True)

    sel_time = db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):
    def get(self):
        workerid = self.request.get_all("workerid")
        if len(workerid) == 0:
          workerid = 'durkheim'
        else:
          workerid = workerid[0]
        fields.sort()
        self.render("split_text.html", image_url = image_list[image_index[workerid]],
                                       worker_id = workerid,
                                       image_num = image_index[workerid],
                                       fields    = fields,
                                       big_fields = big_fields)
        #self.render("turk_split_text.html")


    def post(self):

        workerid = self.request.get("workerid")

        try:
            image_i  = int(self.request.get("image_num"))
        except:
            image_i = image_index[workerid]
        image_u  = image_list[image_i]

        mouse_x0 = int(self.request.get("mouseX0"))
        mouse_y0 = int(self.request.get("mouseY0"))
        mouse_x1 = int(self.request.get("mouseX1"))
        mouse_y1 = int(self.request.get("mouseY1"))
        field    = self.request.get("submit")
        newfield = self.request.get("newfield")


        if field[0] != ":":
            if field == "Move to Document Number:":
                    image_index[workerid] = image_i
            if field == "Move Back a Document":
                image_index[workerid] = max(image_i - 1, 0)
            if field == "Move Forward a Document":
                image_index[workerid] = image_i + 1

            if not (image_index[workerid] < max_index[workerid]):
                self.write("You have finished your set of documents! Please contact me and so that I know you have completed your job.")
            else:
                self.redirect('/' + '?workerid=' + workerid)

        else:
            prefix    = field[0:3]
            field_val = field[3:]

            if field_val == "SKEW":
                skew = 1
            else:
                skew = 0

            if field_val == "NEW FIELD":
                if (newfield.upper() not in fields) and (newfield.upper() not in big_fields):
                    fields.append(newfield.upper())
                field_val = newfield.upper()

            s = Selection(image    = image_u,
                          image_i  = image_i,
                          field    = field_val,
                          skew     = skew,
                          mouse_x0 = mouse_x0,
                          mouse_y0 = mouse_y0,
                          mouse_x1 = mouse_x1,
                          mouse_y1 = mouse_y1,
                          workerid = workerid)
            s.put()

            if prefix == ":N:":
              image_index[workerid] = image_i + 1

            if not (image_index[workerid] < max_index[workerid]):
                self.write("You have finished your set of documents! Please contact me and so that I know you have completed your job.")
            else:
                self.redirect('/' + '?workerid=' + workerid)


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)