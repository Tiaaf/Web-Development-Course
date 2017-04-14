#import hashlib #less secure than hmac
import hmac
import random
import string
import os
import jinja2
import webapp2
import re

from google.appengine.ext import db
template_dir = os.path.join(os.path.dirname(__file__),'templates')
#autoescape = True allows automatic escaping of html content
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

#Main content
class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)

    def render_str(self,template, **params):
        t= jinja_env.get_template(template)
        return t.render(params)
 
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
class MainPage(Handler):
    def get(self):
        self.render("mainPage.html")

    def post(self):
        self.redirect("/"+self.request.get("q"))

#birthdate
months = ['January',
              'February',
              'March',
              'April',
              'May',
              'June',
              'July',
              'August',
              'September',
              'October',
              'November',
              'December']

def valid_month(month):
    if month:
        if month.capitalize() in months:
            return month.capitalize()
        elif month.isdigit():
            monthN = int(month)
            if monthN >= 1 and monthN <= 12:
                return monthN

def valid_day(day):
    if day and day.isdigit():
        dayN = int(day)
        if dayN >= 1 and dayN <= 31:
            return dayN

def valid_year(year):
    if year and year.isdigit():
        yearN = int(year)
        if yearN >= 1900 and yearN <= 2020:
            return yearN

def escape_html(s):
    if s:
        i=0
        l = list(s)
        for c in l:
            if c==">":
                l[i]="&gt;"
            if c=="<":
                l[i]="&lt;"
            if c=="\"":
                l[i]="&quot;"
            if c=="&":
                l[i]="&amp;"
            i=i+1
        return "".join(l)
    else:
        return ""

class Birthdate(Handler):
    def render_form(self,error="",month="",day="",year=""):
        self.render("birthdate.html", error = escape_html(error),
                                    month = escape_html(month),
                                    day = escape_html(day),
                                    year = escape_html(year))

    def get(self):
        self.render_form()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')
        
        
        month = valid_month(self.request.get('month'))
        day = valid_day(self.request.get('day'))
        year = valid_year(self.request.get('year'))
    
        if not (month and day and year):
            self.render_form("This is not a valid birthday date noob !",user_month,user_day,user_year)
        else:
            self.redirect("/birthdate/thanks")


class Thanks(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks noob !")

#rot13
html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }

def html_escape(text):
    return escape(text, html_escape_table)

def escape_html(s):
    if s:
        i=0
        l = list(s)
        for c in l:
            if c==">":
                l[i]="&gt;"
            if c=="<":
                l[i]="&lt;"
            if c=="\"":
                l[i]="&quot;"
            if c=="&":
                l[i]="&amp;"
            i=i+1
        return "".join(l)
    else:
        return ""
                

def rot13(s):
    if s:
        l = list(s)
        i=0
        for c in l:
           if ord(c) >= 65 and ord(c) <= 90:
               l[i] = chr(((ord(c) -52)%26)+65)
           elif ord(c) >= 97 and ord(c) <= 122:
               l[i] = chr(((ord(c) -84)%26)+97)
           i=i+1
        return "".join(l)

    
class Rot13(Handler):
    def render_form(self,text=""):
        self.render("rot13form.html", text = escape_html(text))

    def get(self):
        self.render_form()

    def post(self):
        text = rot13(self.request.get('text'))
                
        self.render_form(text)

#shopping list
class Shopping(Handler):
    def render_form(self,items=""):
        self.render("shopping_list.html", items = items)

    def get(self):
        items = self.request.get_all("food")
        self.render_form(items)

#fizzbuzz
class Fizzbuzz(Handler):
    def render_form(self,n):
        self.render("fizzbuzz.html",n=int(n))

    def get(self):
        n = self.request.get("n")
        if not n:
            n = 0
        self.render_form(n)
        
#ascii
class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    
class ASCII(Handler):
    def render_form(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
        self.render("ascii.html", title=title, art=art, error=error, arts = arts)
        
    def get(self):
        self.render_form()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            a = Art(title = title, art = art)
            a.put()

            self.redirect("/ascii")
            
        else:
            error = "Nub !"
            self.render_form(title,art,error)

#blog
class Text(db.Model):
    title = db.StringProperty(required = True)
    text = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    def render(self):
        self._render_text = self.text.replace('\n','<br>')
        return render_str("post.html", text = self)
    
class Blog(Handler):
    def render_form(self):
        #texts = Text.all().order('-created')
        texts = db.GqlQuery("SELECT * FROM Text ORDER BY created LIMIT 10")
        self.render("blog.html", texts = texts)

    def get(self):
        self.render_form()

class NewPost(Handler):
    def render_form(self,title="",text="",error=""):
        self.render("newpost.html",title = title ,text = text,error = error)

    def get(self):
        self.render_form()
        
    def post(self):
        title = self.request.get("subject")
        text = self.request.get("content")
        
        if title and text:
            t = Text(title = title, text = text)
            t.put()
            text_id = str(t.key().id())
            
            self.redirect('/blog/'+text_id,text_id)

        else:
            error = "Nub !"
            self.render_form(title,text,error)

class IdPost(Handler):
    def render_form(self,text_id):
        text = Text.get_by_id(int(text_id),None)

        if text:
            self.render("permalink.html",text = text)
            return

        self.error(404)
        

    def get(self,text_id):
        self.render_form(text_id)

#visits
SECRET = "a4L5i4C0e3I9n7W1o2N6d5E0r1L+a1N=d11"

def hash_str(s):
    #return hashlib.md5(s).hexdigest() #less secure than hmac
    return hmac.new(SECRET,s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    s = h.split("|")[0]
    if make_secure_val(s) == h:
        return s
    else:
        return None
    
class Visits(Handler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        visits = 0
        visit_cookie_val = self.request.cookies.get('visits')
        if visit_cookie_val:
            cookie_val = check_secure_val(visit_cookie_val)
            if cookie_val:
                visits = int(cookie_val)
                
        visits = visits + 1

        new_cookie_val = make_secure_val(str(visits))


        self.response.headers.add_header('Set-Cookie','visits=%s' % new_cookie_val)

        if visits >= 100000:
            self.write("Luv luv <3\n\n %s times on our website it's wonderful !" % visits)
        else:
            self.write("You've been here %s times !" % visits)

#signUp
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASSWORD_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)

def make_salt():
    return ''.join(random.choice(string.letters) for x in range(5))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hmac.new(SECRET,name+pw+salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split('|')[1]
    return h == make_pw_hash(name,pw,salt)

# class Users(db.Model):
#     user_id = db.StringProperty(required = True)
#     password = db.StringProperty(required = True)
#     email = db.StringProperty(required = False)
#     created = db.DateTimeProperty(auto_now_add = True)

#     def already_exists(user_id_entered):
#         if user_id_entered:
#             db.GqlQuery("SELECT * FROM Users WHERE user_id=user_id_entered")
    
class SignUp(Handler):
    def render_form(self,errorUsername="",errorPassword="",errorVerify="",errorEmail=""):
        self.render("signupform1.html", errorUsername = errorUsername,
                                        errorPassword = errorPassword,
                                        errorVerify = errorVerify,
                                        errorEmail = errorEmail)
    
    def get(self):
        self.render_form()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        errorUsername = ""
        errorPassword = ""
        errorVerify = ""
        errorEmail = ""
        
        if valid_username(username) and valid_password(password) and password == verify and (valid_email(email) or email == ""):
            self.request.cookies
            self.redirect("/signup/welcome?username="+username)
        if not valid_username(username):
            errorUsername="That's not a valid username."
        if not valid_password(password):
            errorPassword="That wasn't a valid password."
        elif password != verify:
            errorVerify="Your passwords didn't match."
        if not (valid_email(email) or email==""):
            errorEmail="That's not a valid email."
            
        self.render_form(errorUsername,errorPassword,errorVerify,errorEmail)


class Welcome(Handler):
    def render_form(self,username=""):
        self.render("signupform2.html",username = username)

    def get(self):
        username = self.request.get('username')
        self.render_form(username)



            
app = webapp2.WSGIApplication([('/',MainPage),
                               ('/birthdate',Birthdate),
                               ('/birthdate/thanks',Thanks),
                               ('/rot13',Rot13),
                               ('/ascii',ASCII),
                               ('/shopping',Shopping),
                               ('/fizzbuzz',Fizzbuzz),
                               ('/signup',SignUp),
                               ('/signup/welcome',Welcome),
                               ('/blog',Blog),
                               ('/blog/newpost',NewPost),
                               ('/blog/(\d+)',IdPost),
                               ('/visits',Visits)
                                ],
                               debug=True)
