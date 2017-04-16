from handlers.base import *
from handlers.birthdate import *
from handlers.rot13 import *
from handlers.asciiChan import *
from handlers.shopping import *
from handlers.fizzbuzz import *
from handlers.signup import *
from handlers.blog import *
from handlers.visits import *
from handlers.json import *

app = webapp2.WSGIApplication([('/',MainPage),
                               ('/birthdate',Birthdate),
                               ('/birthdate/thanks',Thanks),
                               ('/rot13',Rot13),
                               ('/ascii',ASCII),
                               ('/shopping',Shopping),
                               ('/fizzbuzz',Fizzbuzz),
                               ('/signup',SignUp),
                               ('/login',Login),
                               ('/logout',Logout),
                               ('/signup/welcome',Welcome),
                               ('/blog',Blog),
                               ('/blog/newpost',NewPost),
                               ('/blog/(\d+)',IdPost),
                               ('/visits',Visits)
                                ],
                               debug=True)
